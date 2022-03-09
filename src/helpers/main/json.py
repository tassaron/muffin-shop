import json
import os


def get_json_archive_path(path, page_num):
    return f"{path}/pages/{'{:0>6d}'.format(page_num)}/posts.json"


def insert_to_json_archive(path, d: dict) -> bool:
    try:
        with open(path, "r") as f:
            data = json.load(f)
        data.append(d)
        with open(path, "w") as f:
            json.dump(data, f)
        return True
    except Exception:
        return False


def remove_from_json_archive(path, i: int) -> bool:
    try:
        with open(path, "r") as f:
            data = json.load(f)
        del data[i]
        with open(path, "w") as f:
            json.dump(data, f)
        return True
    except Exception:
        return False