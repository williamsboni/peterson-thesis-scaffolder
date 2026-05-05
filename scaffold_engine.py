import json
import argparse
import os
from llm_utils import LLMMapper

class ScaffoldingEngine:
    def __init__(self, template_path, mapper=None):
        with open(template_path, 'r') as f:
            self.template = json.load(f)
        self.mapper = mapper or LLMMapper()

    def generate_outline(self, notes_content, mapper_func=None):
        """
        Generates a thesis outline. 
        Priority: mapper_func > self.mapper.map_notes_to_section > default string
        """
        outline = f"# Thesis Outline: {self.template['metadata']['institution']}\n\n"
        outline += f"**Program Level:** {self.template['metadata']['program_level']}\n"
        outline += f"**Faculty:** {self.template['metadata']['faculty']}\n\n"
        
        for section in self.template['structure']:
            outline += f"## {section['title']}\n"
            outline += f"*{section['description']}*\n\n"
            
            if 'subsections' in section:
                for sub in section['subsections']:
                    outline += f"### {sub['id']} {sub['title']}\n"
                    guidance = sub.get('guidance_notes', 'No specific guidance provided.')
                    outline += f"**Guidance:** {guidance}\n\n"
                    
                    if mapper_func:
                        mapping = mapper_func(notes_content, sub['title'])
                    elif self.mapper:
                        mapping = self.mapper.map_notes_to_section(notes_content, sub['title'], guidance)
                    else:
                        mapping = "[READY FOR LLM MAPPING]"
                        
                    outline += f"**Draft Content/Notes:**\n{mapping}\n\n"
            
        return outline

    def save_outline(self, outline, output_path):
        with open(output_path, 'w') as f:
            f.write(outline)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffolding Engine MVP")
    parser.add_argument("--notes", required=True, help="Path to student notes text file")
    parser.add_argument("--template", required=True, help="Path to institutional template JSON")
    parser.add_argument("--output", required=True, help="Path to save the generated Markdown outline")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.notes):
        print(f"Error: Notes file not found at {args.notes}")
        exit(1)
        
    if not os.path.exists(args.template):
        print(f"Error: Template file not found at {args.template}")
        exit(1)
        
    engine = ScaffoldingEngine(args.template)
    
    with open(args.notes, 'r') as f:
        notes = f.read()
        
    outline = engine.generate_outline(notes)
    engine.save_outline(outline, args.output)
    print(f"Successfully generated outline at {args.output}")
