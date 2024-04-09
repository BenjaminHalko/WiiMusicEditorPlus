from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QListWidget

from wii_music_editor.data.styles import style_list, Style, StyleInstruments
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.widgets.list_parent import ListParent
from wii_music_editor.ui.widgets.translate import tr


class StyleListWidget(ListParent):
    styles: list[Style]

    def __init__(self, widget: QListWidget):
        super().__init__(widget)
        self.styles = []

    def reset(self, only_allow: int = -1):
        super().reset()
        self.styles.clear()
        style_type_names = [
            tr('style_type_names', 'Global'),
            tr('style_type_names', 'Quick Jam'),
            tr('style_type_names', 'Song Specific'),
            tr('style_type_names', 'Menu'),
            tr('style_type_names', 'Unused')
        ]
        for i, style in enumerate(style_list):
            if i == 0 or style.style_type != style_list[i - 1].style_type:
                self.addHeader(f"-------- {style_type_names[style.style_type.value]} --------")
            item = QListWidgetItem()
            extraText = ""
            if rom_folder.styles[i] != style.style:
                extraText = f" ~[{tr('ui', 'Replaced')}]~"
            if len(rom_folder.text.styles) > i:
                item.setText(rom_folder.text.styles[i] + extraText)
            else:
                item.setText(style.name + extraText)
            if only_allow != -1 and i != only_allow:
                item.setFlags(item.flags() & Qt.ItemIsSelectable)
            self.widget.addItem(item)
            self.styles.append(style)
        if only_allow != -1:
            self.widget.setCurrentRow(only_allow)

    def getStyle(self) -> Style:
        return self.styles[self._getRow()]
