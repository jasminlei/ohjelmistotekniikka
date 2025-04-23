from dataclasses import dataclass


@dataclass
class StudyPlan:
    plan_id: int
    plan_name: str
    user_id: int
    goal_credits: int
