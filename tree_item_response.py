# Define a Pydantic model for serialization (response model)
from typing import List
from pydantic import BaseModel, ConfigDict, RootModel


class TreeItemResponse(BaseModel):
    id: int
    label: str
    children: List["TreeItemResponse"] = None

    model_config = ConfigDict(
        # Use the same alias for the field name in the JSON response
        json_encoders = {
            "children": lambda v: v if v is not None else []
        },
        # Use the same alias for the field name in the JSON response
        validate_by_name = True        
    )

class Root(RootModel):
    root: List[TreeItemResponse] = None # List of root nodes

    model_config = ConfigDict(
        # Use the same alias for the field name in the JSON response
        json_encoders = {
            "root": lambda v: v if v is not None else []
        },
        # Use the same alias for the field name in the JSON response
        validate_by_name = True        
    )
