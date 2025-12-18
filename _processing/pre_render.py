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
project_status = project_processing.run_checker()
print()
print(BLD, "Running general checker", O)
general_status = general_processing.process_content()
print("Pre-render jobs have finished with the following statuses:")
print()
print("project_processing.py:", pick_ANSI_colour(project_status), project_status, O)
print("general_processing.py:", pick_ANSI_colour(general_status), general_status, O)
print()
print("Proceeding with render.")
