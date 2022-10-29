import csv


class ParserCSV:
    def __init__(self, file_path: str, file_name: str):
        self.file_path = file_path
        self.file_name = file_name

    def get_items(self) -> list:
        with open(self.file_path + self.file_name, newline='') as csvfile:
            items = list(csv.DictReader(csvfile))

        return items
