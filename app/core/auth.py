# 参考: https://fastapi.tiangolo.com/ja/tutorial/security/

from datetime import datetime, timedelta, timezone
import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urlencode

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "52cb5216e33ff2bb2f18fec35816f7b9e2842632523884032a5ee024dfacaa41"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_STARTTLS = os.getenv("SMTP_STARTTLS", "false").lower() == "true"
FRONTEND_VERIFY_URL = os.getenv("FRONTEND_VERIFY_URL", "http://localhost:5173/signup-form")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token_subject(token: str) -> str:
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
	except InvalidTokenError as exc:
		raise ValueError("invalid token") from exc

	subject = payload.get("sub")
	if not isinstance(subject, str) or not subject:
		raise ValueError("invalid token subject")
	return subject


def send_email_verification(email: str, token: str) -> None:
	params = urlencode({"token": token})
	verification_url = f"{FRONTEND_VERIFY_URL}?{params}"
	content = f"30分以内に以下のURLにアクセスして、メールアドレスの確認を行ってください:\n\n{verification_url}"

	message = EmailMessage()
	message["Subject"] = "【予約システム】メールアドレス確認"
	message["From"] = MAIL_FROM
	message["To"] = email
	message.set_content(content)

	try:
		with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
			smtp.ehlo()
			if SMTP_STARTTLS:
				smtp.starttls()
				smtp.ehlo()
			if SMTP_USER and SMTP_PASSWORD:
				smtp.login(SMTP_USER, SMTP_PASSWORD)
			smtp.send_message(message)
	except Exception as exc:
		print(f"failed to send email... verification url: {verification_url}")
		raise RuntimeError("failed to send email") from exc
	