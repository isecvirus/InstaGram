from tabulate import tabulate
from prompt_toolkit import print_formatted_text

class Table:
    def __int__(self, data:list, headers:list):
        self._data_ = []

    def make(self, data, headers:list):
        return tabulate(headers=headers, tabular_data=data, showindex='always', missingval="-", numalign="center", stralign="center")
    def print(self, data, headers:list):
        print_formatted_text(tabulate(headers=headers, tabular_data=data, showindex='always', missingval="-", numalign="center", stralign="center"))
table = Table()