"""
Models to send requests to Zafira server, will be expand as new client features will occur.
They're using camel-case to send as JSON in request directly
"""
import enum


class TestStatus(enum.Enum):
    UNKNOWN = 'UNKNOWN'
    IN_PROGRESS = 'IN_PROGRESS'
    PASSED = 'PASSED'
    FAILED = 'FAILED'
    SKIPPED = 'SKIPPED'
    ABORTED = 'ABORTED'
    QUEUED = 'QUEUED'


class Initiator(enum.Enum):
    SCHEDULER = 'SCHEDULER'
    UPSTREAM_JOB = 'UPSTREAM_JOB'
    HUMAN = 'HUMAN'


class DriverMode(enum.Enum):
    METHOD_MODE = "METHOD_MODE"
    CLASS_MODE = "CLASS_MODE"
    SUITE_MODE = "SUITE_MODE"
