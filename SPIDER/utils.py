from os import makedirs, rmdir
from os.path import exists

def dir_maker(directory):
    if not exists(directory):
        makedirs(directory)
    else:
        pass

def dir_remover(directory):
    if exists(directory):
        rmdir(directory)
    else:
        pass


