import sys
import os
sys.path.append('/home/team/shared/engine/')
from scaffold_engine import ScaffoldingEngine

def mock_llm_mapper(notes, section_title):
    """
    Simulates what an LLM would do: extract relevant parts of notes for a section.
    Tailored for UNIZIK template structure.
    """
    notes_lower = notes.lower()
    section_lower = section_title.lower()

    if "background" in section_lower:
        return "- Remote work has become more common since 2020.\n- Bloom et al. (2015) work from home study."
    elif "problem" in section_lower:
        return "- Managers think productivity is down vs employees say they are happier.\n- Identifying if people are working more or differently."
    elif "purpose" in section_lower or "objectives" in section_lower:
        return "- Measure productivity levels in remote vs office settings.\n- Identify factors that improve remote productivity."
    elif "conceptual" in section_lower:
        return "- Self-Determination Theory (SDT) and autonomy."
    elif "empirical" in section_lower:
        return "- Bloom et al. (2015) research on work from home."
    elif "design" in section_lower:
        return "- Quantitative research design."
    elif "population" in section_lower:
        return "- Surveys of 100 tech workers in Lagos."
    elif "sample" in section_lower:
        return "- Purposive sampling technique."
    elif "abstract" in section_lower:
        return "[LLM will generate this summary once chapters are drafted.]"
    elif "scope" in section_lower:
        return "- Tech sector workers in Lagos, Nigeria."
    elif "instrument" in section_lower:
        return "- Online questionnaires (implied by 'surveys')."
    else:
        return "[No direct mention in notes. Recommendation: Research further on " + section_title + "]"

template_path = '/home/team/shared/data/templates/unizik_undergrad.json'
notes_path = '/home/team/shared/samples/student_notes.txt'
output_path = '/home/team/shared/samples/unizik_outline.md'

if not os.path.exists(template_path):
    print(f"Error: Template not found at {template_path}")
    sys.exit(1)

engine = ScaffoldingEngine(template_path)

with open(notes_path, 'r') as f:
    notes = f.read()

# Run with mock mapper
outline = engine.generate_outline(notes, mapper_func=mock_llm_mapper)
engine.save_outline(outline, output_path)

print(f"UNIZIK Scaffolding Demo Complete. Output saved to {output_path}")
