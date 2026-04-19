from pydantic import BaseModel

class AiResponseDTO(BaseModel):
    response : str