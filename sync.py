import os
from concurrent.futures import ThreadPoolExecutor, as_completed

executor = ThreadPoolExecutor()
tasks = []


def download(item, path):
    if not os.path.exists(path) or os.path.getsize(path) != item.size:
        file = item.open(stream=True)
        with open(path, "wb") as opened_file:
            opened_file.write(file.raw.read())


def create_folder(base_path, path):
    current_path = base_path
    for folder_name in path:
        current_path = os.path.join(current_path, folder_name)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
    return current_path


def iterate(src_folder, local_base_path, path=[]):
    items = src_folder.dir()

    for item in items:
        current_item = src_folder[item]

        if current_item.type == "folder":
            new_path = path + [current_item.name]

            create_folder(local_base_path, new_path)

            iterate(current_item, local_base_path, new_path)
        else:
            if current_item.dir() is None:
                try:
                    download_path = os.path.join(local_base_path, *path, current_item.name)
                    print(download_path)
                    task = executor.submit(download, current_item, download_path)
                    tasks.append(task)
                except:
                    pass


def sync(api, location):
    src_root_folder = api.drive

    if not os.path.exists(location):
        os.makedirs(location)

    print("started sync")
    iterate(src_root_folder, location)

    for future in as_completed(tasks):
        try:
            future.result()
        except Exception as e:
            print(f"sync error: {e}")

    print("sync complete")
