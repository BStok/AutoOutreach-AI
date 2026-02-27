
import os
from openai import OpenAI



from src.context.profile import BASICS, TONE, ANTI_PATTERNS, select_experiences



import json

def build_prompt(
    receiver_name, role_title, role_description,
    audience_type, intent,  # audience_type = org type, intent = research/internship
    experiences, signals
):
    name = BASICS["name"]
    role = BASICS["role"]
    
    # serialize experiences to readable text
    exp_text = "\n".join(
        f"- {e['summary']} (signals: {', '.join(e.get('signals', []))})"
        for e in experiences
    )

    # get tone based on role type (hr / engineer / professor)
    # infer from audience_type as a simple heuristic
    tone_key = "engineer"
    if "professor" in audience_type.lower() or intent == "research":
        tone_key = "professor"
    elif "hr" in role_title.lower():
        tone_key = "hr"
    tone = TONE[tone_key]

    # banned topics
    banned = ANTI_PATTERNS.get(tone_key, [])
    banned_text = ", ".join(banned) if banned else "none"

    # active signals as allowed claims
    claims_text = ", ".join(signals)

    prompt = f"""
You write short, personalized cold emails.
No fluff. No generic praise.
You must obey tone, constraints, and banned topics.
You never mention being an AI.

Sender:
- Name: {name}
- Current role: {role}
- Intent: {intent}

Receiver:
- Name: {receiver_name}
- Role: {role_title}
- Domain: {role_description}
- Organization type: {audience_type}

Goal: Start a conversation, do not ask for a job.

Tone controls:
- Formality: {tone.get('formality', 'n/a')}
- Technical depth: {tone.get('technical', 'n/a')}
- Curiosity: {tone.get('curiosity', 'n/a')}

Banned topics: {banned_text}

Relevant experiences:
{exp_text}

Allowed claims (signal keywords): {claims_text}

Constraints:
- NO coursework mentions
- NO generic skills lists
- NO resume dumping
- NO praise adjectives ("I admire", "impressive", etc.)

Write ONE sentence connecting their domain to one concrete signal from my experience.

Output:
- 4–6 sentences total
- <= 120 words
- Plain text, no emojis
- End with a low-pressure close
"""
    return prompt


#client initialisation
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    )



def generate_email(receiver_name, role_title, role_description, audience_type, intent, resume_tag=None):
    experiences, signals = select_experiences(audience_type, intent, resume_tag)
    prompt = build_prompt(
        receiver_name, role_title, role_description,
        audience_type, intent,
        experiences, signals
    )

    
    completion = client.chat.completions.create(
        model="Nanbeige/Nanbeige4.1-3B:featherless-ai",
        messages=[
            {"role": "system", "content": "You write concise, personalized cold emails. Plain text only."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )

    return completion.choices[0].message.content.strip()




