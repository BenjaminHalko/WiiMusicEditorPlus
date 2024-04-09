from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem


class ListParent:
    widget: QListWidget
    headers: list[int]

    def __init__(self, widget: QListWidget):
        super().__init__()
        self.widget = widget
        self.headers = []

    def reset(self):
        self.widget.clear()

    def addHeader(self, text: str):
        item = QListWidgetItem()
        item.setText(text)
        item.setFlags(item.flags() & Qt.ItemIsSelectable)
        self.widget.addItem(item)
        self.headers.append(self.widget.count())

    def _getRow(self) -> int:
        row = self.widget.currentRow()
        for header in self.headers:
            if self.widget.currentRow() >= header:
                row -= 1
        return row

    def setRow(self, row: int):
        row_to_return = row
        row_to_check = 0
        for header in self.headers:
            if row >= row_to_check:
                row_to_return += 1
            row_to_check += header
        self.widget.setCurrentRow(row_to_return)
