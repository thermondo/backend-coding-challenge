from datetime import datetime
from time import time
from typing import Optional


def make_timestamp(dt: Optional[datetime] = None) -> int:
	epoch = time() if dt is None else dt.timestamp()
	milliseconds = int(epoch * 1000)

	return milliseconds


def from_timestamp(timestamp: int) -> datetime:
	epoch = timestamp / 1000.0
	return datetime.fromtimestamp(epoch)
