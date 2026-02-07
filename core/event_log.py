from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Event:
    type: str
    data: Dict[str, Any] = field(default_factory=dict)


class EventLog:
    def __init__(self):
        self.events: List[Event] = list()

    def push(self, event_type: str, **data):
        self.events.append(Event(event_type, data))

    def extend(self, events: List[Event]):
        self.events.extend(events)

    def flush(self) -> List[Event]:
        out = self.events
        self.events = list()
        return out