from box_authenticate import get_box_client, get_auth_url, save_access_refresh_tokens
from box_file_helpers import box_ls
import tempfile, os

client = get_box_client()

vdj_folder_id = '112736689427'

files = box_ls(client=client, folder_id=vdj_folder_id, file_extension='xlsx', pattern='DivVar', last_modified='2020-01-01')

# loop through file id's


# create temp file
with open('FileFromBox.xlsx', 'wb') as open_file:
    client.file(file_id=file_id).download_to(open_file)



#delete temp file
os.remove("/Users/niranjan.ilawe/Documents/GitHub/PyBoxPackage/pybox/FileFromBox.xlsx")

with tempfile.TemporaryFile() as fp:
    client.file(file_id=file_id).download_to(fp)

fp.read()

box_file = client.file(file_id='842030064507').get()
output_file = open("/Users/niranjan.ilawe/Documents/GitHub/PyBoxPackage/pybox/" + box_file.name, 'wb')
box_file.download_to(output_file)




user_id = '15730332787'
user = client.user(user_id).get()

if user.is_sync_enabled:
    print('User {0} has sync enabled'.format(user.name))

folder_id = '142574139233'
new_file = client.folder(folder_id).upload('/Users/niranjan.ilawe/Documents/GitHub/PyBoxPackage/pybox/')
print('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))