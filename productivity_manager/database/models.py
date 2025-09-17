from dataclasses import dataclass
from typing import Optional


@dataclass
class Todo:
    id: Optional[int]
    title: str
    description: str = ""
    priority: str = "Medium"  # High/Medium/Low
    category: str = "General"
    due_date: Optional[str] = None  # ISO string
    completed: bool = False


@dataclass
class TimeEntry:
    id: Optional[int]
    task_id: Optional[int]
    start_time: str  # ISO string
    end_time: str  # ISO string
    duration_seconds: int
    notes: str = ""

