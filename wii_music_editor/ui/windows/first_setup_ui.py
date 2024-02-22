# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'first_setup.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_FirstSetup(object):
    def setupUi(self, FirstSetup):
        if not FirstSetup.objectName():
            FirstSetup.setObjectName(u"FirstSetup")
        FirstSetup.setWindowModality(Qt.ApplicationModal)
        FirstSetup.resize(435, 308)
        FirstSetup.setStyleSheet(u"QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #ffa02f;\n"
"     padding: 1px;\n"
"     border-radius: 3px;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: white;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QMenuBar\n"
"{\n"
"	background: #242424;\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
""
                        "        stop:0.4 #343434/*,\n"
"        stop:0.2 #343434,\n"
"        stop:0.1 #ffaa00*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: white;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"   "
                        " border-radius: 6;\n"
"    padding: 3px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"	padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    s"
                        "election-background-color: #ffaa00;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:images/images/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"Q"
                        "ScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
""
                        "     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: #121212;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b1"
                        "9;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"	padding-left: 1px;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #242424;\n"
""
                        "}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #414141;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDo"
                        "ckWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:images/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, s"
                        "top: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; "
                        "/* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: "
                        "6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QRadioButton:disabled\n"
"{\n"
"    background-color: #404040;\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:images/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"QWidget[error=\"true\"]\n"
"{\n"
"	border: 1px solid red;\n"
"}\n"
"\n"
"QWidget[error=\"true\""
                        "]\n"
"{\n"
"	border: 1px solid red;\n"
"}")
        self.verticalLayout = QVBoxLayout(FirstSetup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainWidget = QStackedWidget(FirstSetup)
        self.MainWidget.setObjectName(u"MainWidget")
        self.Title = QWidget()
        self.Title.setObjectName(u"Title")
        self.verticalLayout_2 = QVBoxLayout(self.Title)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.MainTitle = QLabel(self.Title)
        self.MainTitle.setObjectName(u"MainTitle")
        font = QFont()
        font.setFamilies([u"Continuum Medium"])
        font.setPointSize(14)
        self.MainTitle.setFont(font)
        self.MainTitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.MainTitle)

        self.TitleLine = QFrame(self.Title)
        self.TitleLine.setObjectName(u"TitleLine")
        self.TitleLine.setFrameShape(QFrame.HLine)
        self.TitleLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.TitleLine)

        self.Desc = QLabel(self.Title)
        self.Desc.setObjectName(u"Desc")

        self.verticalLayout_2.addWidget(self.Desc)

        self.TitleSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.TitleSpacer)

        self.MainWidget.addWidget(self.Title)
        self.Roms = QWidget()
        self.Roms.setObjectName(u"Roms")
        self.verticalLayout_4 = QVBoxLayout(self.Roms)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.RomTitle = QLabel(self.Roms)
        self.RomTitle.setObjectName(u"RomTitle")
        self.RomTitle.setFont(font)

        self.verticalLayout_4.addWidget(self.RomTitle)

        self.RomLine = QFrame(self.Roms)
        self.RomLine.setObjectName(u"RomLine")
        self.RomLine.setFrameShape(QFrame.HLine)
        self.RomLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.RomLine)

        self.RomPath = QGroupBox(self.Roms)
        self.RomPath.setObjectName(u"RomPath")
        self.verticalLayout_7 = QVBoxLayout(self.RomPath)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.RomPath_Label = QLabel(self.RomPath)
        self.RomPath_Label.setObjectName(u"RomPath_Label")
        self.RomPath_Label.setMinimumSize(QSize(0, 26))
        self.RomPath_Label.setMaximumSize(QSize(16777215, 26))
        self.RomPath_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"}\n"
"\n"
"QLabel[error=\"true\"]\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: red;\n"
"background-color: #242424;\n"
"}")

        self.verticalLayout_7.addWidget(self.RomPath_Label)

        self.RomPath_Buttons = QHBoxLayout()
        self.RomPath_Buttons.setObjectName(u"RomPath_Buttons")
        self.RomPath_File = QPushButton(self.RomPath)
        self.RomPath_File.setObjectName(u"RomPath_File")

        self.RomPath_Buttons.addWidget(self.RomPath_File)

        self.RomPath_Folder = QPushButton(self.RomPath)
        self.RomPath_Folder.setObjectName(u"RomPath_Folder")

        self.RomPath_Buttons.addWidget(self.RomPath_Folder)


        self.verticalLayout_7.addLayout(self.RomPath_Buttons)


        self.verticalLayout_4.addWidget(self.RomPath)

        self.RomSettings = QGroupBox(self.Roms)
        self.RomSettings.setObjectName(u"RomSettings")
        self.RomSettings.setEnabled(False)
        self.verticalLayout_9 = QVBoxLayout(self.RomSettings)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.Region = QHBoxLayout()
        self.Region.setObjectName(u"Region")
        self.RegionLabel = QLabel(self.RomSettings)
        self.RegionLabel.setObjectName(u"RegionLabel")

        self.Region.addWidget(self.RegionLabel)

        self.RegionBox = QComboBox(self.RomSettings)
        self.RegionBox.addItem("")
        self.RegionBox.addItem("")
        self.RegionBox.addItem("")
        self.RegionBox.addItem("")
        self.RegionBox.setObjectName(u"RegionBox")
        self.RegionBox.setMinimumSize(QSize(60, 20))

        self.Region.addWidget(self.RegionBox)


        self.verticalLayout_9.addLayout(self.Region)

        self.RomLanguage = QHBoxLayout()
        self.RomLanguage.setObjectName(u"RomLanguage")
        self.RomLanguageLabel = QLabel(self.RomSettings)
        self.RomLanguageLabel.setObjectName(u"RomLanguageLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RomLanguageLabel.sizePolicy().hasHeightForWidth())
        self.RomLanguageLabel.setSizePolicy(sizePolicy)

        self.RomLanguage.addWidget(self.RomLanguageLabel)

        self.RomLanguageBox = QComboBox(self.RomSettings)
        self.RomLanguageBox.setObjectName(u"RomLanguageBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RomLanguageBox.sizePolicy().hasHeightForWidth())
        self.RomLanguageBox.setSizePolicy(sizePolicy1)
        self.RomLanguageBox.setCurrentText(u"")

        self.RomLanguage.addWidget(self.RomLanguageBox)


        self.verticalLayout_9.addLayout(self.RomLanguage)


        self.verticalLayout_4.addWidget(self.RomSettings)

        self.RomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.RomSpacer)

        self.MainWidget.addWidget(self.Roms)
        self.Dolphin = QWidget()
        self.Dolphin.setObjectName(u"Dolphin")
        self.verticalLayout_11 = QVBoxLayout(self.Dolphin)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.DolphinTitle = QLabel(self.Dolphin)
        self.DolphinTitle.setObjectName(u"DolphinTitle")
        self.DolphinTitle.setFont(font)

        self.verticalLayout_11.addWidget(self.DolphinTitle)

        self.DolphinLine = QFrame(self.Dolphin)
        self.DolphinLine.setObjectName(u"DolphinLine")
        self.DolphinLine.setFrameShape(QFrame.HLine)
        self.DolphinLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.DolphinLine)

        self.DolphinPath_Title = QGroupBox(self.Dolphin)
        self.DolphinPath_Title.setObjectName(u"DolphinPath_Title")
        self.verticalLayout_5 = QVBoxLayout(self.DolphinPath_Title)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.DolphinPath_Label = QLabel(self.DolphinPath_Title)
        self.DolphinPath_Label.setObjectName(u"DolphinPath_Label")
        self.DolphinPath_Label.setMinimumSize(QSize(0, 26))
        self.DolphinPath_Label.setMaximumSize(QSize(16777215, 26))
        self.DolphinPath_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"}\n"
"\n"
"QLabel[error=\"true\"]\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: red;\n"
"background-color: #242424;\n"
"}")

        self.verticalLayout_5.addWidget(self.DolphinPath_Label)

        self.DolphinPath_Browse = QPushButton(self.DolphinPath_Title)
        self.DolphinPath_Browse.setObjectName(u"DolphinPath_Browse")

        self.verticalLayout_5.addWidget(self.DolphinPath_Browse)


        self.verticalLayout_11.addWidget(self.DolphinPath_Title)

        self.DolphinSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.DolphinSpacer)

        self.MainWidget.addWidget(self.Dolphin)
        self.End = QWidget()
        self.End.setObjectName(u"End")
        self.verticalLayout_6 = QVBoxLayout(self.End)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.EndTitle = QLabel(self.End)
        self.EndTitle.setObjectName(u"EndTitle")
        font1 = QFont()
        font1.setFamilies([u"Continuum Medium"])
        font1.setPointSize(20)
        self.EndTitle.setFont(font1)

        self.verticalLayout_6.addWidget(self.EndTitle)

        self.EndLine = QFrame(self.End)
        self.EndLine.setObjectName(u"EndLine")
        self.EndLine.setFrameShape(QFrame.HLine)
        self.EndLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.EndLine)

        self.EndDesc = QLabel(self.End)
        self.EndDesc.setObjectName(u"EndDesc")

        self.verticalLayout_6.addWidget(self.EndDesc)

        self.EndSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.EndSpacer)

        self.EndLinks = QLabel(self.End)
        self.EndLinks.setObjectName(u"EndLinks")
        self.EndLinks.setOpenExternalLinks(True)

        self.verticalLayout_6.addWidget(self.EndLinks)

        self.MainWidget.addWidget(self.End)

        self.verticalLayout.addWidget(self.MainWidget)

        self.BottomLine = QFrame(FirstSetup)
        self.BottomLine.setObjectName(u"BottomLine")
        self.BottomLine.setFrameShape(QFrame.HLine)
        self.BottomLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.BottomLine)

        self.MenuButtons = QHBoxLayout()
        self.MenuButtons.setObjectName(u"MenuButtons")
        self.MenuSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.MenuButtons.addItem(self.MenuSpacer)

        self.BackButton = QPushButton(FirstSetup)
        self.BackButton.setObjectName(u"BackButton")
        self.BackButton.setMinimumSize(QSize(70, 0))

        self.MenuButtons.addWidget(self.BackButton)

        self.NextButton = QPushButton(FirstSetup)
        self.NextButton.setObjectName(u"NextButton")
        self.NextButton.setMinimumSize(QSize(70, 0))

        self.MenuButtons.addWidget(self.NextButton)


        self.verticalLayout.addLayout(self.MenuButtons)


        self.retranslateUi(FirstSetup)

        self.MainWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FirstSetup)
    # setupUi

    def retranslateUi(self, FirstSetup):
        FirstSetup.setWindowTitle(QCoreApplication.translate("FirstSetup", u"First Setup", None))
        self.MainTitle.setText(QCoreApplication.translate("FirstSetup", u"Thanks for downloading the\n"
"Wii Music Editor Plus!", None))
        self.Desc.setText(QCoreApplication.translate("FirstSetup", u"Let's help you setup the essentials!", None))
        self.RomTitle.setText(QCoreApplication.translate("FirstSetup", u"Loading Roms", None))
        self.RomPath.setTitle(QCoreApplication.translate("FirstSetup", u"Rom Path", None))
        self.RomPath_Label.setText(QCoreApplication.translate("FirstSetup", u"No Specified Path", None))
        self.RomPath_File.setText(QCoreApplication.translate("FirstSetup", u"Load From File", None))
        self.RomPath_Folder.setText(QCoreApplication.translate("FirstSetup", u"Load From Folder", None))
        self.RomSettings.setTitle(QCoreApplication.translate("FirstSetup", u"Rom Settings", None))
        self.RegionLabel.setText(QCoreApplication.translate("FirstSetup", u"Fallback Region (Used if rom region can't be determinded):", None))
        self.RegionBox.setItemText(0, QCoreApplication.translate("FirstSetup", u"U.S.", None))
        self.RegionBox.setItemText(1, QCoreApplication.translate("FirstSetup", u"Europe", None))
        self.RegionBox.setItemText(2, QCoreApplication.translate("FirstSetup", u"Japan", None))
        self.RegionBox.setItemText(3, QCoreApplication.translate("FirstSetup", u"Korea", None))

        self.RomLanguageLabel.setText(QCoreApplication.translate("FirstSetup", u"Rom Language:", None))
        self.DolphinTitle.setText(QCoreApplication.translate("FirstSetup", u"Setting Up Dolphin", None))
        self.DolphinPath_Title.setTitle(QCoreApplication.translate("FirstSetup", u"Dolphin Path", None))
        self.DolphinPath_Label.setText(QCoreApplication.translate("FirstSetup", u"No Specified Path", None))
        self.DolphinPath_Browse.setText(QCoreApplication.translate("FirstSetup", u"Browse", None))
        self.EndTitle.setText(QCoreApplication.translate("FirstSetup", u"<html><head/><body><p align=\"center\">All Done!</p></body></html>", None))
        self.EndDesc.setText(QCoreApplication.translate("FirstSetup", u"Enjoy modding Wii Music!", None))
        self.EndLinks.setText(QCoreApplication.translate("FirstSetup", u"<html><head/><body><p>YouTube: <a href=\"https://www.youtube.com/BenjaminHalko\"><span style=\" text-decoration: underline; color:#ffaa00;\">https://www.youtube.com/BenjaminHalko</span></a></p><p>Donate: <a href=\"https://ko-fi.com/benjaminhalko\"><span style=\" text-decoration: underline; color:#ffaa00;\">https://ko-fi.com/benjaminhalko</span></a></p><p>Wiki: <a href=\"https://github.com/BenjaminHalko/WiiMusicEditorPlus/wiki\"><span style=\" text-decoration: underline; color:#ffaa00;\">https://github.com/BenjaminHalko/WiiMusicEditorPlus/wiki</span></a></p><p>Discord: <a href=\"https://discord.gg/NC3wYAeCDs\"><span style=\" text-decoration: underline; color:#ffaa00;\">https://discord.gg/NC3wYAeCDs</span></a></p></body></html>", None))
        self.BackButton.setText(QCoreApplication.translate("FirstSetup", u"Back", None))
        self.NextButton.setText(QCoreApplication.translate("FirstSetup", u"Next", None))
    # retranslateUi

