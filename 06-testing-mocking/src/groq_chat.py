"""A function that calls an LLM API (Groq). Tests replace the client with a mock."""

from groq import Groq

MODEL = "llama-3.3-70b-versatile"


def ask_groq(question: str, client: Groq = None) -> str:
    """Send a question to Groq and return the answer."""
    if not question.strip():
        raise ValueError("Question cannot be empty")
    client = client or Groq()       # dependency injection: tests pass a fake client
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        max_tokens=1024,
    )
    return response.choices[0].message.content
