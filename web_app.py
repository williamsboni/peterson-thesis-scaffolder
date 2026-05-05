import streamlit as st
import os
import json
import tempfile
from scaffold_engine import ScaffoldingEngine
from pdf_export import export_outline_to_pdf
from llm_utils import LLMMapper

# Set page config
st.set_page_config(page_title="Thesis Scaffolder", layout="wide")

# Constants
TEMPLATES_DIR = 'data/templates'
OUTPUT_DIR = tempfile.gettempdir()

def get_available_universities():
    templates = []
    if os.path.exists(TEMPLATES_DIR):
        for file in os.listdir(TEMPLATES_DIR):
            if file.endswith('.json'):
                path = os.path.join(TEMPLATES_DIR, file)
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        templates.append({
                            "name": data['metadata']['institution'],
                            "file": file,
                            "path": path
                        })
                except Exception:
                    continue
    return templates

def main():
    st.title("🎓 Automated Project & Thesis Scaffolder")
    st.markdown("""
    Scaffold your thesis outline based on your institution's specific requirements. 
    Upload your raw notes, and our AI will structure them into the correct chapters and identify research gaps.
    """)

    # Sidebar - University Selection
    st.sidebar.header("Settings")
    universities = get_available_universities()
    if not universities:
        st.error("No institutional templates found in shared directory.")
        return

    uni_names = [u['name'] for u in universities]
    selected_uni_name = st.sidebar.selectbox("Select your University", uni_names)
    selected_uni = next(u for u in universities if u['name'] == selected_uni_name)

    # Input Section
    st.header("Input Research Notes")
    input_method = st.radio("Choose input method:", ("Paste Text", "Upload File"))

    notes_content = ""
    if input_method == "Paste Text":
        notes_content = st.text_area("Paste your raw research notes or topic brief here:", height=300)
    else:
        uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"])
        if uploaded_file is not None:
            notes_content = uploaded_file.read().decode("utf-8")

    if st.button("Generate Scaffolding"):
        if not notes_content.strip():
            st.warning("Please provide some research notes first.")
        else:
            with st.spinner("Processing your notes..."):
                try:
                    # 1. Initialize Engine
                    engine = ScaffoldingEngine(selected_uni['path'])
                    
                    # 2. Generate Outline
                    outline_md = engine.generate_outline(notes_content)
                    
                    # 3. Store in session state for later download
                    st.session_state['outline_md'] = outline_md
                    st.session_state['selected_uni'] = selected_uni
                    
                    st.success("Scaffolding generated successfully!")
                except Exception as e:
                    st.error(f"Error generating scaffolding: {str(e)}")

    # Results Section
    if 'outline_md' in st.session_state:
        st.divider()
        st.header("Structured Thesis Outline")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(st.session_state['outline_md'])
            
        with col2:
            st.subheader("Actions")
            
            # Export to PDF
            if st.button("Prepare PDF Download"):
                with st.spinner("Creating PDF..."):
                    try:
                        # Create temp files for conversion
                        md_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
                        md_temp.write(st.session_state['outline_md'].encode('utf-8'))
                        md_temp.close()
                        
                        pdf_path = os.path.join(OUTPUT_DIR, f"{st.session_state['selected_uni']['file'].replace('.json', '')}_outline.pdf")
                        
                        export_outline_to_pdf(st.session_state['selected_uni']['path'], md_temp.name, pdf_path)
                        
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                            
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
                        
                        os.unlink(md_temp.name) # Cleanup
                    except Exception as e:
                        st.error(f"Error creating PDF: {str(e)}")

if __name__ == "__main__":
    main()
