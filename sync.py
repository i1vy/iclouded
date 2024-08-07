import os
from concurrent.futures import ThreadPoolExecutor, as_completed

executor = ThreadPoolExecutor()
tasks = []
files = []
filestodownload = []


def download(item, path, iclouded_path):
    if not os.path.exists(path) or os.path.getsize(path) != item.size:
        file = item.open(stream=True)
        print("\t" + item.name)
        with open(path, "wb") as opened_file:
            opened_file.write(file.raw.read())


def downloadall(iclouded_path):
    for filey in filestodownload:
        file = filey[0]
        loc = filey[1]
        download_path = os.path.join(iclouded_path, loc, file.name)
        task = executor.submit(download, file, download_path, iclouded_path)
        tasks.append(task)


filelist = []


def list_files_recursive(path):
    global filelist
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            filelist.append(full_path)


def path2icloudpy(path, drive):
    parts = path.split('/')[:-1]
    element = drive

    for part in parts:
        try:
            element = element[part]
        except KeyError:
            print(f"folder {part} doesnt exist in icloud, you have to make it yourself first")
            element = None
            break

    return element


def upload(iclouded_location, api):
    global filelist
    filelist = []
    list_files_recursive(iclouded_location)
    for file in filelist:
        # hell
        icloudedfile = file.replace(iclouded_location, "")[1:]
        if icloudedfile not in files:
            print("\t" + icloudedfile)
            meow = path2icloudpy(icloudedfile, api.drive)
            with open(file, "rb") as file:
                meow.upload(file)


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
                    iclouded_path = os.path.join(*path, current_item.name)
                    files.append(iclouded_path)
                    filestodownload.append([current_item, os.path.join(*path)])
                except:
                    pass


def sync(api, location):
    src_root_folder = api.drive

    if not os.path.exists(location):
        os.makedirs(location)

    print("started sync")
    iterate(src_root_folder, location)
    print("uploading:")
    upload(location, api)
    print("downloading:")
    downloadall(location)

    for future in as_completed(tasks):
        try:
            future.result()
        except Exception as e:
            print(f"sync error: {e}")

    print("sync complete")
