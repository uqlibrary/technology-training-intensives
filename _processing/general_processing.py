from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz

from glob import glob
from os.path import dirname as d
from os.path import basename as b
from os.path import join as j
from os.path import isfile

import yaml

import project_processing


def find_rendered_files(
    yaml_path: str = "_quarto.yml", exclude_projects: bool = True
) -> set[str]:
    with open(yaml_path) as f:
        proj_yaml = yaml.full_load(f)

    globs = (g + "*" if g.endswith("*") else g for g in proj_yaml["project"]["render"])

    files = {f for g in globs for f in glob(g, recursive=True) if isfile(f)}

    if exclude_projects:
        files = {f for f in files if "gallery" not in f or d(f) == "gallery"}

    return files


def change_active_tabset(source: str) -> str:

    active_specifier = "## R {.active}"
    bad_specifier = "## Python {.active}"

    # If during Python intensive, swap
    if dt(2026, 2, 1) < dt.now() < dt(2026, 2, 10):
        active_specifier, bad_specifier = (bad_specifier, active_specifier)

    # Find first tabset
    if '.panel-tabset group="lang"' in source:
        first_tabset_i = source.index('::: {.panel-tabset group="lang"')

        if bad_specifier in source:
            source = source.replace(bad_specifier, bad_specifier[:-10])
            print(
                project_processing.GRN,
                "\tFIXED:",
                project_processing.O,
                bad_specifier,
                "->",
                bad_specifier[:-10],
            )

        if active_specifier not in source:
            source = source[:first_tabset_i] + source[first_tabset_i:].replace(
                active_specifier[:-10], active_specifier, 1
            )
            print(
                project_processing.GRN,
                "\tFIXED:",
                project_processing.O,
                active_specifier[:-10],
                "->",
                active_specifier,
            )

        if source.count("{.active}") == 0:
            print(
                project_processing.RED,
                "\tWARNING:",
                project_processing.O,
                "No {.active} tags in tabsets!",
            )
        elif source.count("{.active}") > 1:
            print(
                project_processing.RED,
                "\tWARNING:",
                project_processing.O,
                "Multiple {.active} produced!",
            )

    elif source.count("{.active}") != 0:
        print(
            project_processing.RED,
            "\tWARNING:",
            project_processing.O,
            "{.active} present yet no tabsets found!",
        )

    return source


def insert_banner(source: str) -> str:
    raise NotImplementedError()


def remove_banner(source: str) -> str:
    raise NotImplementedError()


def process_content() -> str:
    # Determine all rendered files, exclude those in gallery
    qmds = find_rendered_files()

    for qmd in ("./" + f for f in qmds):
        print(project_processing.YLW, "CHECKING:", project_processing.O, qmd)
        with open(qmd) as f:
            content = f.read()

        # Fix paths in Python or R cells - note, this DOES NOT fix paths in markdown cells
        csv_paths = project_processing.find_paths(content, ".csv")
        png_paths = project_processing.find_paths(content, ".png")
        all_paths = csv_paths | png_paths

        content = project_processing.update_links(qmd, all_paths, content)

        content = change_active_tabset(content)

        with open(qmd, "w") as f:
            f.write(content)

    return "COMPLETED"


if __name__ == "__main__":
    process_content()
