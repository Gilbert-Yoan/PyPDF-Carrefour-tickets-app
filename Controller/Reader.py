import PyPDF2
import os
import re
import shutil


class Reader():
    def __init__(self,master):
        self.Controller = master

    def read_file(self, file):
        # creating a pdf reader object
        reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        # cycle over all the pdf pages
        for i in range (0, len(reader.pages)):
        # concatenate the text of all pages together in order
            pdf_text = pdf_text + reader.pages[i].extract_text()
        return pdf_text

    def get_info_dict(self, pdf_text):
        #(?P<categorie>\d*\.\d*)%
        #(?P<name>[A-Za-z0-9 \.]+)
        # (?P<quantite>\d) x[^;]*
        # (?P<prix>\d*\.\d*);")
        pattern = re.compile(r"(?P<categorie>\d*\.\d*)%(?P<name>[A-Za-z0-9 \.+,\/\-\*%]+) (?P<quantite>\d) x[^;]* (?P<prix>\d*\.\d*);")
        res = pattern.findall(pdf_text)
        return res


    def get_date(self, file):
        return re.search(r"\d{4}-\d{2}-\d{2}", file).group(0)


    def ingest_files(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        source_path = parent_path + "\\source_receipts"
        for file in os.scandir(source_path):
            if file.is_file() and not file.name.startswith('.'):
                file_path = source_path + "\\" +file.name
                text = self.read_file(file_path)
                text = text.replace("\n",";")
                res = self.get_info_dict(text)
                date = self.get_date(file.name)
                if self.Controller.inserter.insert_db(date,res) == 0 :
                    print("At least one item has not been inserted because of its category. Error 0.")
                else:
                    print("Database fully provisionned with file "+ file.name + ".")
                    self.Controller.filesystem.archive_file(file.name, file_path, parent_path)
