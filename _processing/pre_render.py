import time
import project_processing
from project_processing import O
import general_processing

BLD = "\033[1m"


def pick_ANSI_colour(status: str) -> str:
    if "FAIL" not in status:
        return project_processing.GRN
    elif "COMPLETED" in status:
        return project_processing.YLW
    else:
        return project_processing.RED


print(BLD, "Running project checker", O)
start = time.time()
project_status = project_processing.run_checker()
end = time.time()
proj_t = round(end - start, 2)
print()
print(f"Project processing took {proj_t}s")
print()
print(BLD, "Running general checker", O)
start = time.time()
general_status = general_processing.process_content()
end = time.time()
gen_t = round(end - start, 2)
print()
print(f"General processing took {gen_t}s")
print()
print("Pre-render jobs have finished with the following statuses:")
print()
print(
    "project_processing.py:",
    pick_ANSI_colour(project_status),
    project_status,
    O,
    "in",
    proj_t,
    "s",
)
print(
    "general_processing.py:",
    pick_ANSI_colour(general_status),
    general_status,
    O,
    "in",
    gen_t,
    "s",
)
print()
print("Proceeding with render.")
