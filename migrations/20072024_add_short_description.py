import sys

sys.path.append("..")

import asyncio
from src.db import get_db_conn


async def main():
    db = await get_db_conn()
    transaction = db.transaction()
    posts = await transaction.execute("SELECT * FROM assignments")
    await transaction.execute("ALTER TABLE assignments ADD COLUMN short_description TEXT")
    for p in posts:
        data = p.asdict()
        await transaction.execute(
            "UPDATE assignments SET short_description = ? WHERE id = ?",
            [data["description"].splitlines()[0], data["id"]],  # type: ignore
        )
    await transaction.commit()


asyncio.run(main())
