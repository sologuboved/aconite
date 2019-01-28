from basic_operations import load_utf_json, dump_utf_json
from global_vars import *


def add_fields(source_json, target_json=None, **fields):
    if not target_json:
        target_json = source_json
    entries = load_utf_json(source_json)
    total = len(entries)
    count = 0
    for entry in entries:
        count += 1
        print("\r{} / {}".format(count, total), end='', flush=True)
        for fieldname, val in fields.items():
            entry[fieldname] = val
    print("\nDumping...")
    dump_utf_json(entries, target_json)


if __name__ == '__main__':
    add_fields(LJ_POEMS_JSON, **{ORIGINAL_BY: str(), ORIGINAL_LANG: str()})
