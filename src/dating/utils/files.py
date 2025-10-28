from fastapi import HTTPException, status, UploadFile
import filetype


def validate_file_size_type(file: UploadFile):
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
    ACCEPTED_FILE_TYPES = {
        "image/png", "image/jpeg", "image/jpg",
        "image/heic", "image/heif", "image/heics",
        "png", "jpeg", "jpg", "heic", "heif", "heics"
    }

    if file.content_type not in ACCEPTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported content type: {file.content_type}",
        )

    file.file.seek(0)
    kind = filetype.guess(file.file)
    file.file.seek(0)

    if kind is None or kind.extension.lower() not in ACCEPTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported or unknown file format",
        )

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large ({size} bytes > {MAX_FILE_SIZE})",
        )
