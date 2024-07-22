from docxtpl import DocxTemplate
from docx2pdf import convert

def gendocx(template, context, docxPath):
    doc = DocxTemplate(template)
#    set_of_variables = doc.get_undeclared_template_variables()
    doc.render(context)
    doc.save(docxPath)

def docx2pdf(docxPath, pdfPath):
    convert(docxPath, pdfPath)
