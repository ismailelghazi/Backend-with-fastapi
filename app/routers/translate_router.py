from fastapi import APIRouter, Depends, HTTPException, Request, status
from .. import schemas, auth, models
from ..utils import hf_client

router = APIRouter(tags=["Translation"])

@router.post("/translate", response_model=schemas.TranslationResponse)
def translate(request: schemas.TranslationRequest, user: models.User = Depends(auth.get_current_user)):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
        
    try:
        translation = hf_client.translate_text(request.text, request.direction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    if isinstance(translation, dict) and translation.get("status") == 503:
         raise HTTPException(status_code=503, detail=translation.get("error"))

    if translation is None:
        raise HTTPException(status_code=502, detail="Translation service unavailable")
        
    return {"translation": translation}
