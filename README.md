# 🎓 Peterson Thesis: Automated Project & Thesis Engine

Peterson Thesis is an end-to-end AI-powered academic success platform designed specifically for students in Nigerian tertiary institutions. It transforms raw research notes into high-fidelity, institutionally compliant thesis drafts, complete with citations, preliminary pages, and defense preparation.

## 🚀 Core Features

1. **Intelligent Scaffolding**: Automatically maps messy research notes to formal chapter outlines based on specific university guidelines (UNIZIK, UNILAG, UNN, OAU, UI, ABU).
2. **Full-Writing Engine**: Generates professional academic prose for all 5 chapters while maintaining "The Golden Thread" of logical consistency across Research Questions, Objectives, and Findings.
3. **Institutional Compliance**: Supports dual-page numbering (Roman/Arabic), standard title pages, declarations, certifications, and abstracts tailored to your specific university.
4. **Automated Citations**: Extracts Author-Year placeholders and generates a fully formatted APA Reference List.
5. **Mock Defense & Red Flag Checker**: Analyzes your draft for academic weaknesses (misalignment, weak methodology) and generates suggested responses to common defense panel questions.

## 🛠️ How to Deploy

### 1. External Deployment (GitHub + Streamlit)
1. **Create a GitHub Repository**: Create a new repository on GitHub.
2. **Upload Files**: Upload the contents of this deployment package.
3. **Connect to Streamlit Cloud**:
    - Go to [share.streamlit.io](https://share.streamlit.io).
    - Select your repository and set the Main file path to `web_app.py`.
4. **Configure API Keys**:
    - Add your `OPENAI_API_KEY` to Streamlit's "Secrets" settings to enable live LLM generation.

### 2. Local Deployment
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run web_app.py
   ```

## 📂 Project Structure
- `web_app.py`: The unified Streamlit interface.
- `writing_engine.py`: Core logic for chapter drafting and state management.
- `scaffold_engine.py`: Logic for mapping notes to institutional templates.
- `llm_utils.py`: Prompt engineering and LLM integration (OpenAI).
- `pdf_export.py`: Custom FPDF engine for institutionally compliant document generation.
- `data/`: Contains institutional JSON templates.

## 🏛️ Supported Universities
- Nnamdi Azikiwe University (UNIZIK)
- University of Lagos (UNILAG)
- University of Nigeria, Nsukka (UNN)
- Obafemi Awolowo University (OAU)
- University of Ibadan (UI)
- Ahmadu Bello University (ABU)

---
*Built by Peterson Enterprises*
