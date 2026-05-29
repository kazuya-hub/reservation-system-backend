
from datetime import datetime

from sqlmodel import SQLModel, Field


class EmailVerificationBase(SQLModel):
	email: str = Field(index=True, unique=True)
	hashed_token: str
	expires_at: datetime


class EmailVerification(EmailVerificationBase, table=True):
	__tablename__ = "t_email_verifications"

	email_verification_id: int | None = Field(default=None, primary_key=True)
	consumed_at: datetime | None = None
