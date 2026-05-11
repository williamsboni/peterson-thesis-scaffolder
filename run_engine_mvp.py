import sys
import os
sys.path.append('/home/team/shared/engine/')
from scaffold_engine import ScaffoldingEngine

def mock_llm_mapper(notes, section_title):
    """
    Simulates what an LLM would do: extract relevant parts of notes for a section.
    """
    if "Background" in section_title:
        return "- Remote work has become more common since 2020.\n- Bloom et al. (2015) work from home study."
    elif "Problem" in section_title:
        return "- Managers think productivity is down vs employees say they are happier.\n- Identifying if people are working more or differently."
    elif "Objectives" in section_title:
        return "- Measure productivity levels in remote vs office settings.\n- Identify factors that improve remote productivity."
    elif "Conceptual" in section_title:
        return "- Self-Determination Theory (SDT) and autonomy."
    elif "Empirical" in section_title:
        return "- Bloom et al. (2015) research on work from home."
    elif "Design" in section_title:
        return "- Quantitative research design."
    elif "Population" in section_title:
        return "- Surveys of 100 tech workers in Lagos.\n- Purposive sampling."
    else:
        return "[No direct mention in notes. Recommendation: Research further on " + section_title + "]"

template_path = '/home/team/shared/data/templates/generic_standard.json'
notes_path = '/home/team/shared/samples/student_notes.txt'
output_path = '/home/team/shared/samples/output_outline.md'

engine = ScaffoldingEngine(template_path)

with open(notes_path, 'r') as f:
    notes = f.read()

# Run with mock mapper to simulate LLM capability
outline = engine.generate_outline(notes, mapper_func=mock_llm_mapper)
engine.save_outline(outline, output_path)

print(f"MVP Engine Run Complete. Output saved to {output_path}")
