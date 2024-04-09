from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from wii_music_editor.data.instruments import instrument_list, InstrumentClass
from wii_music_editor.ui.widgets.list_parent import ListParent
from wii_music_editor.utils.preferences import preferences


class InstrumentListWidget(ListParent):
    instruments: list[InstrumentClass]

    def __init__(self, widget: QListWidget):
        super().__init__(widget)
        self.instruments = []
        self.reset()

    def reset(self, percussion: bool = False, menu: bool = False):
        super().reset()
        self.instruments.clear()
        if not percussion:
            instruments = instrument_list[:40]
        else:
            instruments = instrument_list[40:-1]
        normalRange = instruments
        if preferences.unsafe_mode:
            instruments = instrument_list[:-1]

        for inst in instruments:
            item = QListWidgetItem()
            item.setText(inst.name)
            if menu and not inst.in_menu:
                if preferences.unsafe_mode:
                    item.setForeground(QColor("#cf1800"))
                else:
                    item.setFlags(item.flags() & Qt.ItemIsSelectable)
            if inst not in normalRange:
                item.setForeground(QColor("#cf1800"))
            self.widget.addItem(item)
            self.instruments.append(inst)

        item = QListWidgetItem()
        item.setText(instrument_list[-1].name)
        if menu:
            if preferences.unsafe_mode:
                item.setForeground(QColor("#cf1800"))
            else:
                item.setFlags(item.flags() & Qt.ItemIsSelectable)
        self.widget.addItem(item)
        self.instruments.append(instrument_list[-1])

    def getInstrument(self) -> InstrumentClass:
        return self.instruments[self._getRow()]
