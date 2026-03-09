from enum import Enum


class OnFail(str, Enum):
    """OnFail is an Enum that represents the different actions that can
    be taken when a validation fails.

    Attributes:
        REASK (Literal["reask"]): On failure, Reask the LLM.
        FIX (Literal["fix"]): On failure, apply a static fix.
        FILTER (Literal["filter"]): On failure, filter out the invalid values.
        REFRAIN (Literal["refrain"]): On failure, refrain from responding;
            return an empty value.
        NOOP (Literal["noop"]): On failure, do nothing.
        EXCEPTION (Literal["exception"]): On failure, raise a ValidationError.
        FIX_REASK (Literal["fix_reask"]): On failure, apply a static fix,
            check if the fixed value passed validation, if not then reask the LLM.
        CUSTOM (Literal["custom"]): On failure, call a custom function with the
            invalid value and the FailResult's from any validators run on the value.
    """

    REASK = "reask"
    FIX = "fix"
    FILTER = "filter"
    REFRAIN = "refrain"
    NOOP = "noop"
    EXCEPTION = "exception"
    FIX_REASK = "fix_reask"
    CUSTOM = "custom"
