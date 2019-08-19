from PyPDF2 import PdfFileMerger

#  List PDF to merge in order (Add more if required separated by a comma)
pdfs = ['file1.pdf','file2.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()