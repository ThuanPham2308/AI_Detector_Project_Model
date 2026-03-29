from docx import Document
from docx.shared import RGBColor

def apply_color(run, color):
    if color == "red":
        run.font.color.rgb = RGBColor(255, 0, 0)
    elif color == "yellow":
        run.font.color.rgb = RGBColor(255, 165, 0)
    elif color == "green":
        run.font.color.rgb = RGBColor(0, 128, 0)

def normalize(text):
    return text.lower().replace("\n", " ").strip()


def find_best_match(para_normalized, all_sentences):
    best = None
    best_len = 0

    for s in all_sentences:
        sent = normalize(s["text"])
        if len(sent) < 20:
            continue

        if sent in para_normalized:
            if len(sent) > best_len:
                best = s
                best_len = len(sent)
        elif para_normalized in sent and len(para_normalized) > 15:
            if len(para_normalized) > best_len:
                best = s
                best_len = len(para_normalized)

    return best


def highlight_runs(doc, all_sentences):
    for para in doc.paragraphs:
        para_normalized = normalize(para.text)

        if not para_normalized or len(para_normalized) < 10:
            continue

        matched = find_best_match(para_normalized, all_sentences)

        if matched and matched["color"] != "black":
            for run in para.runs:
                apply_color(run, matched["color"])


def export_result(chapters, input_path, output_path="output.docx"):
    doc = Document(input_path)

    all_sentences = []
    for ch in chapters:
        for sec in ch.get("sections", []):
            all_sentences.extend(sec.get("sentences", []))

    if not all_sentences:
        print("Không có sentence nào để highlight.")
        doc.save(output_path)
        return

    highlight_runs(doc, all_sentences)

    doc.save(output_path)
    print(f"Saved: {output_path}")