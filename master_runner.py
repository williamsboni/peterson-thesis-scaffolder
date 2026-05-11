import os
import sys
import json
import argparse

# Add engine path to sys.path
sys.path.append('/home/team/shared/engine')

from scaffold_engine import ScaffoldingEngine
from llm_utils import LLMMapper
from pdf_export import export_outline_to_pdf

def main():
    parser = argparse.ArgumentParser(description="Peterson Enterprises: Automated Thesis Structuring")
    parser.add_argument("--institution", required=True, choices=["unizik", "unilag", "unn", "oau"], help="Target university")
    parser.add_argument("--notes", required=True, help="Path to your raw research notes text file")
    parser.add_argument("--output_dir", default="/home/team/shared/output", help="Directory to save results")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        
    template_map = {
        "unizik": "/home/team/shared/data/templates/unizik_undergrad.json",
        "unilag": "/home/team/shared/data/templates/unilag_undergrad.json",
        "unn": "/home/team/shared/data/templates/unn_undergrad.json",
        "oau": "/home/team/shared/data/templates/oau_undergrad.json"
    }
    
    template_path = template_map[args.institution]
    
    print(f"--- Peterson Enterprises Scaffolding Engine ---")
    print(f"Targeting: {args.institution.upper()}")
    
    # 1. Initialize Engine
    engine = ScaffoldingEngine(template_path)
    mapper = LLMMapper() # Will use simulator if no API key
    
    # 2. Load Notes
    with open(args.notes, 'r') as f:
        notes_content = f.read()
    
    # 3. Generate Markdown Outline
    print("Step 1: Mapping notes and performing Gap Analysis...")
    outline_md = engine.generate_outline(notes_content, mapper_func=mapper.map_notes_to_section)
    
    md_output_path = os.path.join(args.output_dir, f"{args.institution}_outline.md")
    engine.save_outline(outline_md, md_output_path)
    print(f"Markdown outline generated at: {md_output_path}")
    
    # 4. Export to PDF
    print("Step 2: Exporting to PDF with institutional formatting...")
    pdf_output_path = os.path.join(args.output_dir, f"{args.institution}_outline.pdf")
    try:
        export_outline_to_pdf(template_path, md_output_path, pdf_output_path)
        print(f"Formatted PDF generated at: {pdf_output_path}")
    except Exception as e:
        print(f"PDF Export failed (make sure fpdf2 is installed): {e}")

    print("\n--- Process Complete ---")
    print("Check the output directory for your structured thesis scaffold.")

if __name__ == "__main__":
    main()
