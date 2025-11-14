import os
import pandas as pd
import matplotlib as mpl
import warnings
warnings.filterwarnings("ignore")
# Go through all the project folders and check 

# 1. Data
# 2. Requirements
# 3. File runs without error

root = os.getcwd()

errors = []

mpl.use("Agg")

# Make dict of data paths
data_paths = {csv[:-4]:"data_sources/"+csv for csv in os.listdir("data_sources")}

for path, dirs, files in os.walk("Projects"):
    if path == "Projects":
        continue

    for filename in files:
        if filename[-4:] != ".qmd":
            continue

        with open(path + "/" + filename) as project:
            source = project.read()

        print()
        print(f"Checking \033[1m{path + '\\' + filename}\033[0m...")


        # Check data loads
        os.chdir(path)

        load_start = 0
        while True:
            load_start = source.find("pd.read", load_start + 1)

            if load_start == -1:
                break
            
            load_end = source.find(")", load_start) + 1
            
            load_command = source[load_start:load_end]

            try: 
                exec(load_command)
            except FileNotFoundError:
                print(f"\033[31mBAD PATH\033[0m ({load_command})\n\tAttempting fix...")

                # Determine data needed
                matches = [csv for csv in data_paths.keys() if csv in load_command]

                if len(matches) == 0 or len(matches) > 1:
                    print(f"\t\033[31mFix failed, cannot identify data source\033[30m")
                    errors.append((path + '\\' + filename, "\033[31mBAD PATH\033[0m"))
                else:
                    load_patch = f'pd.read_csv("../../{data_paths[matches[0]]}")'
                    
                    try: 
                        exec(load_patch)
                    except Exception as e:
                        print(f"\t\033[31mPatch failed with '{e}'\033[30m")
                        errors.append((path + '\\' + filename, "\033[31mBAD PATH\033[0m"))
                    else:
                        source = source.replace(load_command, load_patch)
                        with open(filename, "w") as project:
                            project.write(source)
                        print(f"\t\033[32mPatch succesful!\033[30m")


            except Exception as e:
                print(f"\033[31mERROR\033[0m '{e}' with '{load_command}'")
                errors.append((path + '\\' + filename, e))
            else:
                print(f"\033[32mDATA OK\033[0m\t ({load_command})")
                

        # Check dependencies
        import_start = 0
        while True:
            import_start = source.find("import", import_start + 1)

            if import_start == -1:
                break
            
            import_end = source.find("\n", import_start)

            import_command = source[import_start:import_end]

            try: 
                exec(import_command)
            except ModuleNotFoundError:
                print(f"\033[31mBAD REQS\033[0m ({import_command})")
                errors.append((path + '\\' + filename, "\033[31mBAD REQS\033[0m"))
            except Exception as e:
                print(f"\033[31mERROR\033[0m '{e}' with '{import_command}'")
                errors.append((path + '\\' + filename, e))
            else:
                print(f"\033[32mREQS OK\033[0m\t ({import_command})")

        # Collect Python chunks and check for additional errors
        chunk_start = 0
        py_source = ""
        while True:
            chunk_start = source.find(r"```{python}", chunk_start + 1)

            if chunk_start == -1:
                break

            chunk_end = source.find("```", chunk_start + 1)

            py_source += source[chunk_start+11:chunk_end]
            
        try:
            exec(py_source)
        except Exception as e:
            print(f"\033[31mFILE ERROR\033[0m '{e}'")
            errors.append((path + '\\' + filename, e))
        else:
            print(f"\033[32mFILE OK\033[0m")

    os.chdir(root)


print(f"\nSummary of errors")
for error in errors:
    print(error[0], error[1], sep = "\t")