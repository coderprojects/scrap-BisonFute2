import shutil
import os

baseFolder = os.getcwd()

# we have 2 directories to compress
for rep_data in ["QTV_Data", "RRN_Data"]:
    dir = os.path.join(baseFolder, rep_data)
    os.chdir(dir)
    # Get all the file in the dir_day repository
    # We only have day directories under the main folder
    list_elt = [dir_day for dir_day in os.listdir(os.getcwd())]
    # Filter to keep only the directories
    list_elt = list(filter(lambda elt: os.path.isdir(elt), list_elt))
    # Remove the most recent one (the one with the maximum number)
    list_elt.remove(str(max(list(map(int, list_elt)))))
    #For each folder (but the most recent one), 1) compress it, 2) remove the folder.
    for dir in list_elt:
        print(dir)
        shutil.make_archive(os.path.join(os.getcwd(),dir), 'zip', os.path.join(os.getcwd(),dir))
        shutil.rmtree(os.path.join(os.getcwd(),dir))