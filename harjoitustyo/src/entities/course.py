class Course:
    def __init__(
        self,
        course_id,
        code,
        name,
        credits,
        description="",
        is_completed=False,
        is_scheduled=False,
    ):
        self.course_id = course_id
        self.code = code
        self.name = name
        self.credits = credits
        self.description = description
        self.is_completed = is_completed
        self.is_scheduled = is_scheduled
