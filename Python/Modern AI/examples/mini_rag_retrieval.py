"""Build a tiny offline retrieval-augmented context with TF-IDF."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

TOKEN_PATTERN = re.compile(r"[\u4e00-\u9fff]|[a-z0-9]+")


@dataclass(frozen=True)
class Document:
    """A small knowledge-base document."""

    title: str
    text: str


def tokenize(text: str) -> list[str]:
    """Split ASCII words and Chinese characters for this teaching demo."""
    return TOKEN_PATTERN.findall(text.lower())


def inverse_document_frequency(documents: list[Document]) -> dict[str, float]:
    """Calculate smoothed inverse document frequency for all tokens."""
    document_frequency: Counter[str] = Counter()
    for document in documents:
        document_frequency.update(set(tokenize(document.text)))

    document_count = len(documents)
    return {
        token: math.log((document_count + 1) / (frequency + 1)) + 1
        for token, frequency in document_frequency.items()
    }


def tf_idf_vector(text: str, idf: dict[str, float]) -> dict[str, float]:
    """Convert text into a sparse TF-IDF vector."""
    tokens = tokenize(text)
    if not tokens:
        return {}

    counts = Counter(tokens)
    total = len(tokens)
    return {
        token: (frequency / total) * idf[token]
        for token, frequency in counts.items()
        if token in idf
    }


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    """Measure the angle similarity between two sparse vectors."""
    if not left or not right:
        return 0.0

    dot_product = sum(value * right.get(token, 0.0) for token, value in left.items())
    left_length = math.sqrt(sum(value * value for value in left.values()))
    right_length = math.sqrt(sum(value * value for value in right.values()))
    return dot_product / (left_length * right_length)


def retrieve(
    query: str,
    documents: list[Document],
    *,
    top_k: int = 2,
) -> list[tuple[Document, float]]:
    """Return the most relevant documents and their similarity scores."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    idf = inverse_document_frequency(documents)
    query_vector = tf_idf_vector(query, idf)
    ranked = [
        (document, cosine_similarity(query_vector, tf_idf_vector(document.text, idf)))
        for document in documents
    ]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:top_k]


def build_grounded_prompt(query: str, matches: list[tuple[Document, float]]) -> str:
    """Combine retrieved evidence with a question for a later model call."""
    context = "\n\n".join(
        f"[{index}] {document.title}\n{document.text}"
        for index, (document, _) in enumerate(matches, start=1)
    )
    return (
        "请只根据下面的资料回答问题；资料不足时明确说不知道。\n\n"
        f"资料：\n{context}\n\n问题：{query}\n回答："
    )


def main() -> int:
    documents = [
        Document("Git 提交", "git commit 把暂存区的修改保存到本地仓库。"),
        Document("Git 推送", "git push 把本地提交发送到远程仓库。"),
        Document("Python 环境", "venv 可以为每个 Python 项目创建独立的依赖环境。"),
        Document("Linux 服务", "systemctl status 可以查看 systemd 服务的当前状态。"),
    ]
    query = "怎样把本地提交发送到远程仓库？"
    matches = retrieve(query, documents, top_k=2)

    print("Retrieved documents:")
    for document, score in matches:
        print(f"  score={score:.3f}  {document.title}")

    print("\nPrompt prepared for a language model:\n")
    print(build_grounded_prompt(query, matches))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
