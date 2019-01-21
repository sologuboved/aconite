import json
import time
import csv
import os
import sys
import zipfile
from functools import wraps


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)


def which_watch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, 'took', time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))
        print()
        return result
    return wrapper


def zip_it_up(func):
    @wraps(func)
    def wrapper(filename, *args, **kwargs):
        func(filename, *args, **kwargs)
        print("\nZipping it...")
        zip_filename = '{}.zip'.format(filename.split('.')[0])
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_handler:
            zip_handler.write(filename)
        print("Removing original file...")
        os.remove(filename)
    return wrapper


def write_csv(func):
    @wraps(func)
    def wrapper(csv_filename, is_dict, headers, *args, **kwargs):
        count = 0
        with open(csv_filename, 'w', newline='', encoding='utf-8') as handler:
            if is_dict:
                writer = csv.DictWriter(handler, fieldnames=headers, restval=None)
                writer.writeheader()
            else:
                writer = csv.writer(handler)
                writer.writerow(headers)
            for row in func(csv_filename, is_dict, headers, *args, **kwargs):
                count += 1
                writer.writerow(row)
        print("\nTotal: {} rows".format(count))

    return wrapper


def write_pid():
    pid_fname = '{}_{}.pid'.format(os.path.splitext(os.path.basename(sys.argv[0]))[0], str(os.getpid()))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))
