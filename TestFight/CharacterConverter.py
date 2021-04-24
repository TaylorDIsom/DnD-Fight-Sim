# imports
import PyPDF2
# import pytesseract

file = 'character.pdf'
pdf = open(file, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdf)
numpages = pdfReader.numPages
print(numpages)

docInfo = pdfReader.getDocumentInfo()
print(docInfo)

fields = pdfReader.getFields()
# print(fields)

textFields = pdfReader.getFormTextFields()
# print(textFields)

# THIS IS NOTHING
# namedDests = pdfReader.getNamedDestinations()
# print(namedDests)

# THIS IS NOTHING
# outlines = pdfReader.getOutlines()
# print(outlines)

# print(pdf.read())

# print('________________________________________________________')

# for field, text in textFields.items():
#     # pgObj = pdfReader.getPage(pg)
#     # text = pgObj.extractText()
#     # contents = pgObj.getContents()
#     print(field, ':', text)


