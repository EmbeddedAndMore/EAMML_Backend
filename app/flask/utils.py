from __future__ import annotations


def allow_upload(file_name: str, allowed_extensions: list[str]) -> bool:
    cond1 = "." in file_name
    cond2 = file_name.split(".")[-1].lower() in allowed_extensions
    return cond1 and cond2
