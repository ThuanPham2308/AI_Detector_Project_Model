import re

_SECTION_PATTERN = re.compile(
    r"^(\d{1,2}(?:\.\d{1,2}){1,3}\.?\s+[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯ].{2,})",
    re.MULTILINE,
)


def split_sections(text):
    matches = list(_SECTION_PATTERN.finditer(text))

    if not matches:
        return []

    sections = []

    for i, match in enumerate(matches):
        start = match.start()
        title = match.group().strip()

        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        content = text[start:end].strip()

        sections.append({
            "title": title,
            "content": content,
        })

    return sections