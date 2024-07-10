from docxtpl import DocxTemplate
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

def report_doc():
    doc = DocxTemplate('../template_doc/template_tests_GRE.docx')
    with open('../valueReportTest.txt','r') as file:
        data = file.readlines()
    context = {}
    for line in data:
        key, value = line.strip().split(':')
        context[key] = value 
    
    
    # context = {'ver_platform':' BS7510-48X6Q', 'ver_fw':'2.5.0-rc0-1-g0b870dfb'}
    doc.render(context)
    print(context)
    report_doc_name = "report_tests_GRE.docx"
    doc.save(f'../report_doc/{report_doc_name}')
    print(f"Создан word-отчет по тестам c именем {report_doc_name}")
    with open('../valueReportTest.txt','w') as file:
        pass

if __name__=="__main__":
    report_doc()