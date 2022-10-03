from tabulate import tabulate

class Table:
    def __int__(self, data:list, headers:list):
        self._data_ = []

    def Make(self, data, headers:list):
        return tabulate(headers=headers, tabular_data=data, showindex='always', missingval="-", numalign="center", stralign="center")
    def print(self, data, headers:list):
        print(tabulate(headers=headers, tabular_data=data, showindex='always', missingval="-", numalign="center", stralign="center"))
table = Table()