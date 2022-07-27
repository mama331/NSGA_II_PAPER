import os
def find_all_file_excel(path):
    # path = "/home/toanvd/Documents"
    all_forders = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isdir(os.path.join(path, f))
    ]
    all_files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]
    while len(all_forders) > 0:
        path = all_forders.pop(0)
        foders = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.isdir(os.path.join(path, f))
        ]
        files = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
        all_forders.extend(foders)
        all_files.extend(files)
    # file_excels = [i for i in all_files if '.xlsx' in i or '.xls' in i ]
    return all_files