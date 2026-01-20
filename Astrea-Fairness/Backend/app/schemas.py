# Reserved for future validation schemas (Pydantic)
from pydantic import BaseModel

class DatasetAuditParams(BaseModel):
    sensitive: str
    y_true: str
    y_pred: str
