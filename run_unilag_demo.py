import sys
import os
sys.path.append('/home/team/shared/engine/')
from scaffold_engine import ScaffoldingEngine
from llm_utils import LLMMapper

# Use the LLMMapper with fallback simulator
mapper = LLMMapper()

template_path = '/home/team/shared/data/templates/unilag_undergrad.json'
notes_path = '/home/team/shared/samples/student_notes.txt'
output_path = '/home/team/shared/samples/unilag_scaffolded_outline.md'

if not os.path.exists(template_path):
    print(f"Error: Template not found at {template_path}")
    sys.exit(1)

engine = ScaffoldingEngine(template_path, mapper=mapper)

with open(notes_path, 'r') as f:
    notes = f.read()

print("Running Scaffolding Engine with UNILAG Template...")
outline = engine.generate_outline(notes)
engine.save_outline(outline, output_path)

print(f"UNILAG Scaffolding Demo Complete. Output saved to {output_path}")
