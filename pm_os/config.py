import os
from dataclasses import dataclass

try:
    import streamlit as st
    _use_streamlit_secrets = True
except ImportError:
    _use_streamlit_secrets = False

def _get_config_value(key: str, default: str = "") -> str:
    if _use_streamlit_secrets:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except (AttributeError, FileNotFoundError):
            return os.getenv(key, default)
    return os.getenv(key, default)

@dataclass(frozen=True)
class Settings:
    demo_mode: bool = _get_config_value("DEMO_MODE", "1") == "1"
    db_path: str = _get_config_value("DB_PATH", "./pm_os.sqlite")
    firm_name: str = _get_config_value("FIRM_NAME", "Private Markets OS")
    openai_api_key: str = _get_config_value("OPENAI_API_KEY", "")

settings = Settings()

