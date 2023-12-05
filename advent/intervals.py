import pydantic


class Interval(pydantic.BaseModel):
    lo: int
    hi: int
