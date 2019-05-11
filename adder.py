from basic_operations import load_utf_json, dump_utf_json


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


def duplicate_entry(source_json, target_json=None, **fields):
    if not target_json:
        target_json = source_json
    entries = load_utf_json(source_json)
    total = len(entries)
    for indx in range(len(entries)):
        count = indx + 1
        entry = entries[indx]
        print("\r{} / {}".format(count, total), end='', flush=True)
        for fieldname, val in fields.items():
            if entry[fieldname] != val:
                break
        else:
            entries.insert(count, entry)
            print("\nFound at {}, inserted at {}!".format(indx, count))
            print("Dumping...")
            dump_utf_json(entries, target_json)
            return
    print("\nNo such entry!")


if __name__ == '__main__':
    # add_fields(LJ_POEMS_JSON, **{IS_SONG: False, IS_DERIVATIVE: False})
    # duplicate_entry(LJ_POEMS_JSON, **{SOURCE: 'https://aconite26.livejournal.com/9632.html'})
    pass
