# import os
# import imaplib
# import email
# from dotenv import load_dotenv
# from email.header import decode_header
# from dotenv import dotenv_values

# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# env_path = os.path.join(BASE_DIR, ".env")

# print("Exists:", os.path.exists(env_path))
# config = dotenv_values(env_path)
# print(config)

# # 🔹 Force read .env directly from project root
# # BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# # env_path = os.path.join(BASE_DIR, ".env")

# # config = dotenv_values(env_path)

# EMAIL_USER = config.get("EMAIL_USER")
# EMAIL_PASS = config.get("EMAIL_PASS")

# print("ENV PATH:", env_path)
# print("EMAIL_USER:", EMAIL_USER)
# print("EMAIL_PASS:", EMAIL_PASS)
# def fetch_emails(limit=3):
#     if not EMAIL_USER or not EMAIL_PASS:
#         raise ValueError("Email credentials not found in .env")

#     try:
#         mail = imaplib.IMAP4_SSL("imap.gmail.com")
#         mail.login(EMAIL_USER, EMAIL_PASS)
#         mail.select("inbox")

#         status, messages = mail.search(None, "ALL")
#         email_ids = messages[0].split()

#         results = []

#         for num in email_ids[-limit:]:
#             status, data = mail.fetch(num, "(RFC822)")
#             msg = email.message_from_bytes(data[0][1])

#             # Decode subject
#             subject, encoding = decode_header(msg["Subject"])[0]
#             if isinstance(subject, bytes):
#                 subject = subject.decode(encoding if encoding else "utf-8")

#             sender = msg.get("From")
#             date = msg.get("Date")

#             # Extract body
#             body = ""
#             if msg.is_multipart():
#                 for part in msg.walk():
#                     if part.get_content_type() == "text/plain":
#                         body = part.get_payload(decode=True).decode(errors="ignore")
#                         break
#             else:
#                 body = msg.get_payload(decode=True).decode(errors="ignore")

#             results.append({
#                 "source": "Email",
#                 "sender": sender,
#                 "date": date,
#                 "subject": subject,
#                 "content": subject + " " + body
#             })

#         mail.logout()
#         return results

#     except Exception as e:
#         print("Email fetch failed:", e)
#         return []
import os
import imaplib
import email
import re
from dotenv import dotenv_values
from email.header import decode_header

# 🔹 Load .env from project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(BASE_DIR, ".env")
config = dotenv_values(env_path)

EMAIL_USER = config.get("EMAIL_USER")
EMAIL_PASS = config.get("EMAIL_PASS")


# 🔹 Clean email body text
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"http\S+", "", text)        # remove URLs
    text = re.sub(r"<.*?>", "", text)         # remove HTML tags
    text = re.sub(r"\s+", " ", text)          # remove extra spaces/newlines
    return text.strip()


def fetch_emails(limit=5):
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError("Email credentials not found in .env")

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # 🔹 Fetch only UNSEEN emails
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        results = []

        for num in email_ids[-limit:]:
            status, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            # 🔹 Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

            sender = msg.get("From")
            date = msg.get("Date")
            message_id = msg.get("Message-ID")

            # 🔹 Extract body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            body = clean_text(body)

            results.append({
                "source": "Email",
                "message_id": message_id,
                "sender": sender,
                "date": date,
                "subject": subject,
                "body": body,
                "content": f"{subject} {body}"
            })

        mail.logout()
        return results

    except Exception as e:
        print("Email fetch failed:", e)
        return []