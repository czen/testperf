import os
import sys
import subprocess
import shutil


def copy_doxyfile():
    doxyfile = os.path.join(os.path.dirname(sys.argv[0]), 'doxy', 'Doxyfile')
    try:
        os.mkdir('doxy')
        shutil.copy(doxyfile, 'doxy')
    except OSError:
        shutil.rmtree(os.path.join('doxy', 'xml'))
        shutil.copy(doxyfile, 'doxy')


def write_path_to_doxyfile(include_path):
    with open(os.path.join('doxy', 'Doxyfile'), 'a') as doxyfile:
        doxyfile.write('INPUT = {}'.format(include_path))


# def find_include_files(include_path):
#     files_and_dirs = os.path.listdir(include_path)
#     dirs = []
#     inc_files = []
#     other_files = []
#     for file_name in os.path.listdir(include_path):
#         if '.h' or '.cpp' or '.c' in file_name:
#             inc_files.append(file_name)
#         elif os.isdir(os.path.join(include_path, file_name)):
#             dirs.append(file_name)
#         else:
#             other_files.append(file_name)


def make_xml(include_path):
    abs_inc_path = os.path.abspath(include_path)
    if not os.path.exists(abs_inc_path):
        print('-----------------------------------------------------')
        print("Error! Path: '{}' doesn't exist".format(include_path))
        print("The perf tests won't be created!")
        print('-----------------------------------------------------')
        raise FileExistsError
    copy_doxyfile()
    write_path_to_doxyfile(abs_inc_path)
    os.chdir('doxy')
    with open(os.devnull, 'wb') as devnull:
        try:
            subprocess.check_call('doxygen', stdout=devnull, stderr=subprocess.STDOUT)
            print('Starting doxygen...\n')
        except Exception as err:
            print(err)
            print('Starting doxygen                         [FAIL]\n')
    os.chdir('..')