import aiohttp
from fastapi import HTTPException, UploadFile, status
from app.config import settings


DEEPAI_API_URL = "https://api.deepai.org/api/nsfw-detector"
NSFW_LIMIT = 0.7


async def check_nsfw_content(file: UploadFile) -> dict:
    """
    Асинхронно отправляет загруженный файл в DeepAI NSFW API и анализирует результат.

    Args:
        file: Объект UploadFile, полученный от FastAPI.

    Returns:
        Словарь с результатом проверки в формате {"status": "...", "reason": "..."}.

    Raises:
        HTTPException: Если произошла ошибка при запросе к API DeepAI.
    """
    headers = {'api-key': settings.API_KEY}
    
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!{settings.API_KEY}')
    
    form_data = aiohttp.FormData()
    form_data.add_field(
        'image',
        await file.read(),
        filename=file.filename,
        content_type=file.content_type
    )
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(DEEPAI_API_URL, data=form_data, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Ошибка при обращении к DeepAI API: {error_text}"
                    )
                
                result = await response.json()
                print(f'!!!!!!!!!!!!!!!!1{result}')
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Не удалось подключиться к сервису DeepAI: {e}"
        )
    finally:
        await file.close()
    
    nsfw_score = result.get("output", {}).get("nsfw_score")

    if nsfw_score is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось получить nsfw_score из ответа DeepAI."
        )

    if nsfw_score > NSFW_LIMIT:
        return {"status": "REJECTED", "reason": "NSFW content"}
    else:
        return {"status": "OK"}
    
    
