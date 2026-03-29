import re

_LOWER_START = re.compile(
    r"\n(?=[a-záàảãạăắặằẳẵâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ])"
)

def split_sentences(text):
    text = text.replace("•", ". ")
    text = re.sub(r"^\s*[-–]\s+", ". ", text, flags=re.MULTILINE)

    text = _LOWER_START.sub(" ", text)

    text = re.sub(r"\n+", ". ", text)

    raw = re.split(r"(?<=[.!?])\s+", text)

    sentences = []
    for s in raw:
        s = s.strip()
        if len(s) > 10 and re.search(r"[a-zA-ZÀ-ỹ]", s):
            sentences.append(s)

    return sentences