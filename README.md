# Peterson Enterprises: Automated Thesis Scaffolder

This is the public deployment package for the Automated Project & Thesis Structuring startup.

## How to Deploy to Streamlit Cloud

1.  **Create a GitHub Repository**: Create a new repository on GitHub (e.g., `thesis-scaffolder`).
2.  **Upload Files**: Upload all files from this `deploy` folder to your new repository.
    - `web_app.py`
    - `scaffold_engine.py`
    - `llm_utils.py`
    - `pdf_export.py`
    - `requirements.txt`
    - `data/templates/` (folder with all JSON files)
3.  **Connect to Streamlit Cloud**:
    - Go to [share.streamlit.io](https://share.streamlit.io).
    - Sign in with GitHub.
    - Click "New app".
    - Select your repository and set the Main file path to `web_app.py`.
4.  **Add Secrets (Optional)**:
    - If you have an OpenAI API key, add it in the Streamlit Cloud "Settings" -> "Secrets" as:
      ```toml
      OPENAI_API_KEY = "your_key_here"
      ```
    - The app will automatically switch from 'Simulated' mode to 'Live' mode.

## Supported Institutions
- University of Lagos (UNILAG)
- Nnamdi Azikiwe University (UNIZIK)
- University of Nigeria, Nsukka (UNN)
- Obafemi Awolowo University (OAU)
- University of Ibadan (UI)
- Ahmadu Bello University (ABU)
