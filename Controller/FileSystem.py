import os
import re
import shutil

class FileSystem(object):

    def archive_file(self, file, file_path, dir_path):
        archive_path = dir_path + "\\archived_receipts" + "\\" + file
        shutil.copyfile(file_path, archive_path)
        os.remove(file_path)

    def restore_files(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        source_path = parent_path + "\\archived_receipts"
        target_path = parent_path + "\\source_receipts"
        for file in os.scandir(source_path):
            if file.is_file() and not file.name.startswith('.'):
                file_path = source_path + "\\" + file.name
                new_file_path = target_path + "\\" + file.name
                shutil.copyfile(file_path, new_file_path)
                os.remove(file_path)
