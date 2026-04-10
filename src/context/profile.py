BASICS = {
  "name": "Sanya Gupta",
  "role": "Pre Final-year IT student",
  "core_skills": ["Python", "ML", "Backend"],
  "interests": ["Applied ML", "Research", "Systems"]
}



EXPERIENCES = [
    #DIC
    {
    "id": "ml_research",
    "type": "internship",
    "skills": ["ML","DL", "PyTorch"],
    "summary": "Developed deep learning models for cranial implant generation at a healthcare startup, focusing on medical image segmentation.",
    "signals": ["research","ml"]
    },

  #AISOC
    {
    "id": "aisoc_yolo",
    "type": "project",
    "summary": "Developed a real-time vehicle detection and classification system for low-light conditions using deep learning.",
    "skills": ["python", "deep learning", "computer vision"],
    "details": ["yolo", "dataset augmentation", "low-light preprocessing"],
    "signals": ["ml", "computer_vision", "production"]
    },

    #ET-AL 
    {
    "id": "citecraft_research_intelligence",
    "type": "project",
    "summary": "Built a full-stack research intelligence platform that aggregates papers from 5 academic sources, parses PDFs via a RAG pipeline, and generates structured multi-paper comparisons using LLMs.",
    "skills": ["python", "fastapi", "postgresql", "react", "typescript", "nlp", "information_retrieval"],
    "details": [
        "multi-source paper aggregation (arXiv, PubMed, bioRxiv, CORE, Google Scholar)",
        "semantic PDF chunking with section detection",
        "allenai/specter embeddings for scientific text",
        "cosine similarity retrieval over per-user vector store",
        "RAG pipeline with Qwen2.5-72B for dimension-aware comparison",
        "JWT auth with FastAPI + PostgreSQL",
        "deployed on Railway (backend) and Vercel (frontend)"
    ],
    "signals": ["research", "nlp", "systems", "fullstack", "information_retrieval", "rag"]
    },

    #AutoOutreach 
    {
    "id": "autooutreach",
    "type": "project",
    "summary": "Built an automation system for personalized cold email outreach, integrating structured profiles, resume selection, and LLM-based text generation.",
    "skills": ["python", "automation", "llm_integration"],
    "details": [
        "google sheets api",
        "gmail api ",
        "context-based prompt generation",
        "resume selection logic"
    ],
    "signals": ["systems", "automation", "ownership"]
    },

    #Agent KDG
    {
    "id": "group_ci_cd_automation",
    "type": "project",
    "summary": "Implemented automated containerized deployment for a collaborative web application, handling build and server deployment workflows.",
    "skills": ["python", "docker", "deployment"],
    "details": [
        "dockerfile generation from project structure",
        "docker hub integration",
        "github-based workflow",
        "server deployment"
    ],
    "signals": ["systems", "backend", "automation"]
    }
]

INTENT_SIGNAL_PRIORITY = {
  "internship": ["learning", "breadth", "production"],
  "fulltime": ["ownership", "depth", "production"],
  "research": ["research", "theory", "experimentation"]
}

TONE = {
  "hr": {"formality": 0.8, "technical": 0.2},
  "engineer": {"formality": 0.4, "technical": 0.8},
  "professor": {"curiosity": 0.9, "sales": 0.1}
}

TARGET_PROFILES = {
  "research_intern": {
    "prioritize": ["research", "ml", "math"],
    "tone": "curious, academic"
  },
  "startup_backend": {
    "prioritize": ["production", "ownership"],
    "tone": "practical, fast-moving"
  }
}

EXTRAS = [
  {"tag": "leadership", "content": "..."},
  {"tag": "sports", "content": "..."}
]

#must not be included
ANTI_PATTERNS = {
  "professor": ["hiring", "job ask"],
  "startup": ["coursework", "grades"]
}

RESUME = {
    "research": r"C:\Users\projects\AutoOutreach-AI\resumes\Sanya_Gupta-CVR.pdf",
    "internship": r"C:\Users\projects\AutoOutreach-AI\resumes\Sanya_Gupta-CVD.pdf"
}

def get_resume_path(id):
    """
    intent: exact keyword from Google Sheet e.g. "Research", "Internship"
    returns: file path string or None
    """
    if(id == 2): 
        return RESUME["research"]
    else:
        return RESUME["internship"]
    




def select_experiences(audience_type, intent, resume_tag):
    """
    audience_type: key from TARGET_PROFILES e.g. "research_intern", "startup_backend"
    intent: key from INTENT_SIGNAL_PRIORITY e.g. "internship", "research"
    resume_tag: optional extra tag to include e.g. "leadership"
    
    returns: (list of selected experience dicts, list of active signals)
    """

    # 1. Build the signal priority set for this context
    intent_signals = set(INTENT_SIGNAL_PRIORITY.get(intent, []))
    
    profile = TARGET_PROFILES.get(audience_type, {})
    profile_signals = set(profile.get("prioritize", []))
    
    priority_signals = intent_signals | profile_signals  # union of both

    # 2. Score each experience by how many priority signals it matches
    scored = []
    for exp in EXPERIENCES:
        exp_signals = set(exp.get("signals", []))
        score = len(exp_signals & priority_signals)  # intersection count
        if score > 0:
            scored.append((score, exp))

    # 3. Sort by score descending, take top 2-3
    scored.sort(key=lambda x: x[0], reverse=True)
    selected_experiences = [exp for _, exp in scored[:3]]

    # 4. Collect all active signals from selected experiences
    active_signals = list(
        {sig for exp in selected_experiences for sig in exp.get("signals", [])}
    )

    

    return selected_experiences, active_signals



