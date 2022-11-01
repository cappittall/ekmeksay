import os
path = './__pycache__'
os.chdir(path)
for file in os.listdir():
    if file.endswith('.pyc'):
        newfile = file.split('.')[0] + '.pyc' 
        os.rename(file, newfile)
os.rename('detect.pyc', 'detect.py')
os.chdir('..')