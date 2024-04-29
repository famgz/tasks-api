from pathlib import Path
from time import sleep
import os
import json


def json_(path,
          new='__null__',
          backup: bool = False,
          n_backups: int = 1,
          indent=None,
          sort_keys: bool = False,
          read_tries: int = 5,
          read_encoding='utf-8-sig',
          write_encoding='utf-8',
          ensure_ascii=True,
          create_file=False,
          ):
    '''
    Generic JSON assistant.
    Read/write JSON data based on `new`.
    TODO: add update parameter to append information
    '''
    file_path = Path(path).resolve()
    file_existed = True
    _null = old = '__null__'

    # file does not exist
    if not file_path.exists():
        file_existed = False
        print(
            f'[bright_black]\[json_]file does not exists: {file_path}{" creating it..." if create_file or new is not _null else ""}')
        if create_file and new is _null:
            # create file with empty dict {}
            with open(file_path, 'w', encoding=write_encoding) as f:
                json.dump({}, f)

    if file_existed:
        # file path is invalid, likely a folder
        if not file_path.is_file():
            print(f'[yellow]Invalid file path: {file_path}')
            return False

        # read file
        for i in range(read_tries):
            if not os.access(file_path, os.R_OK):
                print(f'[bright_black]Cannot access file ({i}): {file_path}')
                sleep(.1)
                continue
            try:
                with open(file_path, 'r', encoding=read_encoding) as f:
                    old = json.load(f)
                break
            except (PermissionError, FileNotFoundError) as e:
                print(e, file_path)
            except json.decoder.JSONDecodeError as e:
                print(e, file_path)

    '''READ MODE'''
    # returns data if exists or empty dict
    if new is _null:
        return old if old is not _null else {}

    # abort write if no changes
    if new == old:
        return False

    # validate new
    assert new not in (None, False, True), f'Invalid data to write: {new}'

    '''WRITE MODE'''
    # check if JSON serializable
    _ = json.dumps(new)

    # backup if file exists
    if backup and (old is not _null):
        import shutil
        saved = False
        folderpath = file_path.parent
        filename = file_path.name
        checks = range(1, max(n_backups+1, 2))
        # search for available .bak slot
        for i in checks:
            suffix = '' if i == 1 else f'({i})'
            bak_path = f'{file_path}{suffix}.bak'
            if not os.path.isfile(bak_path):
                shutil.move(file_path, bak_path)
                saved = True
                break
        # no .bak slot available to overwrite, fallback to older file
        if not saved:
            files = [file for file in folderpath.iterdir(
            ) if file.is_file() and file.name.startswith(filename)]
            files.sort(key=lambda x: x.stat().st_mtime)
            bak_path = files[0]
            shutil.move(file_path, bak_path)
            saved = True

    # use loop to avoid keyboard interrupt corruption (can also be done with "signal"?)
    # TODO: add update implementation
    # content = old.update(new) for dicts / old.append(new) for lists
    while True:
        try:
            # write data
            with open(file_path, 'w', encoding=write_encoding) as f:
                json.dump(new, f, indent=indent, sort_keys=sort_keys,
                          ensure_ascii=ensure_ascii)  # indent=0 creates new lines
            return True
        except KeyboardInterrupt:
            pass
