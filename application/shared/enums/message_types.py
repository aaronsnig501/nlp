from enum import Enum


class MessageTypes(str, Enum):

    REQUEST_RECEIVED = "REQUEST_RECEIVED"
    REQUEST_PROCESSED = "REQUEST_PROCESSED"
