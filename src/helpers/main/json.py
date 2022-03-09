import json
import os


def get_json_archive_path(path, page_num):
    return f"{path}/pages/{'{:0>6d}'.format(page_num)}/posts.json"


    
def insert_to_json_archive(path, d: dict) -> bool:
    pass
