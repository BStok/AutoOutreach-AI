
# AutoOutreach-AI

AutoOutreach-AI is an automated outreach pipeline that generates and sends
context-aware, personalized emails to professors and hiring managers.

The system uses a **Google Sheet as the control plane**. Contacts, metadata,
and outreach status are managed in the sheet, while the pipeline decides:

• what email to generate  
• what resume to attach  
• when to send it  

This converts manual cold emailing into a **structured automation workflow**.

---

## Features

- Personalized email generation using an LLM
- Targeted outreach (professors / recruiters / hiring managers)
- Automatic resume selection based on role or domain
- Google Sheets–driven workflow
- Email delivery via **Gmail API**
- Outreach logging and status tracking
- Duplicate-send safeguards

---

## Architecture

Google Sheets → Contact + metadata source  
LLM Engine → Generates email content  
Resume Selector → Chooses correct resume version  
Gmail API → Sends emails  

Updating the sheet automatically changes the pipeline's behavior.

---

## Setup

Because the system interacts with Google services, users must configure their
own credentials.

### 1. Clone the repository

    git clone https://github.com/Bstok/AutoOutreach-AI  
    cd AutoOutreach-AI

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Create Google Cloud credentials

1. Go to Google Cloud Console  
2. Create a project  
3. Enable:
   - Google Sheets API
   - Gmail API
4. Create OAuth credentials
5. Download the `credentials.json` file

Place `credentials.json` in the project root.

---

### 4. Configure the Google Sheet

Create a sheet with columns similar to:

Name | Organization | Role | Email | Category | Resume_Tag | Status | Notes

The pipeline reads rows marked for outreach with Status = 'To Do'.

---

### 5. Run the pipeline

    python src/main.py

The system will:

1. Fetch contacts from the sheet  
2. Generate personalized emails  
3. Select the appropriate resume  
4. Send the email using Gmail API  
5. Update the outreach status

---

## Status

Functional system requiring local API credential configuration.
