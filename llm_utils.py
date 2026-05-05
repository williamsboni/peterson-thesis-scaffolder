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
