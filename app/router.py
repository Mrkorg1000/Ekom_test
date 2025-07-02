from fastapi import APIRouter, HTTPException, UploadFile, status

from app.schemas import NSFWCheckResponse
from app.utils import check_nsfw_content


ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png"]


router = APIRouter(
    prefix="/moderate",
    tags=["moderate"],
)

@router.post("", response_model=NSFWCheckResponse)
async def check_image(file: UploadFile):
    """
    Принимает файл изображения (`multipart/form-data`) и проверяет его
    с помощью DeepAI NSFW Detector.

    - **Условие:** Если `nsfw_score > 0.7`, контент считается неприемлемым.
    - **Ограничения:** Принимаются только файлы с `content-type` `image/jpeg` или `image/png`.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Неподдерживаемый тип файла: '{file.content_type}'. Разрешены только {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    result_dict = await check_nsfw_content(file)
    return NSFWCheckResponse(**result_dict)
