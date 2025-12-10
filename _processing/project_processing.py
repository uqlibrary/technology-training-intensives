from datetime import datetime as dt
import os
from os.path import dirname as d
from os.path import basename as b
from os.path import join as j
from os.path import relpath as rel
import re
import shutil
from subprocess import run
import sys
import warnings
import matplotlib as mpl

ROOT = os.getcwd()
MONTHS = {
    "Python": {"25Summer": "Jan", "25Winter": "Jul", "26Summer": "Feb"},
    "R": {"25Summer": "Jan", "25Winter": "Jul", "26Summer": "Jan"},
    "QGIS": {"25Summer": "Jan", "25Winter": "Jul", "26Summer": "Feb"},
}
# ANSI colour escape sequences (for console colours)
O = "\033[0m"  # Default (reset)
RED = "\033[31m"  # Red
GRN = "\033[32m"  # Green
YLW = "\033[33m"  # Yellow
BLU = "\033[34m"  # Blue


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


def test_py(qmd: str, source: str, log: list) -> None:
    with HiddenPrints():
        try:
            exec(source)
        except Exception as e:
            log.append((qmd, e))
            print(RED, "\tFAILED:", O, e)


def create_backup(qmd: str) -> None:
    backup_dir = j(d(qmd), "original_source")
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)
        shutil.copy2(qmd, j(backup_dir, ""))
    elif not os.path.exists(j(backup_dir, b(qmd))):
        shutil.copy2(qmd, j(backup_dir, ""))


def yaml_spaces(head: str) -> str:
    first_yaml_ln_i = head.index("\n", head.index("---")) + 1
    first_yaml_arg_i = head.index(head[first_yaml_ln_i:].lstrip()[0], first_yaml_ln_i)
    spaces = head[first_yaml_ln_i:first_yaml_arg_i]

    if spaces.count(" ") != len(spaces):
        raise ValueError(f"Cannot determine spaces in YAML.")

    return spaces


def fix_yaml_date(head: str, spaces: str, lang: str, iteration: str) -> str:
    date = MONTHS[lang][iteration] + "-20" + iteration[:2]
    if "Date:" in head:
        head = head.replace("Date:", "date:")
        print(GRN, "\tFIXED:", O, "Date: -> date")

    # # Fixes previous bad date fromat
    # if (bad_old := MONTHS[lang][iteration] + "-" + iteration[:2]) in head:
    #     head = head.replace(bad_old, date)
    #     print(GRN, "\tFIXED:", O, bad_old, "->", date)

    if "date:" not in head:
        yaml_date = f"{spaces}date: {date}"
        head += yaml_date + "\n"
        print(GRN, "\tFIXED:", O, "N/A ->", yaml_date)

    elif "today" in head:
        head = head.replace("today", date)
        print(GRN, "\tFIXED:", O, "today ->", date)

    return head


def fix_yaml_categories(
    head: str, spaces: str, lang: str, iteration: str, data_paths: set = set()
) -> str:

    # Add categories
    data_files = '", "data: '.join(
        [b(data) for data in data_paths if b(data) in os.listdir("data")]
    )

    if data_files:
        data_files = ', "data: ' + data_files + '"'

    categories = f"{spaces}categories: [{lang}, {iteration}{data_files}]\n"

    if categories in head:
        pass
    elif "categories: " in head:
        i_cat = head.index("categories: ")
        cat_ln_start = head.rindex("\n", 0, i_cat) + 1
        cat_ln_end = head.index("\n", i_cat) + 1
        head = head[:cat_ln_start] + categories + head[cat_ln_end:]
    else:
        head += categories

    return head


def hide_broken_thumbnail(qmd: str, head: str) -> str:
    os.chdir(d(qmd))
    # Check thumbnail
    if "image: " in head:
        i_image = head.index("image: ")
        image_path = head[i_image + len("image: ") : head.index("\n", i_image)].strip()

        if (
            not os.path.exists(image_path)
            and "#" not in head[head.rindex("\n", 0, i_image) : i_image]
        ):
            head = head.replace("image: ", "#image: ")
    os.chdir(ROOT)
    return head


def find_paths(body: str, ext: str) -> set[str]:
    if not ext.startswith("."):
        raise ValueError(f"{ext} is not a valid extension.")

    paths = set()
    for quote in ('"', "'"):
        i = body.find(ext + quote)

        while i != -1:
            data_path_start = body.rfind(quote, 0, i) + 1
            data_path_end = body.find(quote, i)

            paths.add(body[data_path_start:data_path_end])

            i = body.find(ext + quote, data_path_end)

    return paths


def update_links(qmd: str, paths: set[str], body: str) -> str:
    os.chdir(d(qmd))
    for path in paths:
        if os.path.exists(path):
            continue

        # Check if the file exists somewhere in the qmd dir
        matches_in_dir = {
            j(p, f) for p, _, fs in os.walk(".") for f in fs if f == b(path)
        }

        if matches_in_dir and os.path.exists(new_path := matches_in_dir.pop()):
            body = body.replace(path, new_path)
            print(GRN, "\tFIXED:", O, path + " -> " + new_path)

        # If not, check if the file is in the data folder
        elif os.path.exists(new_path := rel(j(ROOT, "data", b(path)))):
            body = body.replace(path, new_path)
            print(GRN, "\tFIXED:", O, path + " -> " + new_path)
        else:
            message = f"Cannot fix {path}"
            print(RED, "\tWARNING:", O, message)

    os.chdir(ROOT)
    return body


def restore_originals() -> None:
    if not os.path.isdir("gallery"):
        raise FileNotFoundError("Where are we? Check your working directory.")

    raise NotImplementedError()


def run_checker(dev: bool = False, clear_log: bool = False) -> None:
    if not os.path.exists("_quarto.yml"):
        raise EnvironmentError("Not in quarto project dir.")

    if os.getenv("IGNORE_VENV_REQ") != "true" and sys.prefix == sys.base_prefix:
        raise EnvironmentError(
            "Not in a virtual environment, required for testing Python imports.\n\nHave you activated? Run source .venv/bin/activate"
        )

    if not os.path.exists(j(d(sys.prefix), "_quarto.yml")):
        raise EnvironmentError("Not in the correct virtual environment.")

    warnings.filterwarnings("ignore")
    mpl.use("Agg")

    old_state_files = {j(path, f) for path, _, fs in os.walk("./") for f in fs}

    if clear_log:
        ok_projects = []
    else:
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
    to_exclude = set()
    to_include = set()

    print("Checking all projects in gallery/ for errors.")
    for qmd in qmds:
        last_checks = [
            dt.strptime(f[1], "%Y-%m-%d %H:%M:%S") for f in ok_projects if f[0] == qmd
        ]

        if last_checks and dt.fromtimestamp(os.stat(qmd).st_mtime) < max(last_checks):
            left_unchecked.append(qmd)
            continue

        create_backup(qmd)

        print(f"{YLW}TESTING:{O}", qmd)

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
            print(RED, "\tFAILED:", O, message)
            continue

        head = content[:yaml_end]
        body = content[yaml_end:]

        spaces = yaml_spaces(head)

        #### Process yaml/head ####
        head = fix_yaml_date(head, spaces, lang, iteration)

        # Find all data paths
        data_paths = find_paths(body, ".csv")
        png_paths = find_paths(body, ".png")

        # Fix yaml
        head = fix_yaml_categories(head, spaces, lang, iteration, data_paths)
        head = hide_broken_thumbnail(qmd, head)

        #### Body ####

        # Check and fix all data paths
        body = update_links(qmd, data_paths, body)
        body = update_links(qmd, png_paths, body)

        # Extract code chunks with regex and execute
        chunks = re.findall(
            r"^[^\n\r\S]*?```[^\n\r\S]*?\{(.*?)\}\s*\n(.*?)^[^\n\r\S]*?```",
            body,
            flags=re.M | re.S,
        )
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

        py_chunks = []
        r_chunks = []

        eval_true = not re.search(r"^\s*eval:\s*false", head, re.M) or re.search(
            r"^\s*#\|\s*eval:\s*true", body, re.M
        )

        if eval_true:
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
                    message = (
                        f"Cannot identify code chunk with option(s) '{ch_options}'"
                    )
                    print(RED, "\tWARNING:", O, message)

        r_code = "\n".join(r_chunks)
        py_code = "\n".join(py_chunks)

        os.chdir(d(qmd))
        if r_code:
            Rout = run("R -s -e".split() + [r_code], capture_output=True)

            if Rout.returncode:
                message = Rout.stderr
                e_log.append((qmd, message.decode()))
                print(RED, "\tFAILED:", O, message)

        if py_code:
            if "plotly" in py_code:
                py_code = (
                    "import plotly.io as pio\npio.renderers.default = None\n" + py_code
                )

            test_py(qmd, py_code, e_log)

        os.chdir(ROOT)

        #### For render ####
        if qmd in [error[0] for error in e_log]:
            if ".exclude" not in qmd:
                to_exclude.add(d(qmd))

            print(RED, "\tFAILS TO RENDER", O)

        else:
            if ".exclude" in qmd:
                # Remove one level from any filepaths
                head = head.replace("../", "")
                body = body.replace("../", "")

                to_include.add(d(qmd))

            print(GRN, "\tSUCCESS", O)

        # Overwrite with patches
        with open(qmd, "w") as f:
            f.write(head + body)

    if e_log:
        print(
            "The following files fail to render and now (or already) live in .exclude/:"
        )
        for file in {error[0] for error in e_log}:
            if d(file) in to_exclude:
                if not os.path.isdir(exclude_dir := j(d(d(file)), ".exclude")):
                    os.mkdir(exclude_dir)

                shutil.move(d(file), exclude_dir)
                to_exclude.remove(d(file))

            print(RED, file, O)

    # Remove any projects with any files that fail even if some pass
    to_include -= {d(file) for file in to_exclude}
    if to_include:
        print("\nThe following projects have been fixed and reincluded:")
        for proj in to_include:
            shutil.move(proj, d(d(proj)))
            print(GRN, d(d(proj)), O)

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
                    qmd + "," + dt.now().strftime("%Y-%m-%d %H:%M:%S")
                    for qmd in qmds
                    if qmd not in [e[0] for e in e_log] and qmd not in left_unchecked
                ]
            )
        )

    # Compare state before and after to remove any created files
    # Some redundancy here given the previous to_include/to_exclude stuff
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
                print(BLU, file, O)

            if dev and input("\nWould you like to keep these? [y]/n: ").lower() == "n":
                for file in backups:
                    os.remove(file)

        if new_files:
            print("\nProject testing has created new files.")
            for file in new_files:
                print(BLU, file, O)
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
            print(BLU, path, O)
        if dev and input("\nWould you like to keep these? [y]/n: ").lower() == "n":
            for path in empty_dirs:
                os.rmdir(path)


if __name__ == "__main__":
    run_checker(True)
