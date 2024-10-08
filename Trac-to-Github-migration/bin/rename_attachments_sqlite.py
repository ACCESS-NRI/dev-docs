#!/bin/env python3

from pathlib import Path

import hashlib
import os
import pathlib
import shutil
import sqlite3

def connect_to_database(db_name):
    """
    Connect to an existing database.

    INPUT:

    - ``db_name`` -- string. The name of the existing database.

    OUTPUT: a database connection object.

    """
    if os.path.isfile(db_name):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        raise IOError("File not found: {}".format(db_name))


def rename_attachments(db_name, from_base, to_base):

    conn = connect_to_database(db_name)
    curs = conn.cursor()
    curs.execute("""
        SELECT type, id, filename
        FROM attachment""")
    for row in curs:
        to_type = row["type"]
        to_id = row["id"]
        to_filename = row["filename"]
        to_dir = Path(to_base) / to_type / to_id
        to_path = to_dir / to_filename

        from_type = to_type
        from_id = hashlib.sha1(to_id.encode("utf-8")).hexdigest()
        from_id_prefix = from_id[:3]
        from_filename = hashlib.sha1(to_filename.encode("utf-8")).hexdigest()
        extension = Path(to_filename).suffix
        from_path = Path(from_base) / from_type / from_id_prefix / from_id / (from_filename + extension)
        if from_path.is_file():
            to_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(from_path, to_path)
            if to_path.is_file():
                print("Success:", from_path, "->", to_path)
            else:
                print("Failure:", from_path, "->", to_path)
                exit(1)

if __name__ == "__main__":
    rename_attachments("db/trac.db", "files/attachments", "files/raw")


