import os
import json

class LLMMapper:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model

    def map_notes_to_section(self, notes, section_title, guidance):
        """
        Uses an LLM to extract relevant information from notes for a specific section.
        """
        prompt = f"""
You are an expert academic advisor. Your task is to extract information from a student's raw research notes to fill a specific section of a thesis outline.

---
INSTITUTIONAL GUIDANCE for "{section_title}":
{guidance}

---
STUDENT'S RAW NOTES:
{notes}

---
TASK:
1. Identify any content in the notes that belongs in the "{section_title}" section.
2. If relevant content exists, summarize it clearly in bullet points as it should appear in a thesis outline.
3. If no relevant content exists, provide a "GAP ANALYSIS": Explain what information is missing and give 2-3 specific suggestions on what the student should research or write to satisfy the requirements for this section.

Output format:
Either:
- Relevant content found: [Your summary]
Or:
- GAP ANALYSIS: [Your explanation and suggestions]
"""
        
        if not self.api_key:
            # Fallback/Simulator for when no API key is provided
            # In a real scenario, this would call OpenAI/Gemini/etc.
            return self._simulate_llm_response(notes, section_title, guidance)

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful academic assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            return "Error: openai library not installed. Please install it to use real LLM mapping."
        except Exception as e:
            return f"Error during LLM call: {str(e)}"

    def generate_prose(self, notes_content, section_title, guidance, context):
        """
        Uses an LLM to generate full academic prose for a section based on Nigerian university standards.
        """
        prompt = f"""
You are an expert academic writer specialized in Nigerian university thesis standards. 
Your task is to write high-quality, professional academic prose for a specific section of a thesis chapter.

---
GENERAL WRITING STANDARDS:
- **Perspective**: Use Third-Person Perspective (e.g., "The researcher," "The study," "The findings"). Never use "I," "We," "My," or "Our."
- **Tone**: Maintain a formal, objective, and scholarly voice. Avoid contractions, colloquialisms, and informal language.
- **Tense Usage**:
    - For Chapter 1 (Introduction) and Chapter 3 (Methodology) in a *proposal* context, use future tense (e.g., "The study will employ...").
    - For a *final thesis*, use past tense for the research process (e.g., "The data were collected...") and present tense for results/facts that remain true (e.g., "The data indicates...").
    - Use the most appropriate tense based on this context: {context}.
- **Citations**: Include in-text citations in the format [Author, Year] where appropriate, especially in the Background, Literature Review, and Discussion. Use the student's notes for real citations or suggest placeholders (e.g., [Smith, 2023]) if the notes are missing specific sources.
- **Transitions**: Use logical markers to guide the reader (e.g., "Furthermore," "Moreover," "In the same vein," "Conversely," "Consequently," "It is against this backdrop that...").

---
SECTION-SPECIFIC STANDARDS:
- **Background to the Study (1.1)**: Follow the **Inverted Pyramid** approach:
    1. Global Level (International perspective).
    2. Regional Level (African/West African context).
    3. National Level (Nigerian situation).
    4. Local/Institutional Level (Specific area/organization being studied).
- **Statement of the Problem (1.2)**: Clearly identify the "gap" using this structure:
    1. The Ideal (how things should be).
    2. The Reality (the current negative situation/problem).
    3. The Consequence (what happens if the problem persists).
- **Research Methodology (Chapter 3)**: Explain the **rationale** for every choice. Do not just list methods; justify why they are appropriate for this specific study.
- **Discussion of Findings (Chapter 5)**: Compare results with previous studies (e.g., "This finding is consistent with Abiola (2020)...").

---
CITATION DENSITY EXPECTATIONS:
- Chapter 1: Moderate (1-2 citations per paragraph in Background).
- Chapter 2: High (most paragraphs should have citations).
- Chapter 3: Low (mostly for specific designs/formulas).
- Chapter 4: Very Low (focus on own findings).
- Chapter 5: High (comparison with literature).

---
INPUT DATA:
- **Section Title**: {section_title}
- **Context**: {context}
- **Institutional Guidance**: {guidance}
- **Student's Raw Notes**: {notes_content}

---
TASK:
1. Write 2-3 paragraphs of formal academic prose for this section.
2. Incorporate the student's raw notes while expanding them into logical, flowing text.
3. Adhere strictly to the general and section-specific standards provided above.
4. If the student's notes are insufficient, provide a professional draft using general academic knowledge, but clearly highlight areas where the student must provide more local data.
5. Ensure the prose is cohesive and meets the expected citation density for this chapter.

Output the prose directly. No preamble.
"""
        if not self.api_key:
             return self._simulate_prose_response(section_title, guidance)

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional academic writer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during prose generation: {str(e)}"

    def generate_defense_prep(self, project_context):
        """
        Uses an LLM to generate suggested responses to typical defense questions based on project context.
        """
        prompt = f"""
        You are a senior academic supervisor at a top Nigerian university.
        You are preparing a student for their final thesis defense.
        
        ---
        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}
        
        ---
        TASK:
        Based on the provided project content, generate suggested responses to these typical defense questions:
        1. "What motivated you to embark on this research?"
        2. "In simple terms, what specific problem is your study trying to solve?"
        3. "Who will benefit from the findings of this research and how?"
        4. "What gap in existing literature did you identify?"
        5. "Why did you choose your specific research design (e.g., Descriptive Survey, Experimental)?"
        6. "Summarize your major findings in less than 2 minutes."
        7. "What is the original contribution of your study to the field?"
        
        ---
        GUIDELINES FOR ANSWERS:
        - Use the specific data from the project context (RQs, Objectives, Methodology, Findings).
        - Keep answers concise, confident, and academic.
        - If a certain chapter hasn't been drafted yet, suggest a general professional way to frame the answer while noting what's missing.
        
        Output the questions and suggested answers as a list.
        """
        if not self.api_key:
             return self._simulate_defense_prep_response()

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior academic supervisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during defense prep generation: {str(e)}"

    def scan_red_flags(self, project_context):
        """
        Uses an LLM to scan the project for "Red Flags" like misalignment.
        """
        prompt = f"""
        You are an eagle-eyed academic external examiner. 
        Your job is to find inconsistencies and "red flags" in a student's thesis project before their defense.
        
        ---
        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}
        
        ---
        RED FLAGS TO CHECK FOR:
        1. **Misalignment**: Do the Title, Statement of the Problem, Research Questions, and Findings all align? (e.g., If RQ1 asks about productivity, is there a finding about productivity?)
        2. **SMART Objectives**: Are the research objectives Specific, Measurable, Achievable, Relevant, and Time-bound?
        3. **Methodological Consistency**: Is the sample size justified? Is the design appropriate for the RQs?
        4. **Logical Flow**: Does Chapter 5 actually answer the questions raised in Chapter 1?
        5. **Nigerian Academic Tone**: Does it follow the strict third-person formal tone required in Nigeria?
        
        ---
        TASK:
        1. Identify any red flags found.
        2. Provide specific, corrective advice for each flag.
        3. If the work is highly consistent, congratulate the student on their "Golden Thread."
        
        Format your response with "🚩 RED FLAG FOUND" or "✅ CONSISTENCY CHECK PASSED".
        """
        if not self.api_key:
             return self._simulate_red_flags_response()

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an external academic examiner."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during red flag scan: {str(e)}"

    def extract_core_context(self, chapter_1_text):
        """
        Uses an LLM to extract Research Questions and Objectives from Chapter 1.
        """
        prompt = f"""
        Extract the primary Research Questions and Objectives from the following text of Chapter 1 of a thesis.
        Format the output as a valid JSON object with keys "research_questions" (list of strings) and "objectives" (list of strings).
        
        TEXT:
        {chapter_1_text}
        
        Return ONLY the JSON object.
        """
        if not self.api_key:
             return {
                "research_questions": ["How does remote work affect productivity?", "What is the role of digital tools?"],
                "objectives": ["To evaluate productivity levels.", "To identify key digital tools."]
            }

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an academic context extractor. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            # Fallback
            return {
                "error": f"Extraction failed: {str(e)}",
                "research_questions": [],
                "objectives": []
            }

    def _simulate_defense_prep_response(self):
        return """
1. **What motivated you to embark on this research?**
*Suggested Response:* "The motivation for this study stems from the observable shift in global work patterns and the need to empirically assess how these changes impact organizational efficiency in the Nigerian tech sector..."

2. **In simple terms, what specific problem is your study trying to solve?**
*Suggested Response:* "The study addresses the critical gap in productivity measurement among remote-first companies in Lagos, where infrastructure challenges often conflict with work-from-home models..."

3. **Who will benefit from the findings of this research and how?**
*Suggested Response:* "The findings will primarily benefit HR managers in policy formulation and tech employees in optimizing their home-work environments..."
"""

    def _simulate_red_flags_response(self):
        return """
✅ **CONSISTENCY CHECK PASSED**: The Title and Research Questions show strong alignment.

🚩 **RED FLAG FOUND**: Sample Size Justification
*Advice:* You mentioned a population of workers but didn't explicitly cite the Taro Yamane formula for sample size determination, which is standard in many Nigerian social science departments.

🚩 **RED FLAG FOUND**: SMART Objectives
*Advice:* Objective 2 ("To identify digital tools") is slightly vague. Consider refining it to: "To identify the specific digital collaboration tools that significantly correlate with high performance in remote teams."
"""

    def _simulate_prose_response(self, section_title, guidance):
        return f"[SIMULATED ACADEMIC PROSE for {section_title}]\n\nGlobally, the phenomenon of {section_title} has garnered significant attention from scholars and practitioners alike. In the African context, and specifically within Nigeria, the implications of this topic are profound. As specified in the institutional guidelines ({guidance[:30]}...), it is imperative to establish a rigorous framework for investigation.\n\nFurthermore, the researcher observes that despite existing interventions, several challenges remain unresolved. Consequently, this study adopts a formal approach to analyze the variables involved, ensuring that the findings contribute meaningfully to the existing body of knowledge in the field. This study is conducted against the backdrop of increasing calls for empirical evidence to drive policy and practice."

    def _simulate_llm_response(self, notes, section_title, guidance):
        """
        A sophisticated simulator that uses basic keyword matching to mimic LLM behavior
        for demo purposes when an API key is missing.
        """
        notes_lower = notes.lower()
        section_lower = section_title.lower()
        
        # Simple keyword-based logic to simulate "understanding"
        keywords = {
            "background": ["context", "history", "since", "became", "et al"],
            "problem": ["issue", "challenge", "problem", "think", "vs"],
            "objective": ["goal", "aim", "measure", "identify"],
            "purpose": ["goal", "aim", "measure", "identify"],
            "conceptual": ["theory", "concept", "framework", "sdt"],
            "theoretical": ["theory", "concept", "framework", "sdt"],
            "methodology": ["research", "design", "survey", "sampling", "population"],
            "design": ["research", "design", "quantitative", "qualitative"],
            "population": ["workers", "people", "group", "participants"],
            "sampling": ["purposive", "random", "technique"]
        }
        
        found = False
        for key, words in keywords.items():
            if key in section_lower:
                if any(word in notes_lower for word in words):
                    found = True
                    break
        
        if found:
            return f"[SIMULATED LLM EXTRACTION for {section_title}]\n- Extracted relevant points based on notes analysis.\n- (Connects to guidance: {guidance[:50]}...)"
        else:
            return f"GAP ANALYSIS: No direct mention of '{section_title}' details found in notes. \nSuggestion: Elaborate on how your notes connect to the {section_title} requirements specified in the institutional guidelines."
