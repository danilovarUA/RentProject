from docx import Document


class Doc:
    def __init__(self, filepath, new_filepath, replacement_dict):
        self.document = Document(filepath)
        self.replace(replacement_dict)
        self.save(new_filepath)

    def replace(self, replacement_dict):
        for pattern in replacement_dict:
            replacement = replacement_dict[pattern]
            for paragraph in self.document.paragraphs:
                if pattern in paragraph.text:
                    inline = paragraph.runs
                    print(str(inline))
                    for i in range(len(inline)):
                        if pattern in inline[i].text:
                            print("patt found")
                            text = inline[i].text.replace(pattern, replacement)
                            inline[i].text = text
                    print(paragraph.text)

    def save(self, new_filepath):
        self.document.save(new_filepath)


def properties_list_to_text(properties_list):
    # TODO not finished
    return "(Properties text)"


if __name__ == "__main__":
    docum = Doc('./Patt.docx', './Res.docx', {"11Орендар11": "Орендар Величезний",
                                              "11Людина11": "Шевченко Т. Г.",
                                              "11Власність11": properties_list_to_text([]),
                                              "11ВідновнаВартість11": "1234",
                                              "11ОстаннійДень11Передачі11": "10/10/2020"})
