from dataclasses import dataclass


@dataclass
class User:
    npm: int
    username: str
    name: str
    is_admin: bool


@dataclass
class Course:
    id: str
    name: str


@dataclass
class Assignment:
    id: str
    name: str
    short_description: str
    description: str
    course_id: str


@dataclass
class Submission:
    id: str
    url: str
    notes: str
    user_id: int
