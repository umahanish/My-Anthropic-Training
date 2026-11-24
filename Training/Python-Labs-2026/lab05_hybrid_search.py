"""Lab 5.2: hybrid retrieval (BM25 + reciprocal rank fusion) with no API key needed.

Embeddings are added in the Voyage section (needs VOYAGE_API_KEY).
Run: python lab05_hybrid_search.py
"""
import re

from rank_bm25 import BM25Okapi

DOCS = {
    "Nimbus Cloud Services": "Primary cloud hosting, compute, storage and managed databases. Contract NCS-2025-0142. Auto-renews unless cancelled 30 days prior.",
    "BrightPath Security Solutions": "Endpoint security tooling, vulnerability scanning and quarterly compliance reports. Contract BPS-2025-0087. Auto-renews unless cancelled 45 days prior.",
    "Vertex Networking Group": "Managed WAN circuits and telecom support for regional offices. Contract VNG-2025-0219. Auto-renews unless cancelled 60 days prior.",
    "Alderwood Office Supplies": "IT peripherals, cabling and consumables. Contract AOS-2025-0033. Auto-renews unless cancelled 60 days prior.",
    "Fixed-Term Consulting LLC": "Contract engineering support for the modernisation project. Contract FTC-2025-0061. Fixed term, no auto-renewal.",
}


def tokenize(text: str) -> list[str]:
    # Keep letters and digits together so "NCS-2025-0142" stays matchable.
    return re.findall(r"[a-z0-9]+", text.lower())


def bm25_rank(query: str) -> list[str]:
    names = list(DOCS)
    bm25 = BM25Okapi([tokenize(d) for d in DOCS.values()])
    scores = bm25.get_scores(tokenize(query))
    return [n for n, _ in sorted(zip(names, scores), key=lambda x: -x[1])]


def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Reciprocal rank fusion: combine rankings by position, not by raw score."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, name in enumerate(ranking, start=1):
            scores[name] = scores.get(name, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: -x[1])


if __name__ == "__main__":
    for query in ["NCS-2025-0142", "contract reference NCS-2025-0142 auto renewal"]:
        print(f"\nQuery: {query!r}")
        for name, score in rrf([bm25_rank(query)]):
            print(f"  {score:.5f}  {name}")
