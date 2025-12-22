import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

if not os.getenv("GROQ_API_KEY"):
    raise EnvironmentError(
        "GROQ_API_KEY not found in environment variables."
    )

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0
)

SYSTEM_PROMPT = SystemMessage(content="""
You are a Senior Digital Marketing Strategist and SEO Specialist.

For every user input, generate a COMPLETE digital marketing content package.

Output format (mandatory):

SEO_TITLE:
META_DESCRIPTION:
FOCUS_KEYWORD:
SECONDARY_KEYWORDS:
HASHTAGS:
CTA:
CONTENT_SNIPPET:

Rules:
- SEO title max 60 characters
- Meta description max 155 characters
- Use persuasive and conversion-focused language
- Never ask questions back to the user
""")

def generate_marketing_content(user_prompt: str) -> str:
    messages = [
        SYSTEM_PROMPT,
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)
    return response.content

