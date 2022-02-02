from zipfile import ZipFile
import os

addondirectory = 'simloader'
templatedirectory  = 'template'
meshiodirectory = 'extern/meshio/src/meshio'
fileseqdirectory = 'extern/fileseq/src/fileseq'
futuredirectory = 'extern/python-future/src/future'
richdirectory = 'extern/rich/rich'


dirs = {addondirectory:addondirectory,
    templatedirectory:templatedirectory,
    meshiodirectory:'meshio',
    fileseqdirectory:'fileseq',
    futuredirectory:'future',
    richdirectory:'rich',
}

with ZipFile('simloader_addon.zip','w') as addonzip:
    #  write simloader directory
    for k,v in dirs.items():
        for subdir, dirs, files in os.walk(k):
            for file in files:
                if "__pycache__" in  subdir:
                    continue
                filepath = os.path.join(subdir, file)
                relative_path = os.path.relpath(filepath,k)
                endpath = os.path.join(v, relative_path)
                print(endpath)
                addonzip.write(filepath,endpath)

    # write init.py
    addonzip.write('__init__.py')
    

