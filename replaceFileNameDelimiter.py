import os

directory = '/Users/sukobl/Downloads/Temp'
# improve later to take a list of delimiter types
currentDelimiter = ' '
newDelimiter = '_'
[os.rename(os.path.join(directory, files), os.path.join(directory, files).replace(currentDelimiter, newDelimiter).lower()) for files in os.listdir(directory)]