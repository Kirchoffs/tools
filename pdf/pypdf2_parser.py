import PyPDF2

pdf_file = open('stock/2021-JUL.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
for page_num in range(len(pdf_reader.pages)):
    page_obj = pdf_reader.pages[page_num]
    print(page_obj.extract_text())
pdf_file.close()