from datetime import datetime
import os
from os.path import dirname as d
from os.path import basename as b
from os.path import join as j
import re
import shutil
from subprocess import run
import sys
import warnings
import matplotlib as mpl

MONTHS = {
    "Python": {"25Summer": "Jan", "25Winter": "Jul", "26Summer": "Feb"},
    "R": {"25Summer": "Jan", "25Winter": "Jul", "26Summer": "Jan"},
    "QGIS": {"25Summer": "Jan", "25Winter": "Jul", "26Summer": "Feb"},
}
# ANSI colour escape sequences (for console colours)
O = "\033[0m"  # Default (reset)
R = "\033[31m"  # Red
G = "\033[32m"  # Green
Y = "\033[33m"  # Yellow
B = "\033[34m"  # Blue


# Source - https://stackoverflow.com/a
# Posted by Alexander C, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-24, License - CC BY-SA 4.0
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def run_py(source):
    with HiddenPrints():
        try:
            exec(source)
        except Exception as e:
            return e
        else:
            return None


def create_backup(qmd: str) -> None:
    backup_dir = j(d(qmd), "original_source")
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)
        shutil.copy2(qmd, j(backup_dir, ""))
    elif not os.path.exists(j(backup_dir, b(qmd))):
        shutil.copy2(qmd, j(backup_dir, ""))


def run_checker(dev: bool = False) -> None:
    if not os.path.exists("_quarto.yml"):
        raise EnvironmentError("Not in quarto project dir.")

    if sys.prefix == sys.base_prefix:
        raise EnvironmentError(
            "Not in a virtual environment, required for testing Python imports.\n\nHave you activated? Run source .venv/bin/activate"
        )

    if not os.path.exists(j(d(sys.prefix), "_quarto.yml")):
        raise EnvironmentError("Not in the correct virtual environment.")

    warnings.filterwarnings("ignore")
    mpl.use("Agg")

    old_state_files = {j(path, f) for path, _, fs in os.walk("./") for f in fs}

    with open("_processing/project_ok.log") as f:
        ok_projects = [ln.strip().split(",") for ln in f.readlines()]

    qmds = [
        j(path, file)
        for path, _, files in os.walk("gallery")
        for file in files
        if file.endswith(".qmd")
        and (
            b(d(d(d(path)))) == "gallery"
            or (b(d(d(d(d(path))))) == "gallery" and ".exclude" in path)
        )
    ]

    e_log = []
    left_unchecked = []

    print("Checking all projects in gallery/ for errors.")
    for qmd in qmds:
        last_checks = [
            datetime.strptime(f[1], "%Y-%m-%d %H:%M:%S")
            for f in ok_projects
            if f[0] == qmd
        ]

        if last_checks != [] and datetime.fromtimestamp(os.stat(qmd).st_mtime) < max(
            last_checks
        ):
            left_unchecked.append(qmd)
            continue

        create_backup(qmd)

        print(f"{Y}TESTING:{O}", qmd)

        # I/O
        with open(qmd) as f:
            content = f.read()

        if ".exclude" in qmd:
            lang = b(d(d(d(d(qmd)))))
            iteration = b(d(d(d(qmd))))
        else:
            lang = b(d(d(d(qmd))))
            iteration = b(d(d(qmd)))

        #### YAML ####
        try:
            yaml_start = content.index("---")
            yaml_end = content.index("---", yaml_start + 1)
        except ValueError:
            message = "No YAML"
            e_log.append((qmd, message))
            print(R, "\tFAILED:", O, message)
            continue

        yaml = content[:yaml_end]
        body = content[yaml_end:]

        # Spaces in YAML
        first_yaml_ln_i = content.index("\n", yaml_start) + 1
        first_yaml_arg_i = content.index(
            content[first_yaml_ln_i:].lstrip()[0], first_yaml_ln_i
        )
        spaces = content[first_yaml_ln_i:first_yaml_arg_i]

        if spaces.count(" ") != len(spaces):
            raise ValueError(f"Cannot determine spaces in {qmd}.")

        # Fix dates
        date = MONTHS[lang][iteration] + "-" + iteration[:2]

        if "Date: " in yaml:
            yaml = yaml.replace("Date: ", "date: ")

        if "date: " not in yaml:
            yaml += f"{spaces}date: {date}\n"
        elif "today" in yaml:
            yaml = yaml.replace("today", date)

        # Find all data paths
        # TODO: Go through a bunch? xlsx, xls, png, jpg...? json, geojson etc. for QGIS?
        data_paths = set()
        png_paths = set()

        for quote in ('"', "'"):
            i = body.find(f".csv{quote}")

            while i != -1:
                data_path_start = body.rfind(quote, 0, i) + 1
                data_path_end = body.find(quote, i)

                data_paths.add(body[data_path_start:data_path_end])

                i = body.find(f".csv{quote}", data_path_end)

            i = body.find(f".png{quote}")

            while i != -1:
                png_path_start = body.rfind(quote, 0, i) + 1
                png_path_end = body.find(quote, i)

                png_paths.add(body[png_path_start:png_path_end])

                i = body.find(f".png{quote}", png_path_end)

        # Add categories
        data_files = '", "data: '.join(
            [
                os.path.basename(data)
                for data in data_paths
                if os.path.basename(data) in os.listdir("data")
            ]
        )

        if data_files != "":
            data_files = ', "data: ' + data_files + '"'

        categories = f"{spaces}categories: [{lang}, {iteration}{data_files}]\n"

        if categories in yaml:
            pass
        elif "categories: " in yaml:
            i_cat = yaml.index("categories: ")
            cat_ln_start = yaml.rindex("\n", 0, i_cat) + 1
            cat_ln_end = yaml.index("\n", i_cat) + 1
            yaml = yaml[:cat_ln_start] + categories + yaml[cat_ln_end:]
        else:
            yaml += categories

        # Check thumbnail
        if "image: " in yaml:
            i_image = yaml.index("image: ")

            image_file = yaml[
                i_image + len("image: ") : yaml.index("\n", i_image)
            ].strip()

            if os.path.exists(j(d(qmd), image_file)):
                yaml = yaml.replace(image_file, j(d(qmd), image_file))
            elif (
                not os.path.exists(image_file)
                and "#" not in yaml[yaml.rindex("\n", 0, i_image) : i_image]
            ):
                yaml = yaml.replace("image: ", "#image: ")

        #### Body ####

        # Check and fix all data paths
        for path in data_paths:
            if os.path.exists(path):
                continue

            if os.path.exists(new_path := j(d(qmd), path)):
                body = body.replace(path, new_path)
                print(G, "\tFIXED:", O, path + " -> " + new_path)
            elif os.path.exists(new_path := path.replace("/.exclude", "")):
                body = body.replace(path, new_path)
                print(G, "\tFIXED:", O, path + " -> " + new_path)
            elif os.path.exists(new_path := j("data", b(path))):
                body = body.replace(path, new_path)
                print(G, "\tFIXED:", O, path + " -> " + new_path)
            else:
                message = f"Cannot fix {path}"
                e_log.append((qmd, message))
                print(R, "\tFAILED:", O, message)

        for path in png_paths:
            if os.path.exists(path):
                continue

            if os.path.exists(new_path := j(d(qmd), path)):
                body = body.replace(path, new_path)
                print(G, "\tFIXED:", O, path + " -> " + new_path)
            elif os.path.exists(new_path := path.replace("/.exclude", "")):
                body = body.replace(path, new_path)
                print(G, "\tFIXED:", O, path + " -> " + new_path)
            elif os.path.exists(new_path := j("data", b(path))):
                body = body.replace(path, new_path)
                print(G, "\tFIXED:", O, path + " -> " + new_path)
            else:
                message = f"Cannot fix {path}"
                e_log.append((qmd, message))
                print(R, "\tFAILED:", O, message)

        # Check and fix all pngs?

        # Regex: ^[^\n\r\S]*?```\{(.*?)\}\s*\n(.*?)^[^\n\r\S]*?```
        # Captures all executable code blocks.
        # ^             Start of line
        # [^\n\r\S]*?   Zero or more whitespace (not newline, carriage return or non-whitespace), lazy
        # ```\{         ```{
        # (.*?)         Zero or more characters, lazy. Brackets make this a capturing group (chunk options incl lang)
        # \}            }
        # \s*?\n         Zero or more whitespace, lazy, then a newline
        # (.*?)         Zero or more characters, lazy. Brackets make this a capturing group (the code)
        # ^             Start of line
        # [^\n\r\S]*?   Zero or more whitespace (not newline, carriage return or non-whitespace), lazy
        # ```           ```

        chunks = re.findall(
            r"^[^\n\r\S]*?```[^\n\r\S]*?\{(.*?)\}\s*\n(.*?)^[^\n\r\S]*?```",
            body,
            flags=re.M | re.S,
        )

        py_chunks = []
        r_chunks = []

        for ch_options, ch_code in chunks:
            if re.search(r"^\s*#\|\s*eval:\s*false", ch_code, re.M):
                continue

            clean_ops = [
                op.strip().lower() for op in re.split(r"[,\s]", ch_options.strip())
            ]

            if "r" in clean_ops:
                r_chunks += [ch_code]
            elif "python" in clean_ops:
                py_chunks += [ch_code]
            else:
                message = f"Cannot execute code chunk with option(s) '{ch_options}'"
                e_log.append((qmd, message))
                print(R, "\tFAILED:", O, message)

        r_code = "\n".join(r_chunks)
        py_code = "\n".join(py_chunks)

        if r_code != "":
            Rout = run("R -s -e".split() + [r_code], capture_output=True)

            if Rout.returncode != 0:
                message = Rout.stderr
                e_log.append((qmd, message.decode()))
                print(R, "\tFAILED:", O, message)

        if "plotly" in py_code:
            py_code = (
                "import plotly.io as pio\npio.renderers.default = None\n" + py_code
            )

        if py_code != "":
            e = run_py(py_code)
            if e is not None:
                message = e
                e_log.append((qmd, message))
                print(R, "\tFAILED:", O, message)

        # Overwrite with patches
        with open(qmd, "w") as f:
            f.write(yaml + body)

        #### For render ####
        if qmd in [error[0] for error in e_log]:

            # Move to .exclude if not already in it
            if ".exclude" not in qmd:
                if not os.path.isdir(exclude_dir := j(d(d(qmd)), ".exclude")):
                    os.mkdir(exclude_dir)

                shutil.move(d(qmd), exclude_dir)

            print(R, "\tFAILS TO RENDER", O)

        else:
            if ".exclude" in qmd:
                shutil.move(d(qmd), d(d(d(qmd))))

            print(G, "\tSUCCESS", O)

    print("The following files fail to render and now live in .exclude/:")
    for file in {error[0] for error in e_log}:
        print(R, file, O)

    print("\nWriting to logs and updating quarto inputs.")
    with open("_processing/project_errors.log", "w") as f:
        f.write("\n".join(str(item) for item in e_log))

    with open("_processing/project_ok.log", "w") as f:
        f.write(
            "\n".join(
                [
                    ",".join((path, time))
                    for path, time in ok_projects
                    if path in left_unchecked
                ]
                + [
                    qmd + "," + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for qmd in qmds
                    if qmd not in [e[0] for e in e_log] and qmd not in left_unchecked
                ]
            )
        )

    # Compare state before and after to remove any created files
    new_state_files = {j(path, f) for path, _, fs in os.walk("./") for f in fs}
    all_new_files = new_state_files - old_state_files

    backups = {path for path in all_new_files if "original_source" in path}
    excludes = {file for file in all_new_files if ".exclude" in file}
    from_excludes = {
        file.replace("/.exclude", "")
        for file in old_state_files
        if ".exclude" in file and file.replace("/.exclude", "") in all_new_files
    }
    new_files = (
        (all_new_files - backups)
        & (all_new_files - excludes)
        & (all_new_files - from_excludes)
    )

    if not all_new_files:
        print("\nNo new files were created during project testing.")
    else:
        if backups:
            print("\nProject testing has created backups of original source files:")

            for file in backups:
                print(B, file, O)

            if dev and input("\nWould you like to keep these? [y]/n: ").lower() == "n":
                for file in backups:
                    os.remove(file)

        if excludes:
            print("\nProject testing has moved some projects to a .excludes/ dir:")
            for file in excludes:
                print(R, file, O)
            if dev and input("\nWould you like to keep these? [y]/n: ").lower() == "n":
                for file in excludes:
                    os.remove(file)

        if from_excludes:
            print("\nProject testing has moved some projects from a .excludes/ dir:")
            for file in from_excludes:
                print(G, file, O)
            if dev and input("\nWould you like to keep these? [y]/n: ").lower() == "n":
                for file in from_excludes:
                    os.remove(file)

        if new_files:
            print("\nProject testing has created new files.")
            for file in new_files:
                print(B, file, O)
            if (
                not dev
                or input("\nWould you like to keep these? y/[n]: ").lower() != "y"
            ):
                for file in new_files:
                    os.remove(file)

    empty_dirs = {
        j(path, f)
        for path, fs, _ in os.walk("./")
        for f in fs
        if os.listdir(j(path, f)) == []
    }

    if empty_dirs:
        print("This repo has the following empty dirs:")
        for path in empty_dirs:
            print(B, path, O)
        if dev and input("\nWould you like to keep these? [y]/n: ").lower() == "n":
            for path in empty_dirs:
                os.rmdir(path)


if __name__ == "__main__":
    run_checker(dev=True)
