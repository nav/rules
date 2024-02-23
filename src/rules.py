import enum
import typing
from pydantic import BaseModel
import rule_engine
import entities


class Operator(enum.Enum):
    OR = "or"
    AND = "and"
    EQUAL = "=="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="


class Rule(rule_engine.Rule):
    def __init__(self, text, reason=None, context=None):
        self.reason = reason
        super().__init__(text, context)

    def matches(self, thing):
        result = self.evaluate(thing)
        return result, self.reason
