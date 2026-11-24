"""Lab 5b (Module 5): end-to-end RAG over the real course contract files, with citations.

Pipeline
    load .docx -> chunk by field -> add context header -> BM25 index (+ Voyage embeddings if a key is set)
    -> reciprocal rank fusion -> retrieval eval (recall@k) -> Claude answers from the top chunks with citations

Run
    python lab05_rag_end_to_end.py --eval                    # offline: retrieval quality only
    python lab05_rag_end_to_end.py --ask "Which vendor handles security?" --mock
    python lab05_rag_end_to_end.py --ask "Which contracts must be cancelled before September?"   # live

Exercise
    1. Set CONTEXT_HEADERS = False and run --eval. Retrieval still hits, but "answerable" drops:
       the chunk no longer says which vendor it is about. That is the failure contextual retrieval fixes.
    2. Lower K to 1. What happens to recall, and to the answer for a question that spans two contracts?
"""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from common import SONNET, get_client, last_user_text

CONTRACT_DIR = Path(__file__).resolve().parent.parent / "Claude-Platform-Mastery" / "Contracts"
CONTEXT_HEADERS = True
K = 3
VOYAGE_MODEL = os.getenv("VOYAGE_MODEL", "voyage-4")  # check dashboard.voyageai.com for the current model

# Each question names the vendor(s) a correct retrieval must return.
EVAL_SET = [
    ("Which vendor provides endpoint security and vulnerability scanning?", {"BrightPath Security Solutions"}),
    ("What is contract NCS-2025-0142?", {"Nimbus Cloud Services"}),
    ("Who supplies cabling and consumables for the data closet?", {"Alderwood Office Supplies"}),
    ("Which agreement does not auto-renew?", {"Fixed-Term Consulting LLC"}),
    ("Who runs our WAN circuits?", {"Vertex Networking Group"}),
    ("Which vendor hosts our production databases?", {"Nimbus Cloud Services"}),
]


def load_chunks() -> list[dict]:
    """One chunk per contract field, so each chunk is small and self-describing."""
    import docx  # python-docx

    files = sorted(CONTRACT_DIR.glob("Contract_*.docx"))
    if not files:
        raise SystemExit(f"No contract files found in {CONTRACT_DIR}")
    chunks = []
    for path in files:
        doc = docx.Document(path)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        vendor = paras[1] if len(paras) > 1 else path.stem
        pieces = []
        for table in doc.tables:
            for row in table.rows:
                cells = [c.text.strip() for c in row.cells]
                if len(cells) >= 2 and cells[0]:
                    pieces.append(f"{cells[0]}: {cells[1]}")
        pieces += [p for p in paras[2:] if not p.startswith("Note:")]
        for piece in pieces:
            header = f"From the {vendor} service agreement. " if CONTEXT_HEADERS else ""
            chunks.append({"vendor": vendor, "source": path.name, "text": header + piece})
    return chunks


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def rrf(rankings: list[list[int]], k: int = 60) -> list[int]:
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking, start=1):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda i: -scores[i])


class Retriever:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])
        self.vectors = None
        if os.getenv("VOYAGE_API_KEY"):
            import numpy as np
            import voyageai

            self.voyage, self.np = voyageai.Client(), np
            self.vectors = np.array(self.voyage.embed([c["text"] for c in chunks], model=VOYAGE_MODEL, input_type="document").embeddings)

    def search(self, query: str, k: int = K) -> list[dict]:
        scores = self.bm25.get_scores(tokenize(query))
        rankings = [sorted(range(len(self.chunks)), key=lambda i: -scores[i])]
        if self.vectors is not None:
            q = self.np.array(self.voyage.embed([query], model=VOYAGE_MODEL, input_type="query").embeddings[0])
            sims = self.vectors @ q / (self.np.linalg.norm(self.vectors, axis=1) * self.np.linalg.norm(q))
            rankings.append(sorted(range(len(self.chunks)), key=lambda i: -sims[i]))
        return [self.chunks[i] for i in rrf(rankings)[:k]]


def run_eval(retriever: Retriever) -> None:
    mode = "BM25 + embeddings" if retriever.vectors is not None else "BM25 only (set VOYAGE_API_KEY for hybrid)"
    print(f"Retrieval eval | {mode} | k={K} | context headers={CONTEXT_HEADERS}\n")
    hits = answerable = 0
    print("  retrieved  self-describing  question")
    for question, wanted in EVAL_SET:
        top = retriever.search(question)
        found = {c["vendor"] for c in top}
        ok = wanted <= found
        # A chunk only helps the model if its own text says which vendor it is about.
        named = all(any(v in c["text"] for c in top if c["vendor"] == v) for v in wanted)
        hits += ok
        answerable += ok and named
        print(f"  {'HIT ':9}  {'yes' if named else 'NO ':15}  {question}" if ok else f"  {'MISS':9}  {'-':15}  {question}")
    print(f"\nrecall@{K}: {hits}/{len(EVAL_SET)}   answerable from chunk text: {answerable}/{len(EVAL_SET)}")


def ask(retriever: Retriever, question: str) -> None:
    top = retriever.search(question)
    documents = [
        {"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": c["text"]},
         "title": c["source"], "citations": {"enabled": True}}
        for c in top
    ]
    client = get_client(mock_responder)
    resp = client.messages.create(
        model=SONNET,
        max_tokens=600,
        system="Answer only from the provided documents. If they do not contain the answer, say so.",
        messages=[{"role": "user", "content": documents + [{"type": "text", "text": question}]}],
    )
    print(f"Q: {question}\n")
    for block in resp.content:
        if block.type == "text":
            print(block.text, end="")
            for cite in getattr(block, "citations", None) or []:
                print(f" [{cite.document_title}]", end="")
    print("\n\nRetrieved:", ", ".join(c["vendor"] for c in top))


def mock_responder(kw: dict):
    return "Mock answer built from the retrieved documents. " + last_user_text(kw)[:60]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval", action="store_true")
    parser.add_argument("--ask")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()
    retriever = Retriever(load_chunks())
    if args.ask:
        ask(retriever, args.ask)
    else:
        run_eval(retriever)
