import re


def _split_into_sentences(text: str) -> list[str]:
    return re.split(r'(?<=[.!?])\s+', text)


def _word_boundary_start(text: str, start_index: int) -> int:
    if start_index <= 0 or text[start_index].isspace():
        return max(0, start_index)

    whitespace_positions = [
        text.rfind(" ", 0, start_index),
        text.rfind("\n", 0, start_index),
        text.rfind("\t", 0, start_index),
    ]
    previous_whitespace = max(whitespace_positions)
    return previous_whitespace + 1 if previous_whitespace != -1 else 0


def _safe_overlap(text: str, overlap: int) -> str:
    if overlap <= 0 or not text:
        return ""

    start_index = _word_boundary_start(text, max(0, len(text) - overlap))

    return text[start_index:].lstrip()


def _trim_overlap_to_fit(overlap_text: str, sentence: str, max_chunk_size: int) -> str:
    if not overlap_text:
        return ""

    available_space = max_chunk_size - len(sentence) - 1
    if available_space <= 0:
        return ""

    if len(overlap_text) <= available_space:
        return overlap_text

    start_index = _word_boundary_start(
        overlap_text, len(overlap_text) - available_space
    )

    return overlap_text[start_index:].lstrip()


def chunk_text(text: str, max_chunk_size: int = 512, overlap: int = 64) -> list[str]:
    sentences = _split_into_sentences(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            overlap_text = _safe_overlap(current_chunk, overlap)
            overlap_text = _trim_overlap_to_fit(overlap_text, sentence, max_chunk_size)
            current_chunk = (
                f"{overlap_text} {sentence}".strip() if overlap_text else sentence
            )

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
