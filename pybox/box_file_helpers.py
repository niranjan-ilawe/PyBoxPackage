import os, re
from datetime import date
import pandas as pd


def box_ls_window(
    client,
    folder_id,
    file_extension,
    last_modified,
    start_modified,
    pattern="",
    exclude_folder_pattern="@@@",
):
    """Recursively list all files in the specified Box folder

    Parameters:
        client: Box connection client returned by the get_box_client function
        folder_id (str): Box folder id in which recursive search is to be performed
        file_extension (str): extension of files to be searched
        last_modified (date/str): Function returns files newer than this specified date
        start_modified (date/str): Function returns files older than this specified date
        pattern (str): Returns files that match this pattern
        exclude_folder_pattern (str): Folders within the higher folders with this matching pattern are ignored

    Returns:
        file_list: list of all filepaths within the folder

    """
    file_list = {}

    try:
        folder = client.folder(folder_id=folder_id).get()
        if (
            folder.content_modified_at < last_modified
            and folder.content_modified_at > start_modified
        ):
            return file_list
    except:
        return file_list

    items = client.folder(folder_id=folder_id).get_items()

    for item in items:
        file_info = item.get()
        if file_info.type == "file":
            if (
                file_info.name.endswith(file_extension)
                and file_info.name.find(pattern) != -1
                and file_info.modified_at > last_modified
                and file_info.modified_at < start_modified
            ):
                print(f"Reading {file_info.name}")
                file_list[file_info.id] = file_info.name
                continue
        else:
            if re.match(exclude_folder_pattern, file_info.name) != None:
                continue
            else:
                print(f"---- Entering folder {file_info.name}")
                file_list.update(
                    box_ls_window(
                        client=client,
                        folder_id=file_info.id,
                        file_extension=file_extension,
                        pattern=pattern,
                        last_modified=last_modified,
                        exclude_folder_pattern=exclude_folder_pattern,
                        start_modified=start_modified,
                    )
                )

    return file_list


def box_ls(
    client,
    folder_id,
    file_extension,
    last_modified,
    pattern="",
    exclude_folder_pattern="@@@",
):
    """Recursively list all files in the specified Box folder

    Parameters:
        client: Box connection client returned by the get_box_client function
        folder_id (str): Box folder id in which recursive search is to be performed
        file_extension (str): extension of files to be searched
        last_modified (date/str): Function returns files newer than this specified date
        start_modified (date/str): Function returns files older than this specified date
        pattern (str): Returns files that match this pattern
        exclude_folder_pattern (str): Folders within the higher folders with this matching pattern are ignored

    Returns:
        file_list: list of all filepaths within the folder

    """
    file_list = {}

    try:
        folder = client.folder(folder_id=folder_id).get()
        if folder.content_modified_at < last_modified:
            return file_list
    except:
        return file_list

    items = client.folder(folder_id=folder_id).get_items()

    for item in items:
        file_info = item.get()
        if file_info.type == "file":
            if (
                file_info.name.endswith(file_extension)
                and file_info.name.find(pattern) != -1
                and file_info.modified_at > last_modified
            ):
                print(f"Reading {file_info.name}")
                file_list[file_info.id] = file_info.name
                continue
        else:
            if re.match(exclude_folder_pattern, file_info.name) != None:
                continue
            else:
                print(f"---- Entering folder {file_info.name}")
                file_list.update(
                    box_ls(
                        client=client,
                        folder_id=file_info.id,
                        file_extension=file_extension,
                        pattern=pattern,
                        last_modified=last_modified,
                        exclude_folder_pattern=exclude_folder_pattern,
                    )
                )

    return file_list


# box_ls(client=client, folder_id=folder_id, file_extension='xlsx', pattern='DivVar', last_modified='2021-05-30')


def box_read_excel_file(client, file_id, parsing_func, file_name):
    """Parse excel file located in Box

    Parameters:
        client: Box client object returned by the get_box_client function
        file_id (str): Box id of file to be read
        parsing_function (func): Function to be used to read the specified file

    Returns:
        Returns the output of the specified parsing function
    """

    tmp_file = file_name
    with open(tmp_file, "wb") as open_file:
        client.file(file_id=file_id).download_to(open_file)

    df = parsing_func(tmp_file)
    os.remove(tmp_file)
    return df


def box_create_df_from_files(
    box_client,
    last_modified_date,
    box_folder_id,
    file_extension,
    file_pattern,
    file_parsing_functions,
    start_modified_date="",
):
    """Recursively read files in a folder using the provided parsing function and return a combined dataframe

    Parameters:
        box_client: Box connection client returned by the get_box_client function
        last_modified_date (date/str): Function reads files newer than this specified date
        box_folder_id (str): Box folder id in which recursive read is to be performed
        file_extension (str): Only searchs for files with this extension
        file_pattern (str): Only reads files that match this pattern
        file_parsing_functions (func): Function to be used to read the files
        start_modified_date (str): Function reads files older than this specified date (if provided)

    Returns:
        file_list: list of all filepaths within the folder

    """

    if start_modified_date == "":
        # Iteratively search through box folder to find files matching given extension and pattern
        files = box_ls(
            client=box_client,
            folder_id=box_folder_id,
            file_extension=file_extension,
            pattern=file_pattern,
            last_modified=last_modified_date,
        )
    else:
        files = box_ls_window(
            client=box_client,
            folder_id=box_folder_id,
            file_extension=file_extension,
            pattern=file_pattern,
            last_modified=last_modified_date,
            start_modified=start_modified_date,
        )

    total_no_files = len(files)
    print(f"Files found .. {total_no_files}")

    df = pd.DataFrame()
    if total_no_files > 0:
        # Loop through files
        for file_id in files.keys():
            print(f"Parsing file: {files[file_id]}")
            df = df.append(
                box_read_excel_file(
                    client=box_client,
                    file_id=file_id,
                    parsing_func=file_parsing_functions,
                    file_name=files.get(file_id),
                )
            )

    return df
