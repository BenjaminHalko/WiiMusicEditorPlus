# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.setWindowModality(Qt.ApplicationModal)
        Settings.resize(443, 308)
        Settings.setStyleSheet(u"QToolTip\n"
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
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainWidget = QTabWidget(Settings)
        self.MainWidget.setObjectName(u"MainWidget")
        self.Tab_General = QWidget()
        self.Tab_General.setObjectName(u"Tab_General")
        self.verticalLayout_3 = QVBoxLayout(self.Tab_General)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.SongEditor = QGroupBox(self.Tab_General)
        self.SongEditor.setObjectName(u"SongEditor")
        self.verticalLayout_4 = QVBoxLayout(self.SongEditor)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.SongScoreCheckbox = QCheckBox(self.SongEditor)
        self.SongScoreCheckbox.setObjectName(u"SongScoreCheckbox")

        self.verticalLayout_4.addWidget(self.SongScoreCheckbox)

        self.RapperFix = QCheckBox(self.SongEditor)
        self.RapperFix.setObjectName(u"RapperFix")
        self.RapperFix.setEnabled(False)
        self.RapperFix.setChecked(True)

        self.verticalLayout_4.addWidget(self.RapperFix)

        self.Normalize = QCheckBox(self.SongEditor)
        self.Normalize.setObjectName(u"Normalize")

        self.verticalLayout_4.addWidget(self.Normalize)


        self.verticalLayout_3.addWidget(self.SongEditor)

        self.groupBox = QGroupBox(self.Tab_General)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setTitle(u"Discord")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.Discord = QCheckBox(self.groupBox)
        self.Discord.setObjectName(u"Discord")
        self.Discord.setChecked(True)

        self.verticalLayout_12.addWidget(self.Discord)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.Updates = QGroupBox(self.Tab_General)
        self.Updates.setObjectName(u"Updates")
        self.verticalLayout_13 = QVBoxLayout(self.Updates)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.CheckForUpdates = QCheckBox(self.Updates)
        self.CheckForUpdates.setObjectName(u"CheckForUpdates")
        self.CheckForUpdates.setChecked(True)

        self.verticalLayout_13.addWidget(self.CheckForUpdates)

        self.UnsafeMode = QCheckBox(self.Updates)
        self.UnsafeMode.setObjectName(u"UnsafeMode")
        self.UnsafeMode.setEnabled(True)

        self.verticalLayout_13.addWidget(self.UnsafeMode)


        self.verticalLayout_3.addWidget(self.Updates)

        self.General_Spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.General_Spacer)

        self.MainWidget.addTab(self.Tab_General, "")
        self.Tab_Dolphin = QWidget()
        self.Tab_Dolphin.setObjectName(u"Tab_Dolphin")
        self.verticalLayout_2 = QVBoxLayout(self.Tab_Dolphin)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.DolphinPath_Title = QGroupBox(self.Tab_Dolphin)
        self.DolphinPath_Title.setObjectName(u"DolphinPath_Title")
        self.verticalLayout_5 = QVBoxLayout(self.DolphinPath_Title)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.DolphinPath_Label = QLabel(self.DolphinPath_Title)
        self.DolphinPath_Label.setObjectName(u"DolphinPath_Label")
        font = QFont()
        font.setPointSize(8)
        self.DolphinPath_Label.setFont(font)
        self.DolphinPath_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")

        self.verticalLayout_5.addWidget(self.DolphinPath_Label)

        self.DolphinPath_Browse = QPushButton(self.DolphinPath_Title)
        self.DolphinPath_Browse.setObjectName(u"DolphinPath_Browse")

        self.verticalLayout_5.addWidget(self.DolphinPath_Browse)


        self.verticalLayout_2.addWidget(self.DolphinPath_Title)

        self.DolphinSave_Title = QGroupBox(self.Tab_Dolphin)
        self.DolphinSave_Title.setObjectName(u"DolphinSave_Title")
        self.verticalLayout_6 = QVBoxLayout(self.DolphinSave_Title)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.DolphinSave_Label = QLabel(self.DolphinSave_Title)
        self.DolphinSave_Label.setObjectName(u"DolphinSave_Label")
        self.DolphinSave_Label.setFont(font)
        self.DolphinSave_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")

        self.verticalLayout_6.addWidget(self.DolphinSave_Label)

        self.DolphinSave_Buttons = QHBoxLayout()
        self.DolphinSave_Buttons.setObjectName(u"DolphinSave_Buttons")
        self.DolphinSave_Browse = QPushButton(self.DolphinSave_Title)
        self.DolphinSave_Browse.setObjectName(u"DolphinSave_Browse")

        self.DolphinSave_Buttons.addWidget(self.DolphinSave_Browse)

        self.DolphinSave_Default = QPushButton(self.DolphinSave_Title)
        self.DolphinSave_Default.setObjectName(u"DolphinSave_Default")

        self.DolphinSave_Buttons.addWidget(self.DolphinSave_Default)


        self.verticalLayout_6.addLayout(self.DolphinSave_Buttons)


        self.verticalLayout_2.addWidget(self.DolphinSave_Title)

        self.Tab_Dolphin_Spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.Tab_Dolphin_Spacer)

        self.MainWidget.addTab(self.Tab_Dolphin, "")
        self.MainWidget.setTabText(self.MainWidget.indexOf(self.Tab_Dolphin), u"Dolphin")

        self.verticalLayout.addWidget(self.MainWidget)


        self.retranslateUi(Settings)

        self.MainWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.SongEditor.setTitle(QCoreApplication.translate("Settings", u"Song Editor", None))
        self.SongScoreCheckbox.setText(QCoreApplication.translate("Settings", u"Load Song and Score separately", None))
        self.RapperFix.setText(QCoreApplication.translate("Settings", u"Add the Rapper Crash fix", None))
        self.Normalize.setText(QCoreApplication.translate("Settings", u"Normalize Midi (Makes Midis more Wii Music friendly)", None))
        self.Discord.setText(QCoreApplication.translate("Settings", u"Discord Rich Presence", None))
        self.Updates.setTitle(QCoreApplication.translate("Settings", u"Misc", None))
        self.CheckForUpdates.setText(QCoreApplication.translate("Settings", u"Check for Updates on Startup", None))
        self.UnsafeMode.setText(QCoreApplication.translate("Settings", u"Unsafe mode (Enables options that might crash the game)", None))
        self.MainWidget.setTabText(self.MainWidget.indexOf(self.Tab_General), QCoreApplication.translate("Settings", u"General", None))
        self.DolphinPath_Title.setTitle(QCoreApplication.translate("Settings", u"Dolphin Path", None))
        self.DolphinPath_Label.setText(QCoreApplication.translate("Settings", u"No Specified Path", None))
        self.DolphinPath_Browse.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.DolphinSave_Title.setTitle(QCoreApplication.translate("Settings", u"Dolphin Save Path", None))
        self.DolphinSave_Label.setText(QCoreApplication.translate("Settings", u"Default Path", None))
        self.DolphinSave_Browse.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.DolphinSave_Default.setText(QCoreApplication.translate("Settings", u"Set as Default", None))
    # retranslateUi

