from docx import Document

def read_docx(file_path):
    doc = Document(file_path)

    full_text = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            full_text.append(text)

    return "\n".join(full_text)