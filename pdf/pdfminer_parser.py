from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    output_stream = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, output_stream, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as pdf_file:
        for page in PDFPage.get_pages(pdf_file):
            interpreter.process_page(page)
    text = output_stream.getvalue()
    converter.close()
    output_stream.close()
    return text

pdf_text = extract_text_from_pdf('stock/2022-JAN.pdf')
print(pdf_text)
