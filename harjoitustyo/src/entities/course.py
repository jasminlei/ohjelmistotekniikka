from dataclasses import dataclass


@dataclass
class Course:
    course_id: int
    user_id: int
    code: str
    name: str
    credits: int
    description: str = ""
    is_completed: bool = False
    grade: int = None
    completion_date: int = None
