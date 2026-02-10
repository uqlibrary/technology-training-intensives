import os
from os.path import join, basename

qgis_pdfs = [
    join(p, f) for p, _, fs in os.walk("gallery/QGIS") for f in fs if f.endswith(".pdf")
]

with open("_processing/qgis_project_template.qmd") as f:
    template = f.read()

for pdf in qgis_pdfs:
    qmd = pdf.replace(".pdf", ".qmd")

    filename = basename(pdf)

    replacements = {
        "()": f"({filename})",
        "title:": f"title: {filename[:filename.index('.')]}",
    }

    for key in replacements.keys():
        template = template.replace(key, replacements[key])

    with open(qmd, "w") as f:
        f.write(template)
