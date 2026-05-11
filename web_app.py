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
TEMPLATES_DIR = '/home/team/shared/data/templates'
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
    
    # Sidebar - University Selection
    st.sidebar.header("Settings")
    universities = get_available_universities()
    if not universities:
        st.error("No institutional templates found in shared directory.")
        return

    uni_names = [u['name'] for u in universities]
    selected_uni_name = st.sidebar.selectbox("Select your University", uni_names)
    selected_uni = next(u for u in universities if u['name'] == selected_uni_name)

    # Tabs for different modes
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Scaffolding Mode", "✍️ Full Writing Mode", "🚀 Final Review & Export", "🎓 Mock Defense & Red Flags"])

    with tab1:
        st.header("Step 1: Scaffold your Thesis")
        st.markdown("""
        Upload your raw notes, and our AI will structure them into the correct chapters and identify research gaps.
        """)

        # Input Section
        input_method = st.radio("Choose input method:", ("Paste Text", "Upload File"), key="input_method_tab1")

        notes_content = ""
        if input_method == "Paste Text":
            notes_content = st.text_area("Paste your raw research notes or topic brief here:", height=300, key="notes_tab1")
        else:
            uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"], key="file_tab1")
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
                        st.session_state['raw_notes'] = notes_content
                        
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

    with tab2:
        st.header("Step 2: Full Writing Engine")
        
        if 'outline_md' not in st.session_state:
            st.info("Please generate a scaffold in 'Scaffolding Mode' first to proceed with full writing.")
        else:
            from writing_engine import WritingEngine, StateStore
            
            # Initialize StateStore (using a default ID for now)
            if 'state_store' not in st.session_state:
                st.session_state['state_store'] = StateStore("demo_project")
            
            st.markdown("""
            The Full-Writing Engine generates detailed academic prose chapter-by-chapter based on your approved scaffold.
            """)
            
            # Map display names to chapter IDs
            chapter_map = {
                "Chapter 1: Introduction": "ch1",
                "Chapter 2: Literature Review": "ch2",
                "Chapter 3: Methodology": "ch3",
                "Chapter 4: Results": "ch4",
                "Chapter 5: Discussion": "ch5"
            }
            
            # Consistency Check Dashboard
            with st.expander("🔍 Consistency Check Dashboard", expanded=True):
                core = st.session_state['state_store'].get_core_context()
                if core:
                    st.success("✅ Core Research Context extracted.")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Research Questions:**")
                        for rq in core.get('research_questions', []):
                            st.write(f"- {rq}")
                    with col_b:
                        st.write("**Objectives:**")
                        for obj in core.get('objectives', []):
                            st.write(f"- {obj}")
                else:
                    st.warning("⚠️ Core Research Context not yet extracted. Draft and Finalize Chapter 1 to populate this.")

            selected_chapter_display = st.selectbox("Select Chapter to Draft", list(chapter_map.keys()))
            selected_chapter_id = chapter_map[selected_chapter_display]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Draft {selected_chapter_display}"):
                    with st.spinner(f"Writing {selected_chapter_display}..."):
                        try:
                            writing_engine = WritingEngine(st.session_state['selected_uni']['path'])
                            prose = writing_engine.draft_chapter(
                                selected_chapter_id, 
                                st.session_state['raw_notes'],
                                st.session_state['state_store']
                            )
                            st.success(f"{selected_chapter_display} drafted!")
                        except Exception as e:
                            st.error(f"Error: {e}")
            
            with col2:
                if selected_chapter_id == "ch1":
                    if st.button("Finalize Ch1 & Extract Context"):
                        with st.spinner("Extracting RQs and Objectives..."):
                            ch1_text = st.session_state['state_store'].get_chapter("ch1")
                            if ch1_text:
                                writing_engine = WritingEngine(st.session_state['selected_uni']['path'])
                                core_context = writing_engine.extract_core_context(ch1_text)
                                for k, v in core_context.items():
                                    st.session_state['state_store'].set_core_context(k, v)
                                st.success("Context extracted! Future chapters will now be consistent with Chapter 1.")
                            else:
                                st.error("Please draft Chapter 1 first.")

            current_draft = st.session_state['state_store'].get_chapter(selected_chapter_id)
            
            if current_draft:
                st.subheader(f"Draft for {selected_chapter_display}")
                edited_draft = st.text_area("Edit Draft", current_draft, height=400, key=f"edit_{selected_chapter_id}")
                if st.button("Save Changes", key=f"save_{selected_chapter_id}"):
                    st.session_state['state_store'].update_chapter(selected_chapter_id, edited_draft)
                    st.success("Draft updated.")
                
                st.markdown("---")
                st.subheader("Thesis Progress Summary")
                for display, ch_id in chapter_map.items():
                    status = "✅ Drafted" if st.session_state['state_store'].get_chapter(ch_id) else "⏳ Pending"
                    st.write(f"{display}: {status}")

    with tab3:
        st.header("Step 3: Final Review & Export")
        if 'state_store' not in st.session_state:
            st.info("No project state found. Start by scaffolding and drafting chapters in the previous tabs.")
        else:
            state = st.session_state['state_store']
            from writing_engine import WritingEngine, CitationEngine
            writing_engine = WritingEngine(st.session_state['selected_uni']['path'])
            
            # 1. Project Metadata Collection
            with st.expander("📝 Project Metadata (for Title Page & Prelims)", expanded=False):
                current_meta = state.get_project_metadata()
                with st.form("metadata_form"):
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        title = st.text_input("Project Title", value=current_meta.get('title', ''))
                        student_name = st.text_input("Student Name", value=current_meta.get('student_name', ''))
                        matric_no = st.text_input("Matriculation Number", value=current_meta.get('matric_no', ''))
                        degree = st.text_input("Degree (e.g., B.Sc. Economics)", value=current_meta.get('degree', ''))
                    with col_m2:
                        department = st.text_input("Department", value=current_meta.get('department', ''))
                        faculty = st.text_input("Faculty", value=current_meta.get('faculty', ''))
                        supervisor = st.text_input("Supervisor Name", value=current_meta.get('supervisor', ''))
                        date_str = st.text_input("Date (e.g., May, 2026)", value=current_meta.get('date', ''))
                    
                    if st.form_submit_button("Save Metadata"):
                        meta = {
                            "title": title, "student_name": student_name, "matric_no": matric_no,
                            "degree": degree, "department": department, "faculty": faculty,
                            "supervisor": supervisor, "date": date_str
                        }
                        state.set_project_metadata(meta)
                        st.success("Metadata saved!")

            # 2. Preliminary Pages Generation
            st.subheader("Preliminary Pages")
            if st.button("Generate/Reset Preliminary Pages"):
                prelims = writing_engine.generate_preliminary_pages(state.get_project_metadata(), st.session_state['selected_uni']['name'])
                state.update_chapter("prelims", prelims)
                st.success("Preliminary pages generated!")

            current_prelims = state.get_chapter("prelims")
            if current_prelims:
                edited_prelims = st.text_area("Edit Preliminary Pages", current_prelims, height=300, key="edit_prelims")
                if st.button("Save Preliminary Pages"):
                    state.update_chapter("prelims", edited_prelims)
                    st.success("Preliminary pages updated.")

            st.divider()
            
            # 3. Final Compilation
            drafted_chapters = [cid for cid, content in state.state["chapter_drafts"].items() if content and cid != "prelims"]
            
            if not drafted_chapters:
                st.warning("No chapters have been drafted yet. Complete some drafts in 'Full Writing Mode' first.")
            else:
                st.success(f"Chapters available for export: {', '.join(drafted_chapters)}")
                
                # Combine prose
                full_thesis_md = ""
                # Add Prelims if they exist
                prelims_content = state.get_chapter("prelims")
                if prelims_content:
                    full_thesis_md += prelims_content + "\n\n---\n\n"

                for cid in ["ch1", "ch2", "ch3", "ch4", "ch5"]:
                    content = state.get_chapter(cid)
                    if content:
                        full_thesis_md += content + "\n\n---\n\n"
                
                # Append Reference List
                ce = CitationEngine(state)
                ref_list = ce.generate_reference_list()
                full_thesis_md += ref_list
                
                st.subheader("Final Compilation Preview")
                st.markdown(full_thesis_md[:1000] + "...") # Show snippet in markdown for better preview
                
                if st.button("Generate Final PDF"):
                    with st.spinner("Compiling final, institutionally compliant PDF..."):
                        try:
                            md_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
                            md_temp.write(full_thesis_md.encode('utf-8'))
                            md_temp.close()
                            
                            pdf_path = os.path.join(OUTPUT_DIR, "final_thesis_draft.pdf")
                            export_outline_to_pdf(st.session_state['selected_uni']['path'], md_temp.name, pdf_path)
                            
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()
                                
                            st.download_button(
                                label="📥 Download Final Thesis PDF",
                                data=pdf_bytes,
                                file_name="Final_Thesis_Draft.pdf",
                                mime="application/pdf"
                            )
                            os.unlink(md_temp.name)
                        except Exception as e:
                            st.error(f"Export error: {e}")

    with tab4:
        st.header("Step 4: Mock Defense & Red Flag Checker")
        if 'state_store' not in st.session_state:
            st.info("No project state found. Draft your thesis first.")
        else:
            from writing_engine import DefenseEngine
            de = DefenseEngine(st.session_state['state_store'])
            
            st.markdown("""
            This section helps you prepare for your project defense by checking for inconsistencies (Red Flags) 
            and suggesting strong academic responses to common panelist questions.
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚩 Red Flag Checker")
                st.write("Scan your project for misalignment or weak research design.")
                if st.button("Run Red Flag Scan"):
                    with st.spinner("Analyzing project consistency..."):
                        report = de.check_red_flags()
                        st.info("Scanner results are based on institutional standards for Nigeria.")
                        st.markdown(report)
            
            with col2:
                st.subheader("👨‍🏫 Mock Defense Prep")
                st.write("Generate suggested answers to tough panel questions based on your specific findings.")
                if st.button("Generate Defense Prep"):
                    with st.spinner("Preparing responses based on your drafted chapters..."):
                        responses = de.generate_defense_answers()
                        st.markdown(responses)

if __name__ == "__main__":
    main()
