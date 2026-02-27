autooutreachai/
│
├── src/
│   ├── main.py              # entry point / scheduler hook
│   ├── config.py            # env vars, constants, paths
│   │
│   ├── sheets/
│   │   └── client.py        # read/write Google Sheets
│   │
│   ├── context/
│   │   └── profile.py       # your skills, projects, research, facts
│   │
│   ├── llm/
│   │   └── generator.py     # email + subject generation
│   │
│   ├── resume/
│   │   └── selector.py      # choose correct resume PDF
│   │
│   └── mail/
│       └── sender.py        # SMTP / Gmail API
│
├── resumes/
│   ├── research.pdf
│   ├── ml.pdf
│   └── general.pdf
│
├── logs/
│   └── sent.log
│
├── .env                     
├── requirements.txt
├── README.md
└── .gitignore