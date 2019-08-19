import os
from PyPDF2 import PdfFileMerger

# list files with .pdf as extension
x = [a for a in os.listdir() if a.endswith(".pdf")]

merger = PdfFileMerger()

for pdf in x:
    merger.append(open(pdf, 'rb'))

with open("result.pdf", "wb") as fout:
    merger.write(fout)