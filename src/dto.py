from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: list | None = None
    # status: int = 200
    # error: str | None = None
