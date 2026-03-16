
# from fastapi import FastAPI
# from pydantic import BaseModel
# from db import SessionLocal, init_db
# from models import Notification
# from ai_processor import analyze_notification
# from ingest_email import fetch_emails

# app = FastAPI()

# init_db()

# class ManualNotification(BaseModel):
#     source: str
#     sender: str
#     content: str

# @app.get("/")
# def root():
#     return {"message": "AI Notification Assistant Running"}

# @app.post("/ingest/manual")
# def ingest_manual(notification: ManualNotification):
#     db = SessionLocal()

#     ai_result = analyze_notification(notification.content)

#     notif = Notification(
#         source=notification.source,
#         sender=notification.sender,
#         content=notification.content,
#         priority=ai_result["priority"],
#         summary=ai_result["summary"]
#     )

#     db.add(notif)
#     db.commit()
#     db.close()

#     return {
#         "status": "Manual notification processed",
#         "priority": ai_result["priority"],
#         "summary": ai_result["summary"]
#     }

# @app.post("/ingest/email")
# def ingest_email():
#     db = SessionLocal()
#     emails = fetch_emails()

#     for mail in emails:
#         ai_result = analyze_notification(mail["content"])

#         notif = Notification(
#             source=mail["source"],
#             sender=mail["sender"],
#             content=mail["content"],
#             priority=ai_result["priority"],
#             summary=ai_result["summary"]
#         )

#         db.add(notif)

#     db.commit()
#     db.close()

#     return {"status": "Emails processed"}




# from fastapi import FastAPI
# from pydantic import BaseModel
# from db import SessionLocal, init_db
# from models import Notification
# from ai_processor import analyze_notification
# from ingest_email import fetch_emails

# from apscheduler.schedulers.background import BackgroundScheduler

# app = FastAPI()

# init_db()

# class ManualNotification(BaseModel):
#     source: str
#     sender: str
#     content: str


# @app.get("/")
# def root():
#     return {"message": "AI Notification Assistant Running"}


# @app.post("/ingest/manual")
# def ingest_manual(notification: ManualNotification):
#     db = SessionLocal()

#     ai_result = analyze_notification(notification.content)

#     notif = Notification(
#         source=notification.source,
#         sender=notification.sender,
#         content=notification.content,
#         priority=ai_result["priority"],
#         summary=ai_result["summary"]
#     )

#     db.add(notif)
#     db.commit()
#     db.close()

#     return {
#         "status": "Manual notification processed",
#         "priority": ai_result["priority"],
#         "summary": ai_result["summary"]
#     }


# @app.post("/ingest/email")
# def ingest_email():
#     db = SessionLocal()
#     emails = fetch_emails()

#     for mail in emails:
#         ai_result = analyze_notification(mail["content"])

#         notif = Notification(
#             source=mail["source"],
#             sender=mail["sender"],
#             content=mail["content"],
#             priority=ai_result["priority"],
#             summary=ai_result["summary"]
#         )

#         db.add(notif)

#     db.commit()
#     db.close()

#     return {"status": "Emails processed"}


# # ----------- AUTOMATIC EMAIL CHECKER -----------

# def email_job():
#     db = SessionLocal()
#     emails = fetch_emails()

#     for mail in emails:
#         ai_result = analyze_notification(mail["content"])

#         notif = Notification(
#             source=mail["source"],
#             sender=mail["sender"],
#             content=mail["content"],
#             priority=ai_result["priority"],
#             summary=ai_result["summary"]
#         )

#         db.add(notif)

#     db.commit()
#     db.close()

#     print("Emails checked and processed")


# scheduler = BackgroundScheduler()
# scheduler.add_job(email_job, "interval", minutes=2)
# scheduler.start()




from fastapi import FastAPI
from pydantic import BaseModel
from db import SessionLocal, init_db
from models import Notification
from ai_processor import analyze_notification
from ingest_email import fetch_emails

from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

init_db()

class ManualNotification(BaseModel):
    source: str
    sender: str
    content: str


@app.get("/")
def root():
    return {"message": "AI Notification Assistant Running"}


@app.post("/ingest/manual")
def ingest_manual(notification: ManualNotification):
    db = SessionLocal()

    ai_result = analyze_notification(notification.content)

    notif = Notification(
        source=notification.source,
        sender=notification.sender,
        content=notification.content,
        priority=ai_result["priority"],
        summary=ai_result["summary"]
    )

    db.add(notif)
    db.commit()
    db.close()

    return {
        "status": "Manual notification processed",
        "priority": ai_result["priority"],
        "summary": ai_result["summary"]
    }


@app.post("/ingest/email")
def ingest_email():
    db = SessionLocal()
    emails = fetch_emails()

    for mail in emails:
        ai_result = analyze_notification(mail["content"])

        notif = Notification(
            source=mail["source"],
            sender=mail["sender"],
            content=mail["content"],
            priority=ai_result["priority"],
            summary=ai_result["summary"]
        )

        # Prevent duplicate emails
        existing = db.query(Notification).filter(
            Notification.content == mail["content"]
        ).first()

        if not existing:
            db.add(notif)

    db.commit()
    db.close()

    return {"status": "Emails processed"}


# ----------- AUTOMATIC EMAIL CHECKER -----------

def email_job():
    db = SessionLocal()
    emails = fetch_emails()

    for mail in emails:
        ai_result = analyze_notification(mail["content"])

        notif = Notification(
            source=mail["source"],
            sender=mail["sender"],
            content=mail["content"],
            priority=ai_result["priority"],
            summary=ai_result["summary"]
        )

        # Prevent duplicate emails
        existing = db.query(Notification).filter(
            Notification.content == mail["content"]
        ).first()

        if not existing:
            db.add(notif)

    db.commit()
    db.close()

    print("Emails checked and processed")


scheduler = BackgroundScheduler()
scheduler.add_job(email_job, "interval", minutes=2)
scheduler.start()


# ----------- DAILY AI SUMMARY -----------

@app.get("/daily-summary")
def daily_summary():
    db = SessionLocal()

    notifications = db.query(Notification).order_by(
        Notification.created_at.desc()
    ).limit(20).all()

    db.close()

    if not notifications:
        return {"summary": "No notifications today."}

    combined_text = "\n".join([n.content for n in notifications])

    result = analyze_notification(combined_text)

    return {
        "summary": result["summary"]
    }




