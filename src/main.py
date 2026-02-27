from dotenv import load_dotenv
import os
load_dotenv()  

HF_TOKEN = os.getenv("HF_TOKEN")

from dotenv import load_dotenv
load_dotenv()

from src.llm.mail_generator import generate_email
from src.sheets.client import get_todo_rows, mark_done, sheet
from src.mail.sender import send_gmail_without_attachment, send_mail_with_attachment
from src.context.profile import get_resume_path

def main():
    print("GETTING ROWS ....")
    rows = get_todo_rows()
    print("ROWS :\n")
    print(rows)

    #generate send and update status
    for row in rows:

        #generate text
        email_text = generate_email(
            receiver_name=row["receiver_name"],
            role_title=row["role_title"],
            role_description=row["role_description"],
            audience_type=row["audience_type"],
            intent=row['intent'],
            resume_tag=row.get("resume_tag"),
        )
        
        #resume_tag=row.get("resume_tag")

        #resume_path = get_resume_path(resume_tag)

        #send mail
        #if(resume_path):
            #send_mail_with_attachment(email_text,resume_path,row["receiver_mail"],row['subject'])
        #else:
        send_gmail_without_attachment(email_text,row["receiver_email"],row['subject'])
        print("SENT MAIL WITH TEXT : ...\n")
        print(email_text)
        #update status in sheet
        print("UPDATING SHEET....\n")
        mark_done(row["Row ID"], sheet)
        print("SHEET UPDATED...")



if __name__ == "__main__":
    main()