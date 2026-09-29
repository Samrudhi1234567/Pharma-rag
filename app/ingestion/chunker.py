from dataclasses import dataclass


@dataclass
class TextChunk:
    chunk_index: int
    content: str


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[TextChunk]:
    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized_text = " ".join(text.split())

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(normalized_text):
        end = min(start + chunk_size, len(normalized_text))

        content = normalized_text[start:end].strip()

        if content:
            chunks.append(
                TextChunk(
                    chunk_index=chunk_index,
                    content=content,
                )
            )

        if end >= len(normalized_text):
            break

        start = end - chunk_overlap
        chunk_index += 1

    return chunks