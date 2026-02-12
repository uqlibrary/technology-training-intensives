import os
from os.path import join, basename, splitext
import pymupdf

qgis_pdfs = [
    join(p, f) for p, _, fs in os.walk("gallery/QGIS") for f in fs if f.endswith(".pdf")
]

with open("_processing/qgis_project_template.qmd") as f:
    template = f.read()

for pdf in qgis_pdfs:
    qmd = pdf.replace(".pdf", ".qmd").replace(" ", "_")

    filename = basename(pdf)

    # Create thumbnail from first page
    with pymupdf.open(pdf) as open_pdf:
        # Ensure at least one page in pdf
        if open_pdf.page_count == 0:
            img_path = None
        else:
            # Convert first page to png (svg?)
            first_page = open_pdf[0]
            pix = first_page.get_pixmap()
            img_path = qmd.replace(".qmd", ".png")

            pix.save(img_path)

    ########### THE FOLLOWING CODE EXTRACTS THE FIRST IMAGE ###########
    # UNFORUTATELY IT DOES NOT INCLUDE ANY VECTOR GRAPHICS ON TOP

    # page = open_pdf.load_page(0)
    # input(page.get_displaylist())
    # input("END OF DEBUG")
    # # Loop over all 'pages' to extract first image
    # for i in range(0, open_pdf.page_count):
    #     if len(imgs := open_pdf.get_page_images(i)) == 0:
    #         continue

    #     xref = imgs[-1][0]
    #     img = open_pdf.extract_image(xref)
    #     img_path = qmd.replace(".qmd", f".{img['ext']}")
    #     with open(img_path, "wb") as f:
    #         f.write(img["image"])

    # else:
    #     img_path = None
    ###################################################################

    # Extract metadata (title and author)
    # Filenames are in the following format: title-author.pdf
    if filename.count("-") == 1:
        title, author = splitext(filename)[0].replace("_", " ").split("-")
        author = author.title()
    else:
        title = splitext(filename)[0]
        author = None

    if " " in title or title.islower() or title.isupper():
        title = title.title()

    # Inject metadata into YAML header of .qmd
    replacements = {
        "()": f"({filename})",
        "title:": f"title: {title}",
        "author:": "" if not author else f"author: {author}",
        "image:": "" if not img_path else f"image: {basename(img_path)}",
    }
    input(replacements)

    for key in replacements.keys():
        template = template.replace(key, replacements[key])

    # Write .qmd files to disk
    with open(qmd, "w") as f:
        f.write(template)
