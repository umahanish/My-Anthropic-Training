import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


def extract_docx_text(path: Path) -> str:
    with ZipFile(path) as document:
        xml = document.read("word/document.xml")

    root = ET.fromstring(xml)
    word_namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs = []
    for paragraph in root.iter(f"{word_namespace}p"):
        parts = []
        for element in paragraph.iter():
            if element.tag == f"{word_namespace}t":
                parts.append(element.text or "")
            elif element.tag in (f"{word_namespace}tab", f"{word_namespace}br"):
                parts.append("\n" if element.tag.endswith("br") else "\t")
        paragraphs.append("".join(parts))
    return "\n".join(paragraphs).strip()


dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError(
        f"ANTHROPIC_API_KEY is not set. Add it to {dotenv_path} or the environment."
    )

client = Anthropic(api_key=api_key)

contract_path = Path(__file__).resolve().with_name("Contract_Nimbus_Cloud_Services.docx")
contract_text = extract_docx_text(contract_path)
if not contract_text:
    raise ValueError(f"No text could be extracted from {contract_path}.")

response = client.messages.create(
    model="claude-sonnet-5.5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": f"Summarize this contract in two sentences:\n\n{contract_text}",
    }],
)
print(next(b.text for b in response.content if b.type == "text"))