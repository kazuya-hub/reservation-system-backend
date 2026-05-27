# 参考: https://fastapi.tiangolo.com/ja/tutorial/security/

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "52cb5216e33ff2bb2f18fec35816f7b9e2842632523884032a5ee024dfacaa41"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
