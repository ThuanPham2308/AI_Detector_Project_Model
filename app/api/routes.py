from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.read_docx import read_docx
from app.read_pdf import read_pdf
from app.chapter_splitter import split_chapters
from app.section_splitter import split_sections
from app.ai_checker import check_paragraph

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/check-file")
async def check_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ===== Read file =====
    if file.filename.endswith(".docx"):
        text = read_docx(file_path)
    elif file.filename.endswith(".pdf"):
        text = read_pdf(file_path)
    else:
        return {"error": "Chỉ hỗ trợ .docx hoặc .pdf"}

    chapters = split_chapters(text)
    if not chapters:
        chapters = [{"title": "Full Document", "content": text}]

    final_output = []

    total_weighted = 0
    total_words = 0

    for ch in chapters:
        sections = split_sections(ch["content"])
        if not sections:
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
                    "text": s["text"],
                    "score": round(s["score"] * 100, 2),
                    "color": s["color"]
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
                "ai_percent": round(sec_percent, 2),
                "sentences": sentences_display
            })

        ch_percent = ch_weighted / ch_words if ch_words > 0 else 0

        final_output.append({
            "title": ch["title"],
            "ai_percent": round(ch_percent, 2),
            "sections": section_results
        })

    total_percent = total_weighted / total_words if total_words > 0 else 0

    return {
        "ai_percent": round(total_percent, 2),
        "chapters": final_output
    }