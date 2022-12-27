import sys
import os
import subprocess
import shutil
import concurrent.futures
import subprocess

# Get the number of times from the command line argument
# num_times = int(sys.argv[2])
# case_name = str(sys.argv[1])
# resultTypes=["perturbSin","unsteadySin"]

def read_vars_file(variables2read):
    """Reads the .vars file in the current working directory and returns its contents as a dictionary."""
    # Find the .vars file in the current working directory
    File_extension=".vars"
    variableDictionary = {}
    cwd = os.getcwd()
    vars_file = None
    for file in os.listdir(cwd):
        if file.endswith(File_extension):
            extension_lengt = len(File_extension)
            vars_file = file
            variableDictionary["case_name"] = vars_file[:-extension_lengt]
            break
    # Return an empty dictionary if no .vars file was found
    if vars_file is None:
        return None
    # Read the .vars file and parse its contents
    with open(vars_file, "r") as f:
        for line in f:
            line = line.strip()
            for targetVariable in variables2read:
                if line.startswith(targetVariable):
                    variable_value = line.split(":")[1].strip()
                    variableDictionary[targetVariable] = variable_value
                    variables2read.remove(targetVariable)
                    break
    return variableDictionary

def run_subprocess(cmd):
    return subprocess.run(cmd, shell=True, check=True)

def runCommandsParalel(commands=['ls -l', 'ls -l', 'ls -l'], max_workers=64):
    #runs commands in paralel
    # List of commands to run are commands
    commands_Number = len(commands)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Launch subprocesses in parallel, up to max_workers at a time
        results = [executor.submit(run_subprocess, cmd) for cmd in commands]
        i=0
        for result in concurrent.futures.as_completed(results):
            print(result.result())
            i+=1
    if i==commands_Number:
        print("ALL DONE NICELY")
        return 0
    else:
        print("FAIL")
        return 1

def createCommandsList(case_name, num_times, resultTypes=["perturbSin"]):
    """
    Generates a list of commands for extracting data from a case file.

    Parameters:
    - case_name (str): The name of the case file.
    - num_times (int): The number of time steps to extract data for.
    - resultTypes (list): The types of results to extract data for.

    Returns:
    - list: A list of commands to run.
    """
    # Create the base commands
    commands = [
        f"extract -vtk64 {case_name} real",
        f"extract -vtk64 {case_name} imag",
        f"extract -vtk64 {case_name} phi",
        f"extract -vtk64 {case_name} amp",
    ]
    # Add commands for each result type
    for result in resultTypes:
        for i in range(1, num_times + 1):
            commands.append(f"extract -vtk64 {case_name} {result}{i}")
    return commands

def combine_results(nametag):
    cwd = os.getcwd()
    folders = [folder for folder in os.listdir(cwd) if "."+nametag in folder]
    # Print the found folders
    for folder in folders:
        print(folder)
    source_folders=folders
    # Set the destination folder
    destination_folder = nametag+"ANIMATE"
    # Set the target filename
    target_filename = "Volume64.vtu"
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    # Loop through the source folders
    for folder in source_folders:
        # Construct the full file path for the source file
        i = folder.split(nametag)[1]
        destination_file_name = target_filename.split(".")[0] + "_" + str(i) + ".vtu"
        source_path = os.path.join(folder, target_filename)
        destination_path = os.path.join(destination_folder, destination_file_name)
        # Check if the file exists in the source folder
        if os.path.exists(source_path):
            try:
                shutil.copy(source_path, destination_path)
                shutil.rmtree(folder)
            except shutil.Error as e:
                print("Error copying file: ", e)
            except OSError as e:
                print("Error deleting folder: ", e)
        else:
            print("File not found: ", source_path)
    print("Successfully deleted temp source folders and created animation files")
#___________________________________________________________________________________________
#______________________________________THE MAIN CODE________________________________________
# __________________________________________________________________________________________
variables2read = ["segmentNumber", "wave"]
parameters=read_vars_file(variables2read)

caseName = parameters["case_name"]
waveType = parameters["wave"].capitalize()
segmentNumber = int(parameters["segmentNumber"])
resultTypes=[f"perturb{waveType}",f"unsteady{waveType}"]

commandList = createCommandsList(caseName,segmentNumber,resultTypes)
if not runCommandsParalel(commandList):
    for result in resultTypes:
        combine_results(result)