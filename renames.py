import os
path = './__pycache__'
os.chdir(path)
for file in os.listdir():
    if file.endswith('.pyc'):
        newfile = file.replace('.cpython-310', '')
        print('detect' in file)
        os.rename(file, newfile)
for file in ['main.pyc','detect.pyc', 'mail.pyc']:
    os.rename(file, file.replace('.pyc', 'py') )
os.chdir('..')