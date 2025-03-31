from fastapi import UploadFile, File, HTTPException
from typing import List, Optional


class FileValidator:
    EXTENSION_CONTENT_TYPE_MAP = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    def __init__(self, allowed_extensions: Optional[set[str]] = None, max_size_mb: int = 2, count: int = 1):
        if not allowed_extensions:
            raise HTTPException(status_code=400, detail="Не указаны форматы файлов для загрузки")

        unknown_ext = allowed_extensions - set(self.EXTENSION_CONTENT_TYPE_MAP.keys())
        if unknown_ext:
            raise HTTPException(status_code=400, detail=f"Неподдерживаемые расширения: {', '.join(sorted(unknown_ext))})")

        self.max_size = max_size_mb * 1024 * 1024
        self.count = count
        self.allowed_extensions = allowed_extensions
        self.allowed_content_types = {
            self.EXTENSION_CONTENT_TYPE_MAP[ext]
            for ext in self.allowed_extensions
        }

    async def __call__(self, files: List[UploadFile] = File(...)) -> List[UploadFile]:
        if len(files) > self.count:
            raise HTTPException(status_code=400, detail=f"Максимум можно загрузить {self.count} файлов за раз")

        for file in files:
            ext = file.filename.split(".")[-1].lower()

            if ext not in self.allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"Формат файла .{ext} не разрешён. Разрешены: {', '.join(sorted(self.allowed_extensions))}"
                )

            if file.content_type not in self.allowed_content_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Тип файла {file.content_type} не разрешён. Разрешены: {', '.join(sorted(self.allowed_content_types))}"
                )

            contents = await file.read()
            if len(contents) > self.max_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"Файл {file.filename} слишком большой. Максимальный размер — {self.max_size // (1024 * 1024)}MB"
                )

            file.file.seek(0)

        return files
