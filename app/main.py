from app.read_docx import read_docx
from app.read_pdf import read_pdf
from app.chapter_splitter import split_chapters
from app.section_splitter import split_sections
from app.ai_checker import check_paragraph
from app.export_docx import export_result

import os

def process_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File không tồn tại: {path}")

    if path.endswith(".docx"):
        text = read_docx(path)
    elif path.endswith(".pdf"):
        text = read_pdf(path)
    else:
        raise ValueError("Chỉ hỗ trợ .docx hoặc .pdf")

    chapters = split_chapters(text)
    print("Số chương:", len(chapters))

    if len(chapters) == 0:
        chapters = [{"title": "Full Document", "content": text}]

    final_output = []

    total_weighted = 0
    total_words = 0

    for ch in chapters:
        print(f"\nProcessing Chapter: {ch['title']}")

        sections = split_sections(ch["content"])
        print("  Sections:", len(sections))

        if len(sections) == 0:
            sections = [{"title": ch["title"], "content": ch["content"]}]

        section_results = []

        ch_weighted = 0
        ch_words = 0

        for sec in sections:
            result = check_paragraph(sec["content"])

            sentences = result["sentences"]
            sec_percent = result["ai_percent"]

            sentences_display = [
                {
                    **s,
                    "score": round(s["score"] * 100, 2)
                }
                for s in sentences
            ]

            sec_words = sum(len(s["text"].split()) for s in sentences)

            ch_weighted += sec_percent * sec_words
            ch_words += sec_words

            total_weighted += sec_percent * sec_words
            total_words += sec_words

            section_results.append({
                "title": sec["title"],
                "sentences": sentences_display,
                "ai_percent": round(sec_percent, 2)
            })

            print(f"   - {sec['title']} | {sec_percent:.2f}% AI")

        ch_percent = ch_weighted / ch_words if ch_words > 0 else 0

        final_output.append({
            "title": ch["title"],
            "sections": section_results,
            "ai_percent": round(ch_percent, 2)
        })

        print(f"Chapter AI: {ch_percent:.2f}%")

    percent = total_weighted / total_words if total_words > 0 else 0

    print(f"AI content: {percent:.2f}%")

    export_result(final_output, input_path=path)

if __name__ == "__main__":
    process_file("template.docx")