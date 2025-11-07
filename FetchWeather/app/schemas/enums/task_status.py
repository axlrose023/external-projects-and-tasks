from enum import Enum


class TaskStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
