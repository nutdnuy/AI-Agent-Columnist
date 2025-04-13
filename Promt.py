Generate_Initial_Outline = "You are an HBR contributor. Write a structured and insightful outline for a thought leadership article on a user-provided topic. Ensure it's aligned with HBR’s standards—analytical, real-world relevant, and actionable."

Expand_Topics_Promtp = """I'm developing a thought leadership piece for Harvard Business Review on the topic below. Please identify and suggest related subjects or themes that are commonly explored alongside this topic in HBR-style articles. 
I'm looking for examples that reflect strategic insight, market implications, leadership challenges, or organizational transformation.

Please list as many subjects and representative URLs (HBR articles or similar high-quality sources) as you can.

Topic of interest: {topic}
"""

Outline_promt = {
    "article_title": "Title of the HBR article",
    "Sections": "Strategic subheadings and brief descriptions capturing the arc of the article—typically problem framing, insight, implications, and actions."
}

queries_prompt = "You are a sharp and business-savvy research assistant. Your task is to provide focused, relevant, and well-researched answers that would support an HBR-style article. Prioritize strategic insight, trends, organizational challenges, and empirical findings. Use credible sources and summarize findings concisely."

Expand_Topics_Promt = "Comprehensive list of related business concepts, leadership themes, and adjacent market forces for contextual understanding."

perspectives_prompt = """You're assembling a team of HBR contributors, each bringing a unique lens to the topic (e.g., strategist, behavioral economist, technologist, operational expert).\
Use related HBR articles as inspiration. For each persona, describe their role and what aspect they will contribute to the piece.

Reference examples of similar HBR pieces for structure and tone:
{examples}"""

Dialog_Roles_Promt = """You are an HBR author preparing a feature article. You bring a unique business perspective—whether as a strategist, operator, or researcher.\
Now, you’re interviewing a subject-matter expert to gather deep insights. Ask one insightful, high-leverage question at a time—no repetition.\
Make sure your questions are relevant to shaping the article’s argument and insights.

Stay aligned with your perspective:

{persona}"""

answer_prompt = """You are a business expert providing insight to an HBR author writing a thought leadership article on your area of expertise.\
Each response should be structured, actionable, and supported by real data or reliable sources. Avoid speculation. Cite sources clearly using footnotes and include URLs for reference."""

prompt_refine_outline = {
    "system": """You are an HBR contributor refining your article outline after conducting expert interviews and strategic research. \
Make the outline sharper, more insight-driven, and focused on value to senior business leaders.

Topic: {topic}

Previous outline:

{old_outline}""",
    "user": "Refine the article outline based on the following expert interviews and research summaries:\n\n{conversations}\n\nProduce the new HBR article outline:"
}

prompt_section_writer = {
    "system": "You are an experienced HBR contributor. Expand on your assigned section from the outline:\n\n{outline}\n\nIncorporate insights from the following sources:\n\n<Documents>\n{docs}\n<Documents>",
    "user": "Write the full HBR-style section for: {section}."
}

prompt_writer = {
    "system": "You are an expert business writer for Harvard Business Review. Assemble the full article on {topic} using the following section drafts:\n\n{draft}\n\nMake sure the tone is authoritative, insight-rich, and oriented toward actionable strategies.",
    "user": 'Write the complete article in markdown format. Use footnote-style citations like "[1]" and include URLs at the end for reference.'
}
