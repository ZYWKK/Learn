"""Train a tiny byte-pair-style subword tokenizer with plain Python."""

from __future__ import annotations

from collections import Counter

SymbolSequence = tuple[str, ...]
Vocabulary = dict[SymbolSequence, int]
Pair = tuple[str, str]


def split_word(word: str) -> SymbolSequence:
    """Represent a word as characters plus an end-of-word marker."""
    return tuple(word) + ("</w>",)


def count_pairs(vocabulary: Vocabulary) -> Counter[Pair]:
    """Count adjacent symbol pairs, weighted by word frequency."""
    counts: Counter[Pair] = Counter()
    for symbols, frequency in vocabulary.items():
        counts.update(
            {
                (symbols[index], symbols[index + 1]): frequency
                for index in range(len(symbols) - 1)
            }
        )
    return counts


def merge_symbols(symbols: SymbolSequence, pair: Pair) -> SymbolSequence:
    """Merge every adjacent occurrence of one selected pair."""
    merged: list[str] = []
    index = 0
    while index < len(symbols):
        if index + 1 < len(symbols) and symbols[index : index + 2] == pair:
            merged.append("".join(pair))
            index += 2
        else:
            merged.append(symbols[index])
            index += 1
    return tuple(merged)


def train_bpe(corpus: dict[str, int], merge_count: int) -> tuple[list[Pair], Vocabulary]:
    """Learn frequent pair merges from a word-frequency dictionary."""
    vocabulary = {split_word(word): frequency for word, frequency in corpus.items()}
    merges: list[Pair] = []

    for _ in range(merge_count):
        pair_counts = count_pairs(vocabulary)
        if not pair_counts:
            break

        best_pair = max(pair_counts.items(), key=lambda item: (item[1], item[0]))[0]
        merges.append(best_pair)

        next_vocabulary: Vocabulary = {}
        for symbols, frequency in vocabulary.items():
            merged_symbols = merge_symbols(symbols, best_pair)
            next_vocabulary[merged_symbols] = frequency
        vocabulary = next_vocabulary

    return merges, vocabulary


def encode_word(word: str, merges: list[Pair]) -> list[str]:
    """Apply learned merges to a new word and return readable tokens."""
    symbols = split_word(word)
    for pair in merges:
        symbols = merge_symbols(symbols, pair)

    tokens = []
    for symbol in symbols:
        cleaned = symbol.replace("</w>", "")
        if cleaned:
            tokens.append(cleaned)
    return tokens


def main() -> int:
    corpus = {
        "learn": 5,
        "learner": 3,
        "learning": 6,
        "relearn": 2,
    }
    merges, vocabulary = train_bpe(corpus, merge_count=8)

    print("Learned merge rules:")
    for step, pair in enumerate(merges, start=1):
        print(f"  {step:>2}. {pair[0]!r} + {pair[1]!r}")

    print("\nFinal training vocabulary:")
    for symbols, frequency in vocabulary.items():
        print(f"  {symbols}  frequency={frequency}")

    print("\nEncoding new words:")
    for word in ("learning", "learners", "relearning"):
        print(f"  {word:<10} -> {encode_word(word, merges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
