import os

def box_ls(client, folder_id, file_extension, last_modified, pattern=''):
    """Recursively list all files in the specified Box folder"""
    file_list = {}

    folder = client.folder(folder_id=folder_id).get()
    if folder.content_modified_at < last_modified:
        return file_list

    items = client.folder(folder_id=folder_id).get_items()

    for item in items:
        file_info = item.get()
        if file_info.type == "file":
            if file_info.name.endswith(file_extension) and file_info.name.find(pattern) != -1 and file_info.modified_at > last_modified:
                print(f'Reading {file_info.name}')
                file_list[file_info.id] = file_info.name
                continue
        else:
            print(f'---- Entering folder {file_info.name}')
            file_list.update(box_ls(client=client, 
                                    folder_id=file_info.id, 
                                    file_extension=file_extension, 
                                    pattern=pattern, 
                                    last_modified = last_modified))

    return(file_list)

#box_ls(client=client, folder_id=folder_id, file_extension='xlsx', pattern='DivVar', last_modified='2021-05-30')

def box_parse_excel(client, file_id, parsing_func):
    """Parse excel file located in Box"""

    tmp_file = 'temp_file_from_box.xlsx'
    with open(tmp_file, 'wb') as open_file:
        client.file(file_id=file_id).download_to(open_file)

    df = parsing_func(tmp_file)
    os.remove(tmp_file)
    return(df)