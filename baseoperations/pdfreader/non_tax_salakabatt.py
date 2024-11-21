import os
import pdfplumber
from PyPDF2 import PdfReader



pdf_path = '/mnt/c/Users/Asus/OneDrive/Desktop/ACC_2024/ACC_2024/10-24/BugetReportKAM12_16102024 (ទូទាត់រង្វាន់សេវាសាធារណៈ).pdf'

if os.path.exists(pdf_path):
    reader = PdfReader(pdf_path)
else:
    pass

text = ""
for page in reader.pages:
    text += page.extract_text()

VVF = text[364:367]
CSF = text[384:388]
CDL = text[608:611]
CDL_Value = text[611:621]
print(f'{CDL}: {CDL_Value}')