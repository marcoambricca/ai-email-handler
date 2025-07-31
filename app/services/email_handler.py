from .openai_utils import should_respond_and_generate_reply
from .supabase import log_email
import imaplib, smtplib, email
from email.message import EmailMessage

def fetch_and_reply(customer):
    EMAIL = customer['email']
    PASS = customer['password']
    IMAP_SERVER = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASS)
    mail.select("inbox")

    _, messages = mail.search(None, "UNSEEN")
    ids = messages[0].split()

    for email_id in ids:
        _, data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        from_email = email.utils.parseaddr(msg["From"])[1]
        subject = msg["Subject"]
        date = msg["Date"]

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8")

        if "no-reply" not in from_email:
            should_reply, reply_body = should_respond_and_generate_reply(body)
            if should_reply:
                send_email(EMAIL, PASS, from_email, subject, reply_body)
                log_email(customer["store_name"], from_email, subject, date, body, reply_body)

    mail.logout()

def send_email(from_addr, password, to_addr, subject, body):
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = f"Re: {subject}"
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(from_addr, password)
        smtp.send_message(msg)

