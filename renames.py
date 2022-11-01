import os
path = './__pycache__'
os.chdir(path)
for file in os.listdir():
    if file.endswith('.pyc'):
        newfile = file.split('.')[0] + '.py' 
        print('detect' in file)
        os.rename(file, newfile)
os.chdir('..')