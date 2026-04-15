import os
import json
import requests

from src.context.profile import BASICS, select_experiences


def build_prompt(
    receiver_name, role_title, role_description,
    audience_type, intent,
    experiences, signals
):
    name = BASICS["name"]
    role = BASICS["role"]
    
    # Default values if missing
    if not audience_type or audience_type.strip() == "":
        audience_type = "engineering/corporate"
    if not intent or intent.strip() == "":
        intent = "internship"
    
    # Serialize experiences to readable text
    exp_text = "\n".join(
        f"- {e.get('summary', '')} (signals: {', '.join(e.get('signals', []))})"
        for e in experiences
    ) if experiences else "No specific experiences provided."
    
    # Active signals as allowed claims
    claims_text = ", ".join(signals) if signals else "general technical competency"

    # Unified prompt with explicit structure
    prompt = f"""<|system|>You write concise, personalized cold emails from a candidate applying to a role.

CRITICAL RULES:
1. You ARE the sender (applicant), NOT representing an organization
2. NEVER use "we", "our team", "we are looking for", or organizational language
3. Output ONLY the email body—no greeting, no sign-off, no preamble
4. Always start "Hi, " and end with line separated "Thank You, 
regards,
Sanya Gupta(8288971449)"
4. Exactly 4–6 sentences
5. Maximum 120 words total
6. Professional, direct, slightly technical tone
7. NO coursework mentions, NO generic skill lists
8. Include ONE sentence mentioning resume is attached

STRUCTURE (mandatory):
1. Introduction: who you are and your current role
2. Fit statement: one sentence showing alignment using YOUR experience
3. Domain relevance: one sentence about the field/role (use concrete signal if available, else generate domain-relevant insight)
4. Clear ask: state the specific intent (internship/research opportunity)
5. Closing: mention resume is attached

SENDER:
- Name: {name}
- Current role: {role}
- Intent: {intent}

RECEIVER:
- Name: {receiver_name}
- Role: {role_title}
- Domain: {role_description}
- Organization type: {audience_type}

SENDER'S RELEVANT EXPERIENCES:
{exp_text}

ALLOWED SIGNAL KEYWORDS (use sparingly, max 1-2):
{claims_text}

Do NOT invent details about the receiver. If no receiver-specific information is available, generate a domain-relevant sentence instead.|<|user|>Write a cold email from {name} (currently {role}) to {receiver_name} ({role_title}) expressing interest in {intent}. Email body only.|<|assistant|>"""

    return prompt


def generate_email(receiver_name, role_title, role_description, audience_type=None, intent=None, resume_tag=None):
    # Default values if missing
    if not audience_type or audience_type.strip() == "":
        audience_type = "engineering/corporate"
    if not intent or intent.strip() == "":
        intent = "internship"
    
    experiences, signals = select_experiences(audience_type, intent, resume_tag)
    
    prompt = build_prompt(
        receiver_name, role_title, role_description,
        audience_type, intent,
        experiences, signals
    )

    # Call Ollama locally
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b-instruct",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
    )
    
    result = response.json()
    return result['response'].strip()