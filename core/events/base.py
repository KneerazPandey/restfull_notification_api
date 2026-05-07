from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4


@dataclass(frozen=True, kw_only=True)
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occured_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_name: str = "base.event"