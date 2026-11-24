"""Lab 8: route simple questions to Haiku and multi-step questions to Sonnet.

Run: python lab08_router.py
"""
from common import HAIKU, SONNET, get_client, text_of


def classify(client, question: str) -> str:
    resp = client.messages.create(
        model=HAIKU,
        max_tokens=10,
        messages=[{"role": "user", "content": (
            "Answer with one word: SIMPLE for a direct lookup, COMPLEX for multi-step reasoning.\n\n"
            f"Question: {question}")}],
    )
    return text_of(resp).upper()


def route(client, question: str) -> str:
    label = classify(client, question)
    model = HAIKU if "SIMPLE" in label else SONNET
    print(f"[{label} -> {model}]")
    resp = client.messages.create(model=model, max_tokens=400, messages=[{"role": "user", "content": question}])
    return text_of(resp)


if __name__ == "__main__":
    client = get_client()
    print(route(client, "What is the annual value of the Nimbus Cloud Services contract?"))
    print(route(client, "Which combination of cancellations saves the most money while keeping one security vendor?"))
