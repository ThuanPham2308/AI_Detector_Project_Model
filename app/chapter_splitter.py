import re

_CHAPTER_PATTERN = re.compile(
    r"((?:chương|chapter)\s+[\dIVXivx]+\s*[:\.\-]?\s*.+)",
    re.IGNORECASE,
)

def split_chapters(text):
    matches = list(_CHAPTER_PATTERN.finditer(text))

    if not matches:
        return []

    chapters = []

    for i, match in enumerate(matches):
        start = match.start()
        title = match.group().strip()

        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        content = text[start:end].strip()

        chapters.append({
            "title": title,
            "content": content,
        })

    return chapters