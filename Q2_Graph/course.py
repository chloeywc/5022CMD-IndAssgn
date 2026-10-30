"""
Entity class representing a single course offered by the university.
"""


class Course:
    """A university course."""

    LEVELS = ("Core", "Elective")

    def __init__(self, code, name, credit_hours, level, description=""):
        if level not in self.LEVELS:
            raise ValueError(f"level must be one of {self.LEVELS}")
        self.code = code                  # str: unique ID, e.g. "CS201"
        self.name = name                  # str: e.g. "Data Structures"
        self.credit_hours = credit_hours  # int: whole number of credits
        self.level = level                # str: "Core" or "Elective"
        self.description = description    # str: short summary of the course

    def is_core(self):
        return self.level == "Core"

    def __str__(self):
        return f"{self.code} - {self.name}"