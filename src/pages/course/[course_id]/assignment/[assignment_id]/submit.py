from likulau.hooks import use_request

from starlette.exceptions import HTTPException
from starlette.datastructures import UploadFile
from types_aiobotocore_s3 import S3Client

from likulau.env import env
from likulau.routes import methods
from ulid import ULID
from src.providers.auth import use_current_user
from src.db import get_db_conn
from src.s3 import s3_client
from src.utils import random_str
from starlette.responses import RedirectResponse

MAX_UPLOAD = 8 * 1024 * 1024


@methods(["POST"])
async def page():
    request = use_request()
    current_user = use_current_user()

    if not current_user:
        return RedirectResponse("/auth/login", 302)

    async with request.form(max_files=1, max_fields=2) as form:
        notes = form.get("notes", "")
        f = form.get("file")
        if not (isinstance(f, UploadFile) and isinstance(notes, str)):
            raise HTTPException(400, "Invalid data")

        if f.content_type not in ("application/pdf", "application/zip", "application/x-zip-compressed") and (
            not f.filename or not any(f.filename.endswith(x) for x in (".pdf", ".zip", ".py", ".java"))
        ):
            raise HTTPException(400, "Invalid file")

        if f.size and f.size > MAX_UPLOAD:
            raise HTTPException(400, "File too big")

        path = f"submissions/{random_str(8)}_{f.filename}"
        async with s3_client() as client:
            client: S3Client
            await client.put_object(Bucket=env("BUCKET_NAME"), Key=path, Body=f.file)

    db = await get_db_conn()
    await db.execute(
        "INSERT INTO submissions (id, url, notes, user_id, assignment_id) VALUES (?, ?, ?, ?, ?)",
        (str(ULID()), env("S3_BUCKET_URL") + path, notes, request.session["id"], request.path_params["assignment_id"]),
    )

    return RedirectResponse("./", status_code=302)
