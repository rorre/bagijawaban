import asyncio
from pathlib import Path
import sys
from typing import cast

import frontmatter
from ulid import ULID
from src.db import get_db_conn


async def main():
    if len(sys.argv) != 3:
        return print(f"{sys.argv[0]} <dir> <course_id>")

    db = await get_db_conn()

    for fpath in Path(sys.argv[1]).glob("*.md"):
        with open(fpath, encoding="utf8", errors="ignore") as f:
            post = frontmatter.load(f)

        await db.execute(
            "INSERT INTO assignments (id, name, description, short_description, course_id) VALUES (?, ?, ?, ?)",
            [
                str(ULID()),
                cast(str, post.metadata["title"]),
                post.content,
                cast(str, post.metadata["description"]),
                sys.argv[2],
            ],
        )


asyncio.run(main())
