import os
import sys
# Path to the shared engine
sys.path.append('/home/team/shared/engine')

# Ensure we are using the venv
# Note: In this environment, I should run with the venv python directly.

from pdf_export import export_outline_to_pdf

templates_dir = '/home/team/shared/data/templates'
samples_dir = '/home/team/shared/samples'

tasks = [
    {
        "name": "UNIZIK",
        "json": os.path.join(templates_dir, "unizik_undergrad.json"),
        "md": os.path.join(samples_dir, "unizik_outline.md"),
        "pdf": os.path.join(samples_dir, "unizik_outline.pdf")
    },
    {
        "name": "UNILAG",
        "json": os.path.join(templates_dir, "unilag_undergrad.json"),
        "md": os.path.join(samples_dir, "unilag_scaffolded_outline.md"),
        "pdf": os.path.join(samples_dir, "unilag_scaffolded_outline.pdf")
    }
]

for task in tasks:
    print(f"Exporting {task['name']} to PDF...")
    if os.path.exists(task['json']) and os.path.exists(task['md']):
        export_outline_to_pdf(task['json'], task['md'], task['pdf'])
        print(f"Successfully created {task['pdf']}")
    else:
        print(f"Skipping {task['name']} - missing files.")
