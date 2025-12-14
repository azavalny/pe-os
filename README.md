# Private Markets OS - Streamlit MVP

A comprehensive operating system for private equity and credit firms, integrating market intelligence, deal management, and investor relations.

## Features

### 🏠 Home - Today's Brief
- Daily market brief with key themes
- Inbox alerts and recent emails
- Quick search functionality
- Downloadable briefings

### 💡 Market Intel - Idea Scoring
- Ingest and analyze market snippets from research sources
- AI-powered theme tagging and insight extraction
- Score investment ideas based on thesis fit, novelty, and urgency
- Publish ideas to the deal board
- Track ideas through deal stages (idea → diligence → IC → closed)

### 📬 Inbox Agent - Email Triage
- AI-powered email relevance classification
- Automatic thesis tag extraction
- CRM update suggestions
- Link emails to deals and LP contacts

### 🏢 Deal Room - Document Intelligence
- **Q&A**: Ask questions about deal documents with AI-powered answers
- **IC Memo Generator**: Auto-generate IC memo outlines with key risks and questions
- **Document Comparison**: Compare versions of credit agreements, amendments, etc.
- **Covenant Tracking**: Monitor financial covenants with test dates and thresholds
- Downloadable reports for memos, comparisons, and covenant tables

## Tech Stack

- **UI**: Streamlit
- **Database**: SQLite with SQLAlchemy ORM
- **AI**: Pluggable LLM client (demo mode uses heuristics)
- **Search**: Keyword-based with optional vector search capability
- **Data Processing**: Pandas, NumPy
- **Text Matching**: RapidFuzz for document comparison

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create and activate virtual environment**:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env if needed (defaults work for demo)
```

## Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
private-markets-os/
├── app.py                      # Main Streamlit entrypoint
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
│
├── data/seed/                 # CSV seed data
│   ├── companies.csv
│   ├── deals.csv
│   ├── emails.csv
│   ├── market_snippets.csv
│   ├── documents.csv
│   ├── covenants.csv
│   ├── lps.csv
│   └── contacts.csv
│
├── pages/                     # Streamlit pages
│   ├── 1_Home.py
│   ├── 2_Market_Intel.py
│   ├── 3_Inbox_Agent.py
│   └── 4_Deal_Room.py
│
└── pm_os/                     # Core application logic
    ├── config.py              # Configuration management
    ├── db.py                  # Database setup
    ├── models.py              # SQLAlchemy models
    ├── schema.py              # Pydantic schemas
    ├── mock_data.py           # Database seeding
    │
    ├── llm/                   # LLM abstraction layer
    │   ├── client.py
    │   └── demo_mode.py
    │
    ├── services/              # Business logic
    │   ├── tagging.py         # Theme/keyword tagging
    │   ├── scoring.py         # Idea scoring
    │   ├── email_agent.py     # Email triage
    │   ├── docqa.py           # Document Q&A
    │   ├── compare.py         # Document comparison
    │   └── generators.py      # Report generators
    │
    └── ui/                    # UI components (extensible)
```

## Configuration

Edit `.env` file:

```env
DEMO_MODE=1                    # Set to 0 to use real LLM (requires implementation)
DB_PATH=./pm_os.sqlite         # SQLite database path
FIRM_NAME=Your Firm Name       # Displayed in UI
```

## Demo Mode

By default, the app runs in **DEMO_MODE** which:
- Uses deterministic heuristics instead of real AI
- Requires no API keys
- Generates consistent outputs based on input text
- Perfect for demonstrations and testing

## Data Model

### Core Entities
- **Companies**: Investment targets
- **Deals**: Active opportunities with stages and scores
- **Emails**: Inbox for triage
- **Market Snippets**: Research and market intelligence
- **Documents**: Credit agreements, CIMs, amendments
- **Covenants**: Financial covenant tracking
- **LPs**: Limited partner contacts
- **Contacts**: Broker/banker relationships

## Extending the Application

### Adding Real LLM Integration

1. Edit `pm_os/llm/client.py` to add your provider:
```python
if not settings.demo_mode:
    # Add OpenAI, Anthropic, Azure, etc.
    response = openai.chat.completions.create(...)
```

2. Set `DEMO_MODE=0` in `.env`

3. Add API keys to environment

### Adding Vector Search

1. Install optional dependencies:
```bash
pip install faiss-cpu sentence-transformers
```

2. Implement embedding generation in `pm_os/services/search.py`

3. Index documents and snippets on ingestion

## Development Roadmap

### Phase 1 - MVP ✅
- Core UI with 4 pages
- SQLite data storage
- Demo mode LLM responses
- Basic document operations

### Phase 2 - Intelligence
- Real LLM integration (OpenAI/Anthropic)
- Vector search with FAISS
- Enhanced document parsing
- Citation extraction

### Phase 3 - Integrations
- Salesforce/HubSpot CRM sync
- Email provider integration (Outlook/Gmail)
- Document storage (Dropbox/Box)
- Calendar integration

### Phase 4 - Collaboration
- Multi-user support
- Deal collaboration features
- IC workflow automation
- Reporting dashboards

## License

MIT License

## Support

For questions or issues, contact your development team.

