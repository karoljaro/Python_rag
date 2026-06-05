import re


def split_into_sentences(text: str) -> list[str]:
    return re.split(r'(?<=[.!?]) +', text)


def chunk_text(text: str, max_chunk_size: int = 512, overlap: int = 64) -> list[str]:
    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = current_chunk[-overlap:] + " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
