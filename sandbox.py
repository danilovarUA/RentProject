from docx import Document


def replace_string(filename):
    doc = Document(filename)
    for p in doc.paragraphs:
        if 'ПЕРЕДАЧІ' in p.text:
            inline = p.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                if 'ПЕРЕДАЧІ' in inline[i].text:
                    text = inline[i].text.replace('ПЕРЕДАЧІ', '!!!уамукукум')
                    inline[i].text = text
            print(p.text)

    doc.save('dest1.docx')
    return 1

replace_string("Test.docx")