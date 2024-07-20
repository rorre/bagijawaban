from typing import Type, overload
import libsql_client as libsql

from likulau.env import env

conn: "libsql.Client | None" = None


async def get_db_conn():
    global conn
    if not conn:
        conn = libsql.create_client(url=env("DATABASE_URL"), auth_token=env("DATABASE_AUTH_TOKEN"))
    return conn


async def setup_database():
    conn = await get_db_conn()
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            npm INT PRIMARY KEY,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE
        );
        """
    )

    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
        """
    )

    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            short_description TEXT,
            description TEXT,
            course_id TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        """
    )

    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            notes TEXT,
            user_id INT,
            assignment_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users(npm),
            FOREIGN KEY (assignment_id) REFERENCES assignments(id)
        );
        """
    )


@overload
async def query[T](query: str, args: libsql.InArgs = None) -> libsql.ResultSet: ...


@overload
async def query[T](query: str, args: libsql.InArgs = None, cls: Type[T] = ...) -> list[T]: ...


async def query[T](query: str, args: libsql.InArgs = None, cls: Type[T] | None = None) -> list[T] | libsql.ResultSet:  # type: ignore
    db = await get_db_conn()
    result = await db.execute(query, args)
    if cls:
        return list(map(lambda record: cls(**record.asdict()), result))
    return result
