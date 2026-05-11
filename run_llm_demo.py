import sys
import os
sys.path.append('/home/team/shared/engine/')
from scaffold_engine import ScaffoldingEngine
from llm_utils import LLMMapper

# For this demo, we'll use the LLMMapper without an API key to show the fallback/simulator logic,
# which now includes the prompt construction and gap analysis as requested.
# If an OPENAI_API_KEY was present in the environment, it would use the real API.
mapper = LLMMapper()

template_path = '/home/team/shared/data/templates/unizik_undergrad.json'
notes_path = '/home/team/shared/samples/student_notes.txt'
output_path = '/home/team/shared/samples/llm_scaffolded_outline.md'

if not os.path.exists(template_path):
    print(f"Error: Template not found at {template_path}")
    sys.exit(1)

engine = ScaffoldingEngine(template_path, mapper=mapper)

with open(notes_path, 'r') as f:
    notes = f.read()

print("Running Scaffolding Engine with LLM Mapper...")
outline = engine.generate_outline(notes)
engine.save_outline(outline, output_path)

print(f"LLM-Scaffolding Demo Complete. Output saved to {output_path}")
