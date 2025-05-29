import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = os.environ.get("GMAIL_ADDRESS")
receiver = os.environ.get("GMAIL_RECIPIENT")
app_password = os.environ.get("GMAIL_PASSWORD")

