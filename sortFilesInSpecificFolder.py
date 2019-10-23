# importing libraries used within the program
import os
from pathlib import Path

# Dictionary (Add more where the files type you want isn't in the DIRECTORIES)
DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  ".pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAIN TEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "PYTHON": [".py"],
    "DEVOLOPMENT SCRIPT": [".js"],
    "SAS PROGRAMS": [".sas"],
    "SQL SCRIPTS": [".sql"],
    "JSON": [".json"],
    "LOGS": [".log"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"],
    "CITRIX CONNECTION": [".ica"],
    "AODBE": [".xd",".psd",".ai"]
}

FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}
# This will organise your files
def organise():
    for entry in os.scandir():
        if entry.is_dir():
            continue
        file_path = Path(entry.name)
        file_format = file_path.suffix.lower()
        if file_format in FILE_FORMATS:
            directory_path = Path(FILE_FORMATS[file_format])
            directory_path.mkdir(exist_ok=True)
            # file_path.rename(directory_path.joinpath(file_path))
            # changed to REPLACE method so if the file already exist in the folder the it silently overwrites it.
            file_path.replace(directory_path.joinpath(file_path))
   # If extension not found within the dictionary than create a folder name  called "OTHER-FILES"
    try:
        os.mkdir('OTHER')
    except:
        pass
    for dir in os.scandir():
        try:
            # Delete empty folders
            if dir.is_dir():
                os.rmdir(dir)
            else:
                os.rename(os.getcwd() + '/' + str(Path(dir)), os.getcwd() + '/OTHER/' + str(Path(dir)))
        except:
            pass
if __name__ == "__main__":
	# change the current working directory
    currentWorkingFolder = '/Users/sukobl/Downloads'
    os.chdir(currentWorkingFolder)
    organise()
