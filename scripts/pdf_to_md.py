import sys

sys.path.append(".")
sys.path.append("..")

import asyncio
from pathlib import Path


from likulau.env import env

from src.s3 import upload_file

MD_TEMPLATE = """
---
title: TODO
description: TODO
---

<iframe src="{url}" width="100%" height="720px">
"""


async def main():
    if len(sys.argv) != 3:
        return print(f"{sys.argv[0]} <dir> <prefix>")

    for fpath in Path(sys.argv[1]).glob("**/*.pdf"):
        print(">", fpath)
        path = sys.argv[2] + "/" + fpath.name
        with open(fpath, "rb") as f:
            await upload_file(path, f)

        url = env("S3_BUCKET_URL") + path
        with open(fpath.with_suffix(".md"), "w") as fw:
            fw.write(MD_TEMPLATE.format({"url": url}))


asyncio.run(main())
