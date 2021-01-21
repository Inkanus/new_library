from app import models

def valid_get(obj):
    val_key = obj.get("sort_key", "id") in ["title", "year", "pages", "id"]
    val_order = obj.get("sort_order", "asc") in ["asc", "desc"]
    return val_key and val_order

def valid_post_put(obj, post=True):
    if post:
        keys = all(x in obj for x in ["title", "authors"])
        default = None
    else:
        keys = True
        default = 0
    val_int = all(
        type(x) is int for x in [
            obj.get("year", default),
            obj.get("pages", default)
        ]
    )
    val_list = "genres" not in obj or len(obj.get("genres", [])) == 3
    val_list2 = "authors" not in obj or len(obj.get("authors", [])) == 3
    return keys and val_int and val_list and val_list2