import os

def py_to_qmd(path):
    with open(path) as f:
        source = f.readlines()


    in_header = False 
    in_py = False

    qmd_source = ""
    
    source.pop(0)

    for line in source:       
        # Check header
        if "---" in line and not in_header:
            in_header = True
            new_line = "---\n"
        elif "---" in line and in_header:
            in_header = False
            new_line = "---\n"
        elif ('"""' in line) or (not in_py and "[markdown]" in line):
            new_line = "\n"
        elif in_header:
            new_line = line.replace("#", "")
        elif in_py and "[markdown]" in line:
            in_py = False
            new_line = "```\n"
        elif "#" in line and "%%" in line:
            if in_py:
                new_line = "```\n\n```{python}\n"
            else:
                in_py = True
                new_line = "```{python}\n"
        else:
            new_line = line
        
        qmd_source += new_line

    if in_py:
        qmd_source += "\n```"
    
    return qmd_source


for root, dirs, files in os.walk("Past_projects"):
    python_files = [file for file in files if ".py" in file]
    
    path = root + "/"

    for py in python_files:
        if "converter" in py:
            continue
        
        with open(path + py[:-3] + ".qmd", "w") as qmd:
            qmd.write(py_to_qmd(path + py))
        
        os.remove(path + py)

