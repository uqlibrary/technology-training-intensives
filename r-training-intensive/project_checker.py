import os
import pandas as pd
import subprocess

# Go through all the project folders and check 

# 1. Data
# 2. Requirements
# 3. File runs without error

os.system("cls")
root = os.getcwd()

errors = []


# Modifications to check for

# 1. Actually running the R code
# 2. Checking the quarto options (html only, no bib)


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
        print(f"Checking \033[1m{path + '/' + filename}\033[0m...")


        # Check data loads
        os.chdir(path)

        load_start = 0
        while True:
            load_start = source.find("read.csv", load_start + 1)

            if load_start == -1:
                break
            
            load_end = source.find(")", load_start) + 1
            
            load_command = source[load_start:load_end]

            load_path = load_command[load_command.find('"')+1:-2]


            try: 
                pd.read_csv(load_path)
            except FileNotFoundError:
                print(f"\033[31mBAD PATH\033[0m ({load_command})\nAttempting fix...")

                # Determine data needed
                matches = [csv for csv in data_paths.keys() if csv in load_command]

                if len(matches) == 0 or len(matches) > 1:
                    print(f"\t\033[31mFix failed, cannot identify data source\033[30m")
                    errors.append((path + '\\' + filename, "\033[31mBAD PATH\033[0m"))
                else:
                    load_patch = f'../../{data_paths[matches[0]]}'
                    
                    try: 
                        pd.read_csv(load_patch)
                    except Exception as e:
                        print(f"\t\033[31mPatch failed with '{e}'\033[30m")
                        errors.append((path + '\\' + filename, "\033[31mBAD PATH\033[0m"))
                    else:
                        source = source.replace(load_path, load_patch)
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
            import_start = source.find("library(", import_start + 1)

            if import_start == -1:
                break
            
            import_end = source.find(")", import_start) + 1

            import_command = source[import_start:import_end]

            import_lib = import_command[import_command.find('(')+1:-1]

            # test_load = subprocess.run(["R","-s","-e",f"suppressMessages(library({import_lib}))"], 
            #                            capture_output=True)
            # test_load = subprocess.run(["R","--version"], 
            #                             capture_output=True)
            
            # input(test_load.stderr.decode())
            # input(test_load.stdout.decode())

            with open(root + "/renv.lock", encoding = "utf8") as f:
                lockfile = f.read()

            if import_lib in lockfile:
                print(f"\033[32mREQS OK\033[0m\t ({import_lib})")
            else:
                print(f"\033[31mBAD REQS\033[0m ({import_lib})")
                errors.append((path + '\\' + filename, "\033[31mBAD REQS\033[0m"))
                


            # try: 
            #     os.system(f'R -s -e suppressMessages(library({import_lib}))')
            # except ModuleNotFoundError:
            #     print(f"\033[31mBAD REQS\033[0m ({import_command})")
            #     errors.append((path + '\\' + filename, "\033[31mBAD REQS\033[0m"))
            # except Exception as e:
            #     print(f"\033[31mERROR\033[0m '{e}' with '{import_command}'")
            #     errors.append((path + '\\' + filename, e))
            # else:
            #     print(f"\033[32mREQS OK\033[0m\t ({import_command})")

        # Collect R chunks and check for additional errors
        # chunk_start = 0
        # r_chunk_start = 0
        # R_chunk_start = 0
        # R_source = ""
        # while True:
        #     r_chunk_start = source.find(r"```{r}", r_chunk_start + 1)
        #     R_chunk_start = source.find(r"```{R}", R_chunk_start + 1)

        #     if r_chunk_start == -1 and R_chunk_start == -1:
        #         break
        #     elif r_chunk_start == -1:
        #         chunk_start = R_chunk_start
        #     elif R_chunk_start == -1:
        #         chunk_start = r_chunk_start
        #     else:
        #         chunk_start = min(r_chunk_start, R_chunk_start)
            
        #     chunk_end = source.find("```", chunk_start + 1)

        #     R_source += source[chunk_start+7:chunk_end]       

        # with open("temp.R", "w") as temp:
        #     temp.write(R_source)

        #     subprocess.run(["R", "-f", "temp.R"])
        #     input()
             
        # subprocess.run(["R","-e", R_source])
        # try:
        #     exec(py_source)
        # except Exception as e:
        #     print(f"\033[31mFILE ERROR\033[0m '{e}'")
        #     errors.append((path + '\\' + filename, e))
        # else:
        #     print(f"\033[32mFILE OK\033[0m")

        os.chdir(root)


print(f"\nSummary of outstanding errors")
for error in errors:
    print(error[0], error[1], sep = "\t")
