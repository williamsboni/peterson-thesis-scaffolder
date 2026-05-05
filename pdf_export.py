from fpdf import FPDF
import json
import os

class PDFExportEngine(FPDF):
    def __init__(self, template):
        super().__init__()
        self.template = template
        self.apply_formatting()

    def apply_formatting(self):
        # Default values
        font_family = "Times"
        font_size = 12
        line_spacing = 1.5
        margins = {"left": 25.4, "right": 25.4, "top": 25.4, "bottom": 25.4} # 1 inch in mm

        # Extract formatting from template if available
        # In a real system, we'd have structured formatting data.
        # Here we look at the 'formatting' section guidance notes.
        for section in self.template.get('structure', []):
            if section.get('id') == 'formatting':
                for sub in section.get('subsections', []):
                    notes = sub.get('guidance_notes', '').lower()
                    if 'times new roman' in notes:
                        font_family = "Times"
                    if '12pt' in notes:
                        font_size = 12
                    if '2.0' in notes or 'double' in notes:
                        line_spacing = 2.0
                    if '1.5 inches' in notes and 'left' in notes:
                        margins['left'] = 38.1 # 1.5 inches in mm
                    if '1.0 inch' in notes:
                        if 'right' in notes: margins['right'] = 25.4
                        if 'top' in notes: margins['top'] = 25.4
                        if 'bottom' in notes: margins['bottom'] = 25.4
                    if '40mm' in notes and 'left' in notes:
                        margins['left'] = 40

        self.set_font(font_family, size=font_size)
        self.set_left_margin(margins['left'])
        self.set_right_margin(margins['right'])
        self.set_top_margin(margins['top'])
        self.set_auto_page_break(auto=True, margin=margins['bottom'])
        self.line_spacing_factor = line_spacing

    def header(self):
        pass # Optional: Add institution name in header

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section(self, title, content, level=1):
        if level == 1:
            self.set_font("Times", "B", 16)
            self.ln(10)
            self.cell(0, 10, title, ln=True)
            self.ln(5)
        elif level == 2:
            self.set_font("Times", "B", 14)
            self.ln(5)
            self.cell(0, 10, title, ln=True)
            self.ln(2)
        else:
            self.set_font("Times", "B", 12)
            self.cell(0, 10, title, ln=True)

        self.set_font("Times", "", 12)
        # Handle multi-line content with spacing
        self.multi_cell(0, 6 * self.line_spacing_factor, content)
        self.ln(2)

def export_outline_to_pdf(json_template_path, markdown_outline_path, output_pdf_path):
    with open(json_template_path, 'r') as f:
        template = json.load(f)
    
    with open(markdown_outline_path, 'r') as f:
        md_content = f.read()

    pdf = PDFExportEngine(template)
    pdf.add_page()
    
    # Very basic MD to PDF parsing for the demo
    lines = md_content.split('\n')
    current_section_title = ""
    current_content = []
    
    pdf.set_font("Times", "B", 20)
    pdf.cell(0, 20, template['metadata']['institution'], ln=True, align='C')
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 10, f"Program Level: {template['metadata']['program_level']}", ln=True, align='C')
    pdf.ln(10)

    for line in lines:
        if line.startswith('## '):
            if current_section_title:
                pdf.add_section(current_section_title, "\n".join(current_content), level=1)
            current_section_title = line[3:].strip()
            current_content = []
        elif line.startswith('### '):
            if current_section_title:
                pdf.add_section(current_section_title, "\n".join(current_content), level=1)
                current_section_title = ""
            # We treat ### as level 2
            pdf.add_section(line[4:].strip(), "", level=2)
        elif line.strip() == "" or line.startswith('# '):
            continue
        else:
            current_content.append(line)
            
    if current_section_title:
        pdf.add_section(current_section_title, "\n".join(current_content), level=1)

    pdf.output(output_pdf_path)
    return output_pdf_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python pdf_export.py <template_json> <markdown_file> <output_pdf>")
        sys.exit(1)
    
    export_outline_to_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"Exported to {sys.argv[3]}")
