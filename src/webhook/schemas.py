from pydantic import BaseModel


class WhRecordCreateSchema(BaseModel):
    repo_id: int
    webhook_id: int
    secret: str