#!/bin/bash
source .venv/bin/activate
pip install -r requirements.txt
export  GOOGLE_APPLICATION_CREDENTIALS="secrets/credentials.json"
streamlit run streamlit_app.py