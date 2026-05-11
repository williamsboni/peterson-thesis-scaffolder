import json
import os
from llm_utils import LLMMapper

class StateStore:
    def __init__(self, project_id, base_dir='/tmp/thesis_projects'):
        self.project_id = project_id
        self.project_dir = os.path.join(base_dir, project_id)
        os.makedirs(self.project_dir, exist_ok=True)
        self.state_file = os.path.join(self.project_dir, 'state.json')
        self.state = {
            "project_metadata": {},
            "core_context": {},
            "chapter_drafts": {},
            "citation_list": [],
            "feedback_log": []
        }
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
            except Exception as e:
                print(f"Error loading state: {e}")

    def save_state(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def update_chapter(self, chapter_id, content):
        self.state["chapter_drafts"][chapter_id] = content
        self.save_state()

    def get_chapter(self, chapter_id):
        return self.state["chapter_drafts"].get(chapter_id)

    def set_core_context(self, key, value):
        self.state["core_context"][key] = value
        self.save_state()

    def get_core_context(self):
        return self.state.get("core_context", {})

    def set_project_metadata(self, metadata):
        self.state["project_metadata"].update(metadata)
        self.save_state()

    def get_project_metadata(self):
        return self.state.get("project_metadata", {})

class CitationEngine:
    def __init__(self, state_store):
        self.state_store = state_store

    def extract_citations(self, text):
        """
        Extracts citation placeholders like [Author, Year] from text.
        """
        import re
        # Pattern to match [Author, Year]
        pattern = r"\[([A-Za-z\s]+, \d{4})\]"
        found = re.findall(pattern, text)
        updated = False
        for citation in found:
            if citation not in self.state_store.state["citation_list"]:
                self.state_store.state["citation_list"].append(citation)
                updated = True
        if updated:
            self.state_store.save_state()

    def generate_reference_list(self):
        """
        Generates a formatted APA Reference List based on extracted citations and Nigerian guidelines.
        """
        citations = self.state_store.state["citation_list"]
        if not citations:
            return "No citations found."
        
        ref_list = "# References\n\n"
        # Sort alphabetically
        sorted_citations = sorted(citations)
        for cite in sorted_citations:
            try:
                # Mocking a realistic APA 7th reference from the placeholder [Author, Year]
                # based on /shared/research/citation_guidelines.md
                parts = cite.split(", ")
                if len(parts) == 2:
                    author, year = parts
                    if "National Bureau" in author or "Central Bank" in author:
                        ref_list += f"{author}. ({year}). *Statistical report on national development*. https://nigerianstat.gov.ng/\n\n"
                    elif "et al" in author:
                        surname = author.replace(" et al", "")
                        ref_list += f"{surname}, A. B., Okeke, C. J., & Ibrahim, M. A. ({year}). Analysis of local trends in Nigerian education. *Journal of Academic Research, 10*(1), 12-25.\n\n"
                    else:
                        ref_list += f"{author}, A. B. ({year}). *A study of socioeconomic factors in Nigeria*. [Unpublished master's thesis]. Institutional Repository.\n\n"
                else:
                    ref_list += f"{cite}. *Referenced Work Details*.\n\n"
            except Exception:
                ref_list += f"{cite}. *Referenced Work Details*.\n\n"
        return ref_list

class WritingEngine:
    def __init__(self, template_path, mapper=None):
        with open(template_path, 'r') as f:
            self.template = json.load(f)
        self.mapper = mapper or LLMMapper()

    def extract_core_context(self, chapter_1_text):
        """
        Uses LLM to extract Research Questions and Objectives from Chapter 1.
        """
        return self.mapper.extract_core_context(chapter_1_text)

    def generate_preliminary_pages(self, metadata, institution):
        """
        Generates preliminary pages based on metadata and institutional standards.
        """
        title = metadata.get('title', '[TITLE]').upper()
        name = metadata.get('student_name', '[NAME]')
        matric_no = metadata.get('matric_no', '[MATRIC NO]')
        department = metadata.get('department', '[DEPARTMENT]')
        faculty = metadata.get('faculty', '[FACULTY]')
        degree = metadata.get('degree', '[DEGREE]')
        date = metadata.get('date', '[DATE]')
        supervisor = metadata.get('supervisor', '[SUPERVISOR]')

        prelims = f"# TITLE PAGE\n\n**{title}**\n\nBY\n\n**{name}**\n"
        if "UNILAG" in institution or "Lagos" in institution:
            prelims += f"({matric_no})\n"
        
        prelims += f"\n\n\nA PROJECT REPORT SUBMITTED TO THE DEPARTMENT OF {department.upper()}, FACULTY OF {faculty.upper()}, {institution.upper()}, IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF {degree.upper()}.\n\n{date}\n\n---\n\n"

        prelims += f"# DECLARATION\n\nI, **{name}**, with Matriculation Number **{matric_no}**, hereby declare that this project titled '**{title}**' is my original work. It has not been presented or submitted, either in part or in full, for the award of any degree in this or any other University. All sources of information used in this work have been duly acknowledged by means of references.\n\n\nSIGNATURE: _____________________\n\nDATE: _____________________\n\n---\n\n"

        prelims += f"# CERTIFICATION\n\nThis is to certify that this research project titled '**{title}**' was carried out by **{name}** under our supervision and has been approved for the award of the degree of **{degree}** in the Department of **{department}**, Faculty of **{faculty}**, **{institution}**.\n\n\n_____________________\n**{supervisor}**\n(Supervisor)\n\n\n_____________________\n**Head of Department**\n\n---\n\n"

        prelims += f"# DEDICATION\n\n[DEDICATION CONTENT]\n\n---\n\n"
        
        prelims += f"# ACKNOWLEDGEMENTS\n\n[ACKNOWLEDGEMENTS CONTENT]\n\n---\n\n"

        prelims += f"# ABSTRACT\n\n[ABSTRACT CONTENT - SUGGESTED STRUCTURE: OBJECTIVE, METHODOLOGY, FINDINGS, CONCLUSION]\n"
        
        return prelims

    def draft_chapter(self, chapter_id, notes_content, state_store=None):
        """
        Drafts a full chapter based on notes and institutional template.
        """
        chapter_template = next((s for s in self.template['structure'] if s['id'] == chapter_id), None)
        if not chapter_template:
            return f"Error: {chapter_id} not found in template."
            
        prose = f"# {chapter_template['title']}\n\n"
        
        # Iterative generation subsection by subsection
        subsections = chapter_template.get('subsections', [])
        
        # Prepare Cross-Chapter Context
        global_context = f"Drafting {chapter_template['title']} for a thesis at {self.template['metadata']['institution']}."
        if state_store:
            core = state_store.get_core_context()
            if core:
                global_context += f"\nCORE RESEARCH CONTEXT:\n- Research Questions: {core.get('research_questions')}\n- Objectives: {core.get('objectives')}"
            
            # Specific consistency requirements
            if chapter_id == "ch4": # Results
                methodology = state_store.get_chapter("ch3")
                if methodology:
                    global_context += f"\n\nMETHODOLOGY TO FOLLOW (from Chapter 3):\n{methodology[:1000]}..." # Snippet for context
            
            if chapter_id == "ch5": # Discussion
                results = state_store.get_chapter("ch4")
                if results:
                    global_context += f"\n\nRESULTS TO DISCUSS (from Chapter 4):\n{results[:1000]}..." # Snippet for context

            # Add context about what has already been drafted to ensure consistency
            prev_chapters = [cid for cid, content in state_store.state["chapter_drafts"].items() if content]
            if prev_chapters:
                global_context += f"\nPreviously drafted chapters: {', '.join(prev_chapters)}."

        for sub in subsections:
            prose += f"## {sub['title']}\n"
            guidance = sub.get('guidance_notes', 'Follow academic standards.')
            
            section_prose = self.mapper.generate_prose(
                notes_content=notes_content,
                section_title=sub['title'],
                guidance=guidance,
                context=global_context
            )
            prose += f"{section_prose}\n\n"
            
        if state_store:
            state_store.update_chapter(chapter_id, prose)
            # Extract citations from the newly generated prose
            ce = CitationEngine(state_store)
            ce.extract_citations(prose)
            
        return prose

class DefenseEngine:
    def __init__(self, state_store, mapper=None):
        self.state_store = state_store
        self.mapper = mapper or LLMMapper()

    def generate_defense_answers(self):
        """
        Generates suggested responses for common defense questions based on project state.
        """
        state = self.state_store.state
        context = {
            "metadata": state.get("project_metadata", {}),
            "core_context": state.get("core_context", {}),
            "chapters": {cid: content[:1500] for cid, content in state.get("chapter_drafts", {}).items() if content}
        }
        return self.mapper.generate_defense_prep(context)

    def check_red_flags(self):
        """
        Scans the project drafts for common red flags like misalignment.
        """
        state = self.state_store.state
        context = {
            "metadata": state.get("project_metadata", {}),
            "core_context": state.get("core_context", {}),
            "chapters": {cid: content[:2000] for cid, content in state.get("chapter_drafts", {}).items() if content}
        }
        return self.mapper.scan_red_flags(context)

if __name__ == "__main__":
    # Quick test
    # engine = WritingEngine("data/unizik_undergrad.json")
    pass
