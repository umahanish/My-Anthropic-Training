from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-5",
    max_tokens=300,
    messages=[{"role": "user", "content": "List 3 things to check before a contract auto-renews."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()
    final = stream.get_final_message()
    print(f"\n\nstop_reason: {final.stop_reason}")