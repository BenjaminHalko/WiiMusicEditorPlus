# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(869, 605)
        MainWindow.setContextMenuPolicy(Qt.NoContextMenu)
        MainWindow.setWindowTitle(u"Wii Music Editor Plus")
        MainWindow.setStyleSheet(u"QToolTip\n"
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
"QSpinBox\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QDoubleSpinBox\n"
"{\n"
"    bac"
                        "kground-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
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
"    border-radius: 6;\n"
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
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: "
                        "0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
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
"    selection-background-color: #ffaa00;\n"
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
"     border-left-style: solid;"
                        " /* just a single line */\n"
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
"QScrollBar:horizontal {\n"
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
"QScroll"
                        "Bar::add-line:horizontal {\n"
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
"QScrollBar:vert"
                        "ical\n"
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
"      border: 1px solid #1b1b19;\n"
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
"   "
                        "   subcontrol-position: top;\n"
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
"    background-color: QLinear"
                        "Gradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
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
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
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
"    background-color: Q"
                        "LinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
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
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
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
"    border: 1px solid #444;"
                        "\n"
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
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
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
"    margin-bottom: "
                        "0px;\n"
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
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #323232,\n"
"        st"
                        "op: 0.3 #323232);\n"
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
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:images/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:disabled\n"
"{\n"
"    image:url(:images/images/checkbox_disabled.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
"}")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.MB_LoadFile = QAction(MainWindow)
        self.MB_LoadFile.setObjectName(u"MB_LoadFile")
        self.MB_LoadFolder = QAction(MainWindow)
        self.MB_LoadFolder.setObjectName(u"MB_LoadFolder")
        self.MB_Dolphin = QAction(MainWindow)
        self.MB_Dolphin.setObjectName(u"MB_Dolphin")
        self.MB_DolphinMenu = QAction(MainWindow)
        self.MB_DolphinMenu.setObjectName(u"MB_DolphinMenu")
        self.MB_Updates = QAction(MainWindow)
        self.MB_Updates.setObjectName(u"MB_Updates")
        self.MB_Settings = QAction(MainWindow)
        self.MB_Settings.setObjectName(u"MB_Settings")
        self.MB_DownloadSongs = QAction(MainWindow)
        self.MB_DownloadSongs.setObjectName(u"MB_DownloadSongs")
        self.MB_Help = QAction(MainWindow)
        self.MB_Help.setObjectName(u"MB_Help")
        self.MB_SaveFolder = QAction(MainWindow)
        self.MB_SaveFolder.setObjectName(u"MB_SaveFolder")
        self.MB_SaveFile = QAction(MainWindow)
        self.MB_SaveFile.setObjectName(u"MB_SaveFile")
        self.MB_Documentation = QAction(MainWindow)
        self.MB_Documentation.setObjectName(u"MB_Documentation")
        self.MB_About = QAction(MainWindow)
        self.MB_About.setObjectName(u"MB_About")
        self.MB_Donate = QAction(MainWindow)
        self.MB_Donate.setObjectName(u"MB_Donate")
        self.MB_Discord = QAction(MainWindow)
        self.MB_Discord.setObjectName(u"MB_Discord")
        self.MB_Discord.setText(u"Discord")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(50, 50, 50, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 128))
        brush2.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        brush3 = QBrush(QColor(64, 64, 64, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush4 = QBrush(QColor(64, 64, 64, 128))
        brush4.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush4)
#endif
        self.centralwidget.setPalette(palette)
        self.verticalLayout_17 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.MainWidget = QStackedWidget(self.centralwidget)
        self.MainWidget.setObjectName(u"MainWidget")
        font = QFont()
        font.setFamilies([u"Continuum Bold"])
        font.setPointSize(72)
        self.MainWidget.setFont(font)
        self.MainPage = QWidget()
        self.MainPage.setObjectName(u"MainPage")
        self.verticalLayout_9 = QVBoxLayout(self.MainPage)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.MP_Title = QLabel(self.MainPage)
        self.MP_Title.setObjectName(u"MP_Title")
        self.MP_Title.setMaximumSize(QSize(16777215, 70))
        font1 = QFont()
        font1.setFamilies([u"Continuum Medium"])
        font1.setPointSize(26)
        self.MP_Title.setFont(font1)
        self.MP_Title.setText(u"<html><head/><body><p><img src=\":/images/images/Title.png\"/></p></body></html>")
        self.MP_Title.setScaledContents(False)

        self.verticalLayout_9.addWidget(self.MP_Title)

        self.MP_vLine = QFrame(self.MainPage)
        self.MP_vLine.setObjectName(u"MP_vLine")
        self.MP_vLine.setFrameShape(QFrame.HLine)
        self.MP_vLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.MP_vLine)

        self.MP_RomInfo = QHBoxLayout()
        self.MP_RomInfo.setObjectName(u"MP_RomInfo")
        self.MP_RomInfo_Path = QVBoxLayout()
        self.MP_RomInfo_Path.setObjectName(u"MP_RomInfo_Path")
        self.MP_LoadedFile_Label = QLabel(self.MainPage)
        self.MP_LoadedFile_Label.setObjectName(u"MP_LoadedFile_Label")

        self.MP_RomInfo_Path.addWidget(self.MP_LoadedFile_Label)

        self.MP_LoadedFile_Path = QLabel(self.MainPage)
        self.MP_LoadedFile_Path.setObjectName(u"MP_LoadedFile_Path")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MP_LoadedFile_Path.sizePolicy().hasHeightForWidth())
        self.MP_LoadedFile_Path.setSizePolicy(sizePolicy)
        self.MP_LoadedFile_Path.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")

        self.MP_RomInfo_Path.addWidget(self.MP_LoadedFile_Path)


        self.MP_RomInfo.addLayout(self.MP_RomInfo_Path)

        self.line_2 = QFrame(self.MainPage)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.MP_RomInfo.addWidget(self.line_2)

        self.MP_RomInfo_Region = QVBoxLayout()
        self.MP_RomInfo_Region.setObjectName(u"MP_RomInfo_Region")
        self.MP_Rom_Region_Label = QLabel(self.MainPage)
        self.MP_Rom_Region_Label.setObjectName(u"MP_Rom_Region_Label")
        self.MP_Rom_Region_Label.setMinimumSize(QSize(150, 0))

        self.MP_RomInfo_Region.addWidget(self.MP_Rom_Region_Label)

        self.MP_Rom_Region = QLabel(self.MainPage)
        self.MP_Rom_Region.setObjectName(u"MP_Rom_Region")
        self.MP_Rom_Region.setEnabled(True)
        self.MP_Rom_Region.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")
        self.MP_Rom_Region.setText(u"")

        self.MP_RomInfo_Region.addWidget(self.MP_Rom_Region)


        self.MP_RomInfo.addLayout(self.MP_RomInfo_Region)

        self.line_3 = QFrame(self.MainPage)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.MP_RomInfo.addWidget(self.line_3)

        self.MP_RomInfo_Language = QVBoxLayout()
        self.MP_RomInfo_Language.setObjectName(u"MP_RomInfo_Language")
        self.MP_RomInfo_Language_Label = QLabel(self.MainPage)
        self.MP_RomInfo_Language_Label.setObjectName(u"MP_RomInfo_Language_Label")
        self.MP_RomInfo_Language_Label.setMinimumSize(QSize(150, 0))

        self.MP_RomInfo_Language.addWidget(self.MP_RomInfo_Language_Label)

        self.verticalSpacer_4 = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.MP_RomInfo_Language.addItem(self.verticalSpacer_4)

        self.MP_Language = QComboBox(self.MainPage)
        self.MP_Language.setObjectName(u"MP_Language")
        self.MP_Language.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.MP_Language.sizePolicy().hasHeightForWidth())
        self.MP_Language.setSizePolicy(sizePolicy1)
        self.MP_Language.setCurrentText(u"")

        self.MP_RomInfo_Language.addWidget(self.MP_Language)


        self.MP_RomInfo.addLayout(self.MP_RomInfo_Language)


        self.verticalLayout_9.addLayout(self.MP_RomInfo)

        self.MP_MainFeatures = QHBoxLayout()
        self.MP_MainFeatures.setObjectName(u"MP_MainFeatures")
        self.MP_SongEditor_Button = QPushButton(self.MainPage)
        self.MP_SongEditor_Button.setObjectName(u"MP_SongEditor_Button")
        self.MP_SongEditor_Button.setMinimumSize(QSize(0, 64))
        font2 = QFont()
        font2.setFamilies([u"Continuum Bold"])
        font2.setPointSize(26)
        self.MP_SongEditor_Button.setFont(font2)

        self.MP_MainFeatures.addWidget(self.MP_SongEditor_Button)

        self.MP_StyleEditor_Button = QPushButton(self.MainPage)
        self.MP_StyleEditor_Button.setObjectName(u"MP_StyleEditor_Button")
        self.MP_StyleEditor_Button.setMinimumSize(QSize(0, 64))
        self.MP_StyleEditor_Button.setFont(font2)

        self.MP_MainFeatures.addWidget(self.MP_StyleEditor_Button)


        self.verticalLayout_9.addLayout(self.MP_MainFeatures)

        self.line = QFrame(self.MainPage)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_2)

        self.MP_Advanced = QGroupBox(self.MainPage)
        self.MP_Advanced.setObjectName(u"MP_Advanced")
        self.verticalLayout_11 = QVBoxLayout(self.MP_Advanced)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.MP_Advanced1 = QHBoxLayout()
        self.MP_Advanced1.setObjectName(u"MP_Advanced1")
        self.MP_EditText_Button = QPushButton(self.MP_Advanced)
        self.MP_EditText_Button.setObjectName(u"MP_EditText_Button")
        font3 = QFont()
        font3.setFamilies([u"Continuum Medium"])
        font3.setPointSize(14)
        self.MP_EditText_Button.setFont(font3)

        self.MP_Advanced1.addWidget(self.MP_EditText_Button)

        self.MP_DefaultStyle_Button = QPushButton(self.MP_Advanced)
        self.MP_DefaultStyle_Button.setObjectName(u"MP_DefaultStyle_Button")
        self.MP_DefaultStyle_Button.setFont(font3)

        self.MP_Advanced1.addWidget(self.MP_DefaultStyle_Button)

        self.MP_RemoveSong_Button = QPushButton(self.MP_Advanced)
        self.MP_RemoveSong_Button.setObjectName(u"MP_RemoveSong_Button")
        self.MP_RemoveSong_Button.setEnabled(False)
        self.MP_RemoveSong_Button.setFont(font3)

        self.MP_Advanced1.addWidget(self.MP_RemoveSong_Button)


        self.verticalLayout_11.addLayout(self.MP_Advanced1)


        self.verticalLayout_9.addWidget(self.MP_Advanced)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_3)

        self.MP_Package = QGroupBox(self.MainPage)
        self.MP_Package.setObjectName(u"MP_Package")
        self.horizontalLayout_3 = QHBoxLayout(self.MP_Package)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.MP_Riivolution_Button = QPushButton(self.MP_Package)
        self.MP_Riivolution_Button.setObjectName(u"MP_Riivolution_Button")
        self.MP_Riivolution_Button.setFont(font3)

        self.horizontalLayout_3.addWidget(self.MP_Riivolution_Button)

        self.MP_PackRom_Button = QPushButton(self.MP_Package)
        self.MP_PackRom_Button.setObjectName(u"MP_PackRom_Button")
        self.MP_PackRom_Button.setMinimumSize(QSize(0, 36))
        self.MP_PackRom_Button.setFont(font3)

        self.horizontalLayout_3.addWidget(self.MP_PackRom_Button)


        self.verticalLayout_9.addWidget(self.MP_Package)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer)

        self.MP_RomEditing = QGroupBox(self.MainPage)
        self.MP_RomEditing.setObjectName(u"MP_RomEditing")
        self.verticalLayout_18 = QVBoxLayout(self.MP_RomEditing)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.MP_RomEditing1 = QHBoxLayout()
        self.MP_RomEditing1.setObjectName(u"MP_RomEditing1")
        self.MP_RevertChanges_Button = QPushButton(self.MP_RomEditing)
        self.MP_RevertChanges_Button.setObjectName(u"MP_RevertChanges_Button")
        self.MP_RevertChanges_Button.setMinimumSize(QSize(0, 36))
        self.MP_RevertChanges_Button.setFont(font3)

        self.MP_RomEditing1.addWidget(self.MP_RevertChanges_Button)


        self.verticalLayout_18.addLayout(self.MP_RomEditing1)

        self.MP_RomEditing2 = QHBoxLayout()
        self.MP_RomEditing2.setObjectName(u"MP_RomEditing2")
        self.MP_ImportFiles_Button = QPushButton(self.MP_RomEditing)
        self.MP_ImportFiles_Button.setObjectName(u"MP_ImportFiles_Button")
        self.MP_ImportFiles_Button.setEnabled(False)
        self.MP_ImportFiles_Button.setMinimumSize(QSize(0, 36))
        self.MP_ImportFiles_Button.setFont(font3)

        self.MP_RomEditing2.addWidget(self.MP_ImportFiles_Button)

        self.MP_ExportFiles_Button = QPushButton(self.MP_RomEditing)
        self.MP_ExportFiles_Button.setObjectName(u"MP_ExportFiles_Button")
        self.MP_ExportFiles_Button.setEnabled(False)
        self.MP_ExportFiles_Button.setMinimumSize(QSize(0, 36))
        self.MP_ExportFiles_Button.setFont(font3)

        self.MP_RomEditing2.addWidget(self.MP_ExportFiles_Button)

        self.MP_ImportChanges_Button = QPushButton(self.MP_RomEditing)
        self.MP_ImportChanges_Button.setObjectName(u"MP_ImportChanges_Button")
        self.MP_ImportChanges_Button.setEnabled(False)
        self.MP_ImportChanges_Button.setMinimumSize(QSize(0, 36))
        self.MP_ImportChanges_Button.setFont(font3)

        self.MP_RomEditing2.addWidget(self.MP_ImportChanges_Button)


        self.verticalLayout_18.addLayout(self.MP_RomEditing2)


        self.verticalLayout_9.addWidget(self.MP_RomEditing)

        self.MP_VerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.MP_VerticalSpacer)

        self.MainWidget.addWidget(self.MainPage)
        self.SongEditor = QWidget()
        self.SongEditor.setObjectName(u"SongEditor")
        self.verticalLayout_2 = QVBoxLayout(self.SongEditor)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Title = QHBoxLayout()
        self.Title.setObjectName(u"Title")
        self.SE_Title = QLabel(self.SongEditor)
        self.SE_Title.setObjectName(u"SE_Title")
        self.SE_Title.setMaximumSize(QSize(16777215, 44))
        self.SE_Title.setFont(font1)

        self.Title.addWidget(self.SE_Title)

        self.SE_Back_Button = QPushButton(self.SongEditor)
        self.SE_Back_Button.setObjectName(u"SE_Back_Button")
        self.SE_Back_Button.setMaximumSize(QSize(100, 30))
        font4 = QFont()
        font4.setPointSize(12)
        self.SE_Back_Button.setFont(font4)

        self.Title.addWidget(self.SE_Back_Button)


        self.verticalLayout_2.addLayout(self.Title)

        self.SE_MainLayout = QHBoxLayout()
        self.SE_MainLayout.setObjectName(u"SE_MainLayout")
        self.SE_MidiAndText = QVBoxLayout()
        self.SE_MidiAndText.setObjectName(u"SE_MidiAndText")
        self.SE_Midi = QGroupBox(self.SongEditor)
        self.SE_Midi.setObjectName(u"SE_Midi")
        self.SE_Midi.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.SE_Midi.sizePolicy().hasHeightForWidth())
        self.SE_Midi.setSizePolicy(sizePolicy2)
        self.SE_Midi.setFocusPolicy(Qt.NoFocus)
        self.SE_Midi.setCheckable(True)
        self.SE_Midi.setChecked(True)
        self.verticalLayout_4 = QVBoxLayout(self.SE_Midi)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.SE_Midi_File_Score_Label = QLabel(self.SE_Midi)
        self.SE_Midi_File_Score_Label.setObjectName(u"SE_Midi_File_Score_Label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.SE_Midi_File_Score_Label.sizePolicy().hasHeightForWidth())
        self.SE_Midi_File_Score_Label.setSizePolicy(sizePolicy3)
        self.SE_Midi_File_Score_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")
        self.SE_Midi_File_Score_Label.setText(u"Load a Midi-Type file")

        self.gridLayout.addWidget(self.SE_Midi_File_Score_Label, 0, 1, 1, 1)

        self.SE_Midi_File_Score_Button = QPushButton(self.SE_Midi)
        self.SE_Midi_File_Score_Button.setObjectName(u"SE_Midi_File_Score_Button")
        self.SE_Midi_File_Score_Button.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.SE_Midi_File_Score_Button, 0, 2, 1, 1)

        self.SE_Midi_File_Score_Title = QLabel(self.SE_Midi)
        self.SE_Midi_File_Score_Title.setObjectName(u"SE_Midi_File_Score_Title")

        self.gridLayout.addWidget(self.SE_Midi_File_Score_Title, 0, 0, 1, 1)

        self.SE_Midi_File_Song_Label = QLabel(self.SE_Midi)
        self.SE_Midi_File_Song_Label.setObjectName(u"SE_Midi_File_Song_Label")
        sizePolicy3.setHeightForWidth(self.SE_Midi_File_Song_Label.sizePolicy().hasHeightForWidth())
        self.SE_Midi_File_Song_Label.setSizePolicy(sizePolicy3)
        self.SE_Midi_File_Song_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")
        self.SE_Midi_File_Song_Label.setText(u"Load a Midi-Type file")

        self.gridLayout.addWidget(self.SE_Midi_File_Song_Label, 1, 1, 1, 1)

        self.SE_Midi_File_Song_Title = QLabel(self.SE_Midi)
        self.SE_Midi_File_Song_Title.setObjectName(u"SE_Midi_File_Song_Title")

        self.gridLayout.addWidget(self.SE_Midi_File_Song_Title, 1, 0, 1, 1)

        self.SE_Midi_File_Song_Button = QPushButton(self.SE_Midi)
        self.SE_Midi_File_Song_Button.setObjectName(u"SE_Midi_File_Song_Button")
        self.SE_Midi_File_Song_Button.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.SE_Midi_File_Song_Button, 1, 2, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.SE_Midi_File_Replace_Song = QCheckBox(self.SE_Midi)
        self.SE_Midi_File_Replace_Song.setObjectName(u"SE_Midi_File_Replace_Song")
        self.SE_Midi_File_Replace_Song.setEnabled(True)
        self.SE_Midi_File_Replace_Song.setChecked(True)

        self.verticalLayout_4.addWidget(self.SE_Midi_File_Replace_Song)

        self.SE_Midi_hLine = QFrame(self.SE_Midi)
        self.SE_Midi_hLine.setObjectName(u"SE_Midi_hLine")
        self.SE_Midi_hLine.setFrameShape(QFrame.HLine)
        self.SE_Midi_hLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.SE_Midi_hLine)

        self.SE_Midi_Info = QHBoxLayout()
        self.SE_Midi_Info.setObjectName(u"SE_Midi_Info")
        self.SE_Midi_Tempo = QFrame(self.SE_Midi)
        self.SE_Midi_Tempo.setObjectName(u"SE_Midi_Tempo")
        self.verticalLayout = QVBoxLayout(self.SE_Midi_Tempo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SE_Midi_Tempo_Label = QLabel(self.SE_Midi_Tempo)
        self.SE_Midi_Tempo_Label.setObjectName(u"SE_Midi_Tempo_Label")

        self.verticalLayout.addWidget(self.SE_Midi_Tempo_Label)

        self.SE_Midi_Tempo_Layout = QHBoxLayout()
        self.SE_Midi_Tempo_Layout.setObjectName(u"SE_Midi_Tempo_Layout")
        self.SE_Midi_Tempo_Input = QSpinBox(self.SE_Midi_Tempo)
        self.SE_Midi_Tempo_Input.setObjectName(u"SE_Midi_Tempo_Input")
        self.SE_Midi_Tempo_Input.setMinimumSize(QSize(80, 0))
        self.SE_Midi_Tempo_Input.setMaximum(10000)

        self.SE_Midi_Tempo_Layout.addWidget(self.SE_Midi_Tempo_Input)

        self.SE_Midi_Tempo_BPM = QLabel(self.SE_Midi_Tempo)
        self.SE_Midi_Tempo_BPM.setObjectName(u"SE_Midi_Tempo_BPM")
        self.SE_Midi_Tempo_BPM.setMaximumSize(QSize(30, 16777215))
        self.SE_Midi_Tempo_BPM.setText(u"BPM")

        self.SE_Midi_Tempo_Layout.addWidget(self.SE_Midi_Tempo_BPM)


        self.verticalLayout.addLayout(self.SE_Midi_Tempo_Layout)


        self.SE_Midi_Info.addWidget(self.SE_Midi_Tempo)

        self.SE_Midi_vLine_1 = QFrame(self.SE_Midi)
        self.SE_Midi_vLine_1.setObjectName(u"SE_Midi_vLine_1")
        self.SE_Midi_vLine_1.setFrameShape(QFrame.VLine)
        self.SE_Midi_vLine_1.setFrameShadow(QFrame.Sunken)

        self.SE_Midi_Info.addWidget(self.SE_Midi_vLine_1)

        self.SE_Midi_Length = QFrame(self.SE_Midi)
        self.SE_Midi_Length.setObjectName(u"SE_Midi_Length")
        self.verticalLayout_8 = QVBoxLayout(self.SE_Midi_Length)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.SE_Midi_Length_Label = QLabel(self.SE_Midi_Length)
        self.SE_Midi_Length_Label.setObjectName(u"SE_Midi_Length_Label")

        self.verticalLayout_8.addWidget(self.SE_Midi_Length_Label)

        self.SE_Midi_Length_Layout = QHBoxLayout()
        self.SE_Midi_Length_Layout.setObjectName(u"SE_Midi_Length_Layout")
        self.SE_Midi_Length_Input = QSpinBox(self.SE_Midi_Length)
        self.SE_Midi_Length_Input.setObjectName(u"SE_Midi_Length_Input")
        self.SE_Midi_Length_Input.setMinimumSize(QSize(80, 0))
        self.SE_Midi_Length_Input.setMaximum(10000)
        self.SE_Midi_Length_Input.setValue(0)

        self.SE_Midi_Length_Layout.addWidget(self.SE_Midi_Length_Input)

        self.SE_Midi_Length_Measures = QRadioButton(self.SE_Midi_Length)
        self.SE_Midi_Length_Measures.setObjectName(u"SE_Midi_Length_Measures")
        self.SE_Midi_Length_Measures.setFocusPolicy(Qt.TabFocus)
        self.SE_Midi_Length_Measures.setChecked(True)

        self.SE_Midi_Length_Layout.addWidget(self.SE_Midi_Length_Measures)

        self.SE_Midi_Length_Beats = QRadioButton(self.SE_Midi_Length)
        self.SE_Midi_Length_Beats.setObjectName(u"SE_Midi_Length_Beats")
        self.SE_Midi_Length_Beats.setFocusPolicy(Qt.TabFocus)
        self.SE_Midi_Length_Beats.setChecked(False)

        self.SE_Midi_Length_Layout.addWidget(self.SE_Midi_Length_Beats)


        self.verticalLayout_8.addLayout(self.SE_Midi_Length_Layout)


        self.SE_Midi_Info.addWidget(self.SE_Midi_Length)

        self.SE_Midi_vLine_2 = QFrame(self.SE_Midi)
        self.SE_Midi_vLine_2.setObjectName(u"SE_Midi_vLine_2")
        self.SE_Midi_vLine_2.setFrameShape(QFrame.VLine)
        self.SE_Midi_vLine_2.setFrameShadow(QFrame.Sunken)

        self.SE_Midi_Info.addWidget(self.SE_Midi_vLine_2)

        self.SE_Midi_TimeSignature = QFrame(self.SE_Midi)
        self.SE_Midi_TimeSignature.setObjectName(u"SE_Midi_TimeSignature")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.SE_Midi_TimeSignature.sizePolicy().hasHeightForWidth())
        self.SE_Midi_TimeSignature.setSizePolicy(sizePolicy4)
        self.verticalLayout_6 = QVBoxLayout(self.SE_Midi_TimeSignature)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.SE_Midi_TimeSignature_Label = QLabel(self.SE_Midi_TimeSignature)
        self.SE_Midi_TimeSignature_Label.setObjectName(u"SE_Midi_TimeSignature_Label")

        self.verticalLayout_6.addWidget(self.SE_Midi_TimeSignature_Label, 0, Qt.AlignTop)

        self.SE_Midi_TimeSignature_Layout = QHBoxLayout()
        self.SE_Midi_TimeSignature_Layout.setObjectName(u"SE_Midi_TimeSignature_Layout")
        self.SE_Midi_TimeSignature_Layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.SE_Midi_TimeSignature_4 = QRadioButton(self.SE_Midi_TimeSignature)
        self.SE_Midi_TimeSignature_4.setObjectName(u"SE_Midi_TimeSignature_4")
        self.SE_Midi_TimeSignature_4.setMouseTracking(True)
        self.SE_Midi_TimeSignature_4.setFocusPolicy(Qt.TabFocus)
        self.SE_Midi_TimeSignature_4.setText(u"4/4")
        self.SE_Midi_TimeSignature_4.setChecked(True)

        self.SE_Midi_TimeSignature_Layout.addWidget(self.SE_Midi_TimeSignature_4)

        self.SE_Midi_TimeSignature_3 = QRadioButton(self.SE_Midi_TimeSignature)
        self.SE_Midi_TimeSignature_3.setObjectName(u"SE_Midi_TimeSignature_3")
        self.SE_Midi_TimeSignature_3.setFocusPolicy(Qt.TabFocus)
        self.SE_Midi_TimeSignature_3.setText(u"3/4")

        self.SE_Midi_TimeSignature_Layout.addWidget(self.SE_Midi_TimeSignature_3)


        self.verticalLayout_6.addLayout(self.SE_Midi_TimeSignature_Layout)


        self.SE_Midi_Info.addWidget(self.SE_Midi_TimeSignature)


        self.verticalLayout_4.addLayout(self.SE_Midi_Info)


        self.SE_MidiAndText.addWidget(self.SE_Midi)

        self.SE_VerticalSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.SE_MidiAndText.addItem(self.SE_VerticalSpacerBottom)

        self.SE_ChangeSongText = QGroupBox(self.SongEditor)
        self.SE_ChangeSongText.setObjectName(u"SE_ChangeSongText")
        self.SE_ChangeSongText.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.SE_ChangeSongText.sizePolicy().hasHeightForWidth())
        self.SE_ChangeSongText.setSizePolicy(sizePolicy2)
        self.SE_ChangeSongText.setContextMenuPolicy(Qt.NoContextMenu)
        self.SE_ChangeSongText.setCheckable(False)
        self.SE_ChangeSongText.setChecked(False)
        self.verticalLayout_5 = QVBoxLayout(self.SE_ChangeSongText)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.SE_ChangeSongText_NameAndGenre = QHBoxLayout()
        self.SE_ChangeSongText_NameAndGenre.setObjectName(u"SE_ChangeSongText_NameAndGenre")
        self.SE_ChangeSongText_Name = QVBoxLayout()
        self.SE_ChangeSongText_Name.setObjectName(u"SE_ChangeSongText_Name")
        self.SE_ChangeSongText_Name_Label = QLabel(self.SE_ChangeSongText)
        self.SE_ChangeSongText_Name_Label.setObjectName(u"SE_ChangeSongText_Name_Label")
        self.SE_ChangeSongText_Name_Label.setMaximumSize(QSize(16777215, 13))

        self.SE_ChangeSongText_Name.addWidget(self.SE_ChangeSongText_Name_Label)

        self.SE_ChangeSongText_Name_Input = QLineEdit(self.SE_ChangeSongText)
        self.SE_ChangeSongText_Name_Input.setObjectName(u"SE_ChangeSongText_Name_Input")
        self.SE_ChangeSongText_Name_Input.setMaximumSize(QSize(16777215, 20))

        self.SE_ChangeSongText_Name.addWidget(self.SE_ChangeSongText_Name_Input)


        self.SE_ChangeSongText_NameAndGenre.addLayout(self.SE_ChangeSongText_Name)

        self.SE_ChangeSongText_vLine = QFrame(self.SE_ChangeSongText)
        self.SE_ChangeSongText_vLine.setObjectName(u"SE_ChangeSongText_vLine")
        self.SE_ChangeSongText_vLine.setFrameShape(QFrame.VLine)
        self.SE_ChangeSongText_vLine.setFrameShadow(QFrame.Sunken)

        self.SE_ChangeSongText_NameAndGenre.addWidget(self.SE_ChangeSongText_vLine)

        self.SE_ChangeSongText_Genre = QVBoxLayout()
        self.SE_ChangeSongText_Genre.setObjectName(u"SE_ChangeSongText_Genre")
        self.SE_ChangeSongText_Genre_Label = QLabel(self.SE_ChangeSongText)
        self.SE_ChangeSongText_Genre_Label.setObjectName(u"SE_ChangeSongText_Genre_Label")
        self.SE_ChangeSongText_Genre_Label.setMaximumSize(QSize(16777215, 13))

        self.SE_ChangeSongText_Genre.addWidget(self.SE_ChangeSongText_Genre_Label)

        self.SE_ChangeSongText_Genre_Input = QLineEdit(self.SE_ChangeSongText)
        self.SE_ChangeSongText_Genre_Input.setObjectName(u"SE_ChangeSongText_Genre_Input")

        self.SE_ChangeSongText_Genre.addWidget(self.SE_ChangeSongText_Genre_Input)


        self.SE_ChangeSongText_NameAndGenre.addLayout(self.SE_ChangeSongText_Genre)


        self.verticalLayout_5.addLayout(self.SE_ChangeSongText_NameAndGenre)

        self.SE_ChangeSongText_hLine = QFrame(self.SE_ChangeSongText)
        self.SE_ChangeSongText_hLine.setObjectName(u"SE_ChangeSongText_hLine")
        self.SE_ChangeSongText_hLine.setFrameShape(QFrame.HLine)
        self.SE_ChangeSongText_hLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.SE_ChangeSongText_hLine)

        self.SE_ChangeSongText_Desc_Label = QLabel(self.SE_ChangeSongText)
        self.SE_ChangeSongText_Desc_Label.setObjectName(u"SE_ChangeSongText_Desc_Label")

        self.verticalLayout_5.addWidget(self.SE_ChangeSongText_Desc_Label)

        self.SE_ChangeSongText_Desc_Input = QTextEdit(self.SE_ChangeSongText)
        self.SE_ChangeSongText_Desc_Input.setObjectName(u"SE_ChangeSongText_Desc_Input")
        self.SE_ChangeSongText_Desc_Input.setMinimumSize(QSize(0, 76))
        self.SE_ChangeSongText_Desc_Input.setMaximumSize(QSize(16777215, 71))

        self.verticalLayout_5.addWidget(self.SE_ChangeSongText_Desc_Input)


        self.SE_MidiAndText.addWidget(self.SE_ChangeSongText)

        self.SE_VerticalSpacerTop = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.SE_MidiAndText.addItem(self.SE_VerticalSpacerTop)

        self.SE_Patch = QPushButton(self.SongEditor)
        self.SE_Patch.setObjectName(u"SE_Patch")
        self.SE_Patch.setMinimumSize(QSize(0, 45))
        font5 = QFont()
        font5.setFamilies([u"Continuum Medium"])
        font5.setPointSize(20)
        self.SE_Patch.setFont(font5)

        self.SE_MidiAndText.addWidget(self.SE_Patch)


        self.SE_MainLayout.addLayout(self.SE_MidiAndText)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.SE_SongToChangeBox = QGroupBox(self.SongEditor)
        self.SE_SongToChangeBox.setObjectName(u"SE_SongToChangeBox")
        self.SE_SongToChangeBox.setMinimumSize(QSize(0, 0))
        self.verticalLayout_3 = QVBoxLayout(self.SE_SongToChangeBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.SE_SongToChange = QListWidget(self.SE_SongToChangeBox)
        self.SE_SongToChange.setObjectName(u"SE_SongToChange")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.SE_SongToChange.sizePolicy().hasHeightForWidth())
        self.SE_SongToChange.setSizePolicy(sizePolicy5)

        self.verticalLayout_3.addWidget(self.SE_SongToChange)

        self.SE_ResetButton = QPushButton(self.SE_SongToChangeBox)
        self.SE_ResetButton.setObjectName(u"SE_ResetButton")

        self.verticalLayout_3.addWidget(self.SE_ResetButton)


        self.verticalLayout_23.addWidget(self.SE_SongToChangeBox)

        self.SE_StyleBox = QGroupBox(self.SongEditor)
        self.SE_StyleBox.setObjectName(u"SE_StyleBox")
        self.verticalLayout_22 = QVBoxLayout(self.SE_StyleBox)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.SE_StyleText = QLabel(self.SE_StyleBox)
        self.SE_StyleText.setObjectName(u"SE_StyleText")
        sizePolicy3.setHeightForWidth(self.SE_StyleText.sizePolicy().hasHeightForWidth())
        self.SE_StyleText.setSizePolicy(sizePolicy3)
        self.SE_StyleText.setAcceptDrops(True)
        self.SE_StyleText.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")

        self.verticalLayout_22.addWidget(self.SE_StyleText)

        self.SE_StyleButtons = QHBoxLayout()
        self.SE_StyleButtons.setObjectName(u"SE_StyleButtons")
        self.SE_OpenStyleEditor = QPushButton(self.SE_StyleBox)
        self.SE_OpenStyleEditor.setObjectName(u"SE_OpenStyleEditor")

        self.SE_StyleButtons.addWidget(self.SE_OpenStyleEditor)

        self.SE_OpenDefaultStyleEditor = QPushButton(self.SE_StyleBox)
        self.SE_OpenDefaultStyleEditor.setObjectName(u"SE_OpenDefaultStyleEditor")

        self.SE_StyleButtons.addWidget(self.SE_OpenDefaultStyleEditor)


        self.verticalLayout_22.addLayout(self.SE_StyleButtons)


        self.verticalLayout_23.addWidget(self.SE_StyleBox)


        self.SE_MainLayout.addLayout(self.verticalLayout_23)


        self.verticalLayout_2.addLayout(self.SE_MainLayout)

        self.MainWidget.addWidget(self.SongEditor)
        self.StyleEditor = QWidget()
        self.StyleEditor.setObjectName(u"StyleEditor")
        self.verticalLayout_10 = QVBoxLayout(self.StyleEditor)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.StE_Title = QHBoxLayout()
        self.StE_Title.setObjectName(u"StE_Title")
        self.StE_Title_Label = QLabel(self.StyleEditor)
        self.StE_Title_Label.setObjectName(u"StE_Title_Label")
        self.StE_Title_Label.setMaximumSize(QSize(16777215, 44))
        self.StE_Title_Label.setFont(font1)

        self.StE_Title.addWidget(self.StE_Title_Label)

        self.StE_Back_Button = QPushButton(self.StyleEditor)
        self.StE_Back_Button.setObjectName(u"StE_Back_Button")
        self.StE_Back_Button.setMaximumSize(QSize(100, 30))
        self.StE_Back_Button.setFont(font4)

        self.StE_Title.addWidget(self.StE_Back_Button)


        self.verticalLayout_10.addLayout(self.StE_Title)

        self.StE_MainLayout = QHBoxLayout()
        self.StE_MainLayout.setObjectName(u"StE_MainLayout")
        self.StE_PartsAndFile = QVBoxLayout()
        self.StE_PartsAndFile.setObjectName(u"StE_PartsAndFile")
        self.StE_Parts = QGroupBox(self.StyleEditor)
        self.StE_Parts.setObjectName(u"StE_Parts")
        self.StE_Parts.setMinimumSize(QSize(200, 0))
        self.StE_Parts.setMaximumSize(QSize(16777215, 300))
        self.StE_Parts.setFocusPolicy(Qt.NoFocus)
        self.StE_Parts.setCheckable(False)
        self.verticalLayout_7 = QVBoxLayout(self.StE_Parts)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.StE_Parts_List = QGridLayout()
        self.StE_Parts_List.setObjectName(u"StE_Parts_List")
        self.StE_Part_Percussion1_Instrument = QLabel(self.StE_Parts)
        self.StE_Part_Percussion1_Instrument.setObjectName(u"StE_Part_Percussion1_Instrument")
        self.StE_Part_Percussion1_Instrument.setStyleSheet(u"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;")
        self.StE_Part_Percussion1_Instrument.setText(u"")

        self.StE_Parts_List.addWidget(self.StE_Part_Percussion1_Instrument, 4, 1, 1, 1)

        self.StE_Part_Bass_Label = QLabel(self.StE_Parts)
        self.StE_Part_Bass_Label.setObjectName(u"StE_Part_Bass_Label")

        self.StE_Parts_List.addWidget(self.StE_Part_Bass_Label, 3, 0, 1, 1)

        self.StE_Part_Percussion1_Label = QLabel(self.StE_Parts)
        self.StE_Part_Percussion1_Label.setObjectName(u"StE_Part_Percussion1_Label")

        self.StE_Parts_List.addWidget(self.StE_Part_Percussion1_Label, 4, 0, 1, 1)

        self.StE_Part_Harmony_Label = QLabel(self.StE_Parts)
        self.StE_Part_Harmony_Label.setObjectName(u"StE_Part_Harmony_Label")

        self.StE_Parts_List.addWidget(self.StE_Part_Harmony_Label, 1, 0, 1, 1)

        self.StE_Part_Bass_Instrument = QLabel(self.StE_Parts)
        self.StE_Part_Bass_Instrument.setObjectName(u"StE_Part_Bass_Instrument")
        self.StE_Part_Bass_Instrument.setStyleSheet(u"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;")
        self.StE_Part_Bass_Instrument.setText(u"")

        self.StE_Parts_List.addWidget(self.StE_Part_Bass_Instrument, 3, 1, 1, 1)

        self.StE_Part_Chords_Instrument = QLabel(self.StE_Parts)
        self.StE_Part_Chords_Instrument.setObjectName(u"StE_Part_Chords_Instrument")
        self.StE_Part_Chords_Instrument.setStyleSheet(u"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;")
        self.StE_Part_Chords_Instrument.setText(u"")

        self.StE_Parts_List.addWidget(self.StE_Part_Chords_Instrument, 2, 1, 1, 1)

        self.StE_Part_Harmony_Instrument = QLabel(self.StE_Parts)
        self.StE_Part_Harmony_Instrument.setObjectName(u"StE_Part_Harmony_Instrument")
        self.StE_Part_Harmony_Instrument.setStyleSheet(u"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;")
        self.StE_Part_Harmony_Instrument.setText(u"")

        self.StE_Parts_List.addWidget(self.StE_Part_Harmony_Instrument, 1, 1, 1, 1)

        self.StE_Part_Chords_Label = QLabel(self.StE_Parts)
        self.StE_Part_Chords_Label.setObjectName(u"StE_Part_Chords_Label")

        self.StE_Parts_List.addWidget(self.StE_Part_Chords_Label, 2, 0, 1, 1)

        self.StE_Part_Percussion2_Label = QLabel(self.StE_Parts)
        self.StE_Part_Percussion2_Label.setObjectName(u"StE_Part_Percussion2_Label")

        self.StE_Parts_List.addWidget(self.StE_Part_Percussion2_Label, 5, 0, 1, 1)

        self.StE_Part_Percussion2_Instrument = QLabel(self.StE_Parts)
        self.StE_Part_Percussion2_Instrument.setObjectName(u"StE_Part_Percussion2_Instrument")
        self.StE_Part_Percussion2_Instrument.setStyleSheet(u"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;")
        self.StE_Part_Percussion2_Instrument.setText(u"")

        self.StE_Parts_List.addWidget(self.StE_Part_Percussion2_Instrument, 5, 1, 1, 1)

        self.StE_Part_Melody_Instrument = QLabel(self.StE_Parts)
        self.StE_Part_Melody_Instrument.setObjectName(u"StE_Part_Melody_Instrument")
        sizePolicy.setHeightForWidth(self.StE_Part_Melody_Instrument.sizePolicy().hasHeightForWidth())
        self.StE_Part_Melody_Instrument.setSizePolicy(sizePolicy)
        self.StE_Part_Melody_Instrument.setStyleSheet(u"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;")
        self.StE_Part_Melody_Instrument.setText(u"")

        self.StE_Parts_List.addWidget(self.StE_Part_Melody_Instrument, 0, 1, 1, 1)

        self.StE_Part_Melody_Label = QLabel(self.StE_Parts)
        self.StE_Part_Melody_Label.setObjectName(u"StE_Part_Melody_Label")

        self.StE_Parts_List.addWidget(self.StE_Part_Melody_Label, 0, 0, 1, 1)


        self.verticalLayout_7.addLayout(self.StE_Parts_List)

        self.StE_ResetStyle = QPushButton(self.StE_Parts)
        self.StE_ResetStyle.setObjectName(u"StE_ResetStyle")

        self.verticalLayout_7.addWidget(self.StE_ResetStyle)


        self.StE_PartsAndFile.addWidget(self.StE_Parts)

        self.StE_PartsAndFile_Spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.StE_PartsAndFile.addItem(self.StE_PartsAndFile_Spacer)

        self.StE_Patch = QPushButton(self.StyleEditor)
        self.StE_Patch.setObjectName(u"StE_Patch")
        self.StE_Patch.setMinimumSize(QSize(0, 45))
        self.StE_Patch.setFont(font5)

        self.StE_PartsAndFile.addWidget(self.StE_Patch)


        self.StE_MainLayout.addLayout(self.StE_PartsAndFile)

        self.StE_Instruments = QGroupBox(self.StyleEditor)
        self.StE_Instruments.setObjectName(u"StE_Instruments")
        self.StE_Instruments.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_32 = QVBoxLayout(self.StE_Instruments)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.StE_InstrumentList = QListWidget(self.StE_Instruments)
        self.StE_InstrumentList.setObjectName(u"StE_InstrumentList")

        self.verticalLayout_32.addWidget(self.StE_InstrumentList)

        self.StE_PartSelector_Layout = QHBoxLayout()
        self.StE_PartSelector_Layout.setObjectName(u"StE_PartSelector_Layout")
        self.StE_PartSelector_Label = QLabel(self.StE_Instruments)
        self.StE_PartSelector_Label.setObjectName(u"StE_PartSelector_Label")

        self.StE_PartSelector_Layout.addWidget(self.StE_PartSelector_Label)

        self.StE_PartSelector = QComboBox(self.StE_Instruments)
        self.StE_PartSelector.addItem("")
        self.StE_PartSelector.addItem("")
        self.StE_PartSelector.addItem("")
        self.StE_PartSelector.addItem("")
        self.StE_PartSelector.addItem("")
        self.StE_PartSelector.addItem("")
        self.StE_PartSelector.setObjectName(u"StE_PartSelector")

        self.StE_PartSelector_Layout.addWidget(self.StE_PartSelector)


        self.verticalLayout_32.addLayout(self.StE_PartSelector_Layout)


        self.StE_MainLayout.addWidget(self.StE_Instruments)

        self.StE_Styles = QGroupBox(self.StyleEditor)
        self.StE_Styles.setObjectName(u"StE_Styles")
        self.StE_Styles.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_13 = QVBoxLayout(self.StE_Styles)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.StE_StyleList = QListWidget(self.StE_Styles)
        self.StE_StyleList.setObjectName(u"StE_StyleList")

        self.verticalLayout_13.addWidget(self.StE_StyleList)

        self.StE_ChangeStyleName_Layout = QHBoxLayout()
        self.StE_ChangeStyleName_Layout.setObjectName(u"StE_ChangeStyleName_Layout")
        self.StE_ChangeStyleName_Label = QLabel(self.StE_Styles)
        self.StE_ChangeStyleName_Label.setObjectName(u"StE_ChangeStyleName_Label")

        self.StE_ChangeStyleName_Layout.addWidget(self.StE_ChangeStyleName_Label)

        self.StE_ChangeStyleName = QLineEdit(self.StE_Styles)
        self.StE_ChangeStyleName.setObjectName(u"StE_ChangeStyleName")
        self.StE_ChangeStyleName.setMaximumSize(QSize(16777215, 20))

        self.StE_ChangeStyleName_Layout.addWidget(self.StE_ChangeStyleName)


        self.verticalLayout_13.addLayout(self.StE_ChangeStyleName_Layout)


        self.StE_MainLayout.addWidget(self.StE_Styles)


        self.verticalLayout_10.addLayout(self.StE_MainLayout)

        self.MainWidget.addWidget(self.StyleEditor)
        self.TextEditor = QWidget()
        self.TextEditor.setObjectName(u"TextEditor")
        self.verticalLayout_12 = QVBoxLayout(self.TextEditor)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.TE_Title = QHBoxLayout()
        self.TE_Title.setObjectName(u"TE_Title")
        self.TE_Title_Label = QLabel(self.TextEditor)
        self.TE_Title_Label.setObjectName(u"TE_Title_Label")
        self.TE_Title_Label.setMaximumSize(QSize(16777215, 44))
        self.TE_Title_Label.setFont(font1)

        self.TE_Title.addWidget(self.TE_Title_Label)

        self.TE_Back_Button = QPushButton(self.TextEditor)
        self.TE_Back_Button.setObjectName(u"TE_Back_Button")
        self.TE_Back_Button.setMaximumSize(QSize(100, 30))
        self.TE_Back_Button.setFont(font4)

        self.TE_Title.addWidget(self.TE_Back_Button)


        self.verticalLayout_12.addLayout(self.TE_Title)

        self.TE_Text = QPlainTextEdit(self.TextEditor)
        self.TE_Text.setObjectName(u"TE_Text")

        self.verticalLayout_12.addWidget(self.TE_Text)

        self.TE_Buttons = QHBoxLayout()
        self.TE_Buttons.setObjectName(u"TE_Buttons")
        self.TE_OpenExternal = QPushButton(self.TextEditor)
        self.TE_OpenExternal.setObjectName(u"TE_OpenExternal")
        self.TE_OpenExternal.setMinimumSize(QSize(0, 45))
        self.TE_OpenExternal.setFont(font5)

        self.TE_Buttons.addWidget(self.TE_OpenExternal)

        self.TE_Patch = QPushButton(self.TextEditor)
        self.TE_Patch.setObjectName(u"TE_Patch")
        self.TE_Patch.setMinimumSize(QSize(0, 45))
        self.TE_Patch.setFont(font5)

        self.TE_Buttons.addWidget(self.TE_Patch)


        self.verticalLayout_12.addLayout(self.TE_Buttons)

        self.MainWidget.addWidget(self.TextEditor)
        self.DefaultStyleEditor = QWidget()
        self.DefaultStyleEditor.setObjectName(u"DefaultStyleEditor")
        self.verticalLayout_14 = QVBoxLayout(self.DefaultStyleEditor)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.DS_Title = QHBoxLayout()
        self.DS_Title.setObjectName(u"DS_Title")
        self.DS_Title_Label = QLabel(self.DefaultStyleEditor)
        self.DS_Title_Label.setObjectName(u"DS_Title_Label")
        self.DS_Title_Label.setMaximumSize(QSize(16777215, 44))
        self.DS_Title_Label.setFont(font1)

        self.DS_Title.addWidget(self.DS_Title_Label)

        self.DS_Back_Button = QPushButton(self.DefaultStyleEditor)
        self.DS_Back_Button.setObjectName(u"DS_Back_Button")
        self.DS_Back_Button.setMaximumSize(QSize(100, 30))
        self.DS_Back_Button.setFont(font4)

        self.DS_Title.addWidget(self.DS_Back_Button)


        self.verticalLayout_14.addLayout(self.DS_Title)

        self.DS_Lists = QHBoxLayout()
        self.DS_Lists.setObjectName(u"DS_Lists")
        self.DS_SongBox = QGroupBox(self.DefaultStyleEditor)
        self.DS_SongBox.setObjectName(u"DS_SongBox")
        self.verticalLayout_15 = QVBoxLayout(self.DS_SongBox)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.DS_Songs = QListWidget(self.DS_SongBox)
        self.DS_Songs.setObjectName(u"DS_Songs")

        self.verticalLayout_15.addWidget(self.DS_Songs)


        self.DS_Lists.addWidget(self.DS_SongBox)

        self.DS_StyleBox = QGroupBox(self.DefaultStyleEditor)
        self.DS_StyleBox.setObjectName(u"DS_StyleBox")
        self.verticalLayout_16 = QVBoxLayout(self.DS_StyleBox)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.DS_Styles = QListWidget(self.DS_StyleBox)
        self.DS_Styles.setObjectName(u"DS_Styles")

        self.verticalLayout_16.addWidget(self.DS_Styles)

        self.DS_Reset = QPushButton(self.DS_StyleBox)
        self.DS_Reset.setObjectName(u"DS_Reset")

        self.verticalLayout_16.addWidget(self.DS_Reset)


        self.DS_Lists.addWidget(self.DS_StyleBox)


        self.verticalLayout_14.addLayout(self.DS_Lists)

        self.DS_Patch = QPushButton(self.DefaultStyleEditor)
        self.DS_Patch.setObjectName(u"DS_Patch")
        self.DS_Patch.setMinimumSize(QSize(0, 45))
        self.DS_Patch.setFont(font5)

        self.verticalLayout_14.addWidget(self.DS_Patch)

        self.MainWidget.addWidget(self.DefaultStyleEditor)
        self.RemoveSong = QWidget()
        self.RemoveSong.setObjectName(u"RemoveSong")
        self.verticalLayout_20 = QVBoxLayout(self.RemoveSong)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.RS_Title = QHBoxLayout()
        self.RS_Title.setObjectName(u"RS_Title")
        self.RS_Title_Label = QLabel(self.RemoveSong)
        self.RS_Title_Label.setObjectName(u"RS_Title_Label")
        self.RS_Title_Label.setMaximumSize(QSize(16777215, 44))
        self.RS_Title_Label.setFont(font1)

        self.RS_Title.addWidget(self.RS_Title_Label)

        self.RS_Back_Button = QPushButton(self.RemoveSong)
        self.RS_Back_Button.setObjectName(u"RS_Back_Button")
        self.RS_Back_Button.setMaximumSize(QSize(100, 30))
        self.RS_Back_Button.setFont(font4)

        self.RS_Title.addWidget(self.RS_Back_Button)


        self.verticalLayout_20.addLayout(self.RS_Title)

        self.RS_SongBox = QGroupBox(self.RemoveSong)
        self.RS_SongBox.setObjectName(u"RS_SongBox")
        self.verticalLayout_19 = QVBoxLayout(self.RS_SongBox)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.RS_Songs = QListWidget(self.RS_SongBox)
        self.RS_Songs.setObjectName(u"RS_Songs")
        self.RS_Songs.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.RS_Songs.setMovement(QListView.Static)

        self.verticalLayout_19.addWidget(self.RS_Songs)


        self.verticalLayout_20.addWidget(self.RS_SongBox)

        self.RS_Buttons = QHBoxLayout()
        self.RS_Buttons.setObjectName(u"RS_Buttons")
        self.RS_RemoveCustomSongs = QPushButton(self.RemoveSong)
        self.RS_RemoveCustomSongs.setObjectName(u"RS_RemoveCustomSongs")

        self.RS_Buttons.addWidget(self.RS_RemoveCustomSongs)

        self.RS_Deselect_Button = QPushButton(self.RemoveSong)
        self.RS_Deselect_Button.setObjectName(u"RS_Deselect_Button")

        self.RS_Buttons.addWidget(self.RS_Deselect_Button)


        self.verticalLayout_20.addLayout(self.RS_Buttons)

        self.RS_Patch = QPushButton(self.RemoveSong)
        self.RS_Patch.setObjectName(u"RS_Patch")
        self.RS_Patch.setMinimumSize(QSize(0, 45))
        self.RS_Patch.setFont(font5)

        self.verticalLayout_20.addWidget(self.RS_Patch)

        self.MainWidget.addWidget(self.RemoveSong)
        self.SoundEditor = QWidget()
        self.SoundEditor.setObjectName(u"SoundEditor")
        self.verticalLayout_44 = QVBoxLayout(self.SoundEditor)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.SOE_Title = QHBoxLayout()
        self.SOE_Title.setObjectName(u"SOE_Title")
        self.SOE_Title_Label = QLabel(self.SoundEditor)
        self.SOE_Title_Label.setObjectName(u"SOE_Title_Label")
        self.SOE_Title_Label.setMaximumSize(QSize(16777215, 44))
        self.SOE_Title_Label.setFont(font1)

        self.SOE_Title.addWidget(self.SOE_Title_Label)

        self.SOE_Back_Button = QPushButton(self.SoundEditor)
        self.SOE_Back_Button.setObjectName(u"SOE_Back_Button")
        self.SOE_Back_Button.setMaximumSize(QSize(100, 30))
        self.SOE_Back_Button.setFont(font4)

        self.SOE_Title.addWidget(self.SOE_Back_Button)


        self.verticalLayout_44.addLayout(self.SOE_Title)

        self.SOE_Lists = QHBoxLayout()
        self.SOE_Lists.setObjectName(u"SOE_Lists")
        self.SOE_SoundBox = QGroupBox(self.SoundEditor)
        self.SOE_SoundBox.setObjectName(u"SOE_SoundBox")
        self.verticalLayout_42 = QVBoxLayout(self.SOE_SoundBox)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.SOE_Sounds = QListWidget(self.SOE_SoundBox)
        self.SOE_Sounds.setObjectName(u"SOE_Sounds")

        self.verticalLayout_42.addWidget(self.SOE_Sounds)


        self.SOE_Lists.addWidget(self.SOE_SoundBox)

        self.SOE_RightLayout = QVBoxLayout()
        self.SOE_RightLayout.setObjectName(u"SOE_RightLayout")
        self.SOE_File = QGroupBox(self.SoundEditor)
        self.SOE_File.setObjectName(u"SOE_File")
        self.horizontalLayout = QHBoxLayout(self.SOE_File)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.SOE_File_Label = QLabel(self.SOE_File)
        self.SOE_File_Label.setObjectName(u"SOE_File_Label")
        sizePolicy3.setHeightForWidth(self.SOE_File_Label.sizePolicy().hasHeightForWidth())
        self.SOE_File_Label.setSizePolicy(sizePolicy3)
        self.SOE_File_Label.setStyleSheet(u"QLabel\n"
"{\n"
"padding: 1px;\n"
"border: 1px solid;\n"
"border-color: #1e1e1e;\n"
"background-color: #242424;\n"
"padding-top: 6px;\n"
"padding-bottom: 6px;\n"
"}")
        self.SOE_File_Label.setText(u"Load a Wav-Type file")

        self.horizontalLayout.addWidget(self.SOE_File_Label)

        self.SOE_File_Browse = QPushButton(self.SOE_File)
        self.SOE_File_Browse.setObjectName(u"SOE_File_Browse")
        self.SOE_File_Browse.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.SOE_File_Browse)


        self.SOE_RightLayout.addWidget(self.SOE_File)

        self.SOE_Loop = QGroupBox(self.SoundEditor)
        self.SOE_Loop.setObjectName(u"SOE_Loop")
        self.SOE_Loop.setCheckable(True)
        self.SOE_Loop.setChecked(False)
        self.verticalLayout_21 = QVBoxLayout(self.SOE_Loop)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.SOE_LoopLayout = QHBoxLayout()
        self.SOE_LoopLayout.setObjectName(u"SOE_LoopLayout")
        self.SOE_LoopStartLabel = QLabel(self.SOE_Loop)
        self.SOE_LoopStartLabel.setObjectName(u"SOE_LoopStartLabel")

        self.SOE_LoopLayout.addWidget(self.SOE_LoopStartLabel)

        self.SOE_LoopStart = QDoubleSpinBox(self.SOE_Loop)
        self.SOE_LoopStart.setObjectName(u"SOE_LoopStart")
        self.SOE_LoopStart.setDecimals(3)
        self.SOE_LoopStart.setMaximum(10000000.000000000000000)

        self.SOE_LoopLayout.addWidget(self.SOE_LoopStart)

        self.SOE_LoopLine = QFrame(self.SOE_Loop)
        self.SOE_LoopLine.setObjectName(u"SOE_LoopLine")
        self.SOE_LoopLine.setFrameShape(QFrame.VLine)
        self.SOE_LoopLine.setFrameShadow(QFrame.Sunken)

        self.SOE_LoopLayout.addWidget(self.SOE_LoopLine)

        self.SOE_LoopEndLabel = QLabel(self.SOE_Loop)
        self.SOE_LoopEndLabel.setObjectName(u"SOE_LoopEndLabel")

        self.SOE_LoopLayout.addWidget(self.SOE_LoopEndLabel)

        self.SOE_LoopEnd = QDoubleSpinBox(self.SOE_Loop)
        self.SOE_LoopEnd.setObjectName(u"SOE_LoopEnd")
        self.SOE_LoopEnd.setDecimals(3)
        self.SOE_LoopEnd.setMaximum(10000000.000000000000000)

        self.SOE_LoopLayout.addWidget(self.SOE_LoopEnd)


        self.verticalLayout_21.addLayout(self.SOE_LoopLayout)

        self.SOE_LoopLineH = QFrame(self.SOE_Loop)
        self.SOE_LoopLineH.setObjectName(u"SOE_LoopLineH")
        self.SOE_LoopLineH.setFrameShape(QFrame.HLine)
        self.SOE_LoopLineH.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_21.addWidget(self.SOE_LoopLineH)

        self.SOE_LoopMesurementsLayout = QHBoxLayout()
        self.SOE_LoopMesurementsLayout.setObjectName(u"SOE_LoopMesurementsLayout")
        self.SOE_LoopMesurementsLabel = QLabel(self.SOE_Loop)
        self.SOE_LoopMesurementsLabel.setObjectName(u"SOE_LoopMesurementsLabel")

        self.SOE_LoopMesurementsLayout.addWidget(self.SOE_LoopMesurementsLabel)

        self.SOE_LoopSeconds = QRadioButton(self.SOE_Loop)
        self.SOE_LoopSeconds.setObjectName(u"SOE_LoopSeconds")
        self.SOE_LoopSeconds.setChecked(True)

        self.SOE_LoopMesurementsLayout.addWidget(self.SOE_LoopSeconds)

        self.SOE_LoopSamples = QRadioButton(self.SOE_Loop)
        self.SOE_LoopSamples.setObjectName(u"SOE_LoopSamples")

        self.SOE_LoopMesurementsLayout.addWidget(self.SOE_LoopSamples)


        self.verticalLayout_21.addLayout(self.SOE_LoopMesurementsLayout)


        self.SOE_RightLayout.addWidget(self.SOE_Loop)

        self.SOE_SoundTypeBox = QGroupBox(self.SoundEditor)
        self.SOE_SoundTypeBox.setObjectName(u"SOE_SoundTypeBox")
        self.verticalLayout_43 = QVBoxLayout(self.SOE_SoundTypeBox)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.SOE_SoundType = QListWidget(self.SOE_SoundTypeBox)
        self.SOE_SoundType.setObjectName(u"SOE_SoundType")
        self.SOE_SoundType.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.SOE_SoundType.setMovement(QListView.Static)

        self.verticalLayout_43.addWidget(self.SOE_SoundType)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.SOE_SelectAll = QPushButton(self.SOE_SoundTypeBox)
        self.SOE_SelectAll.setObjectName(u"SOE_SelectAll")

        self.horizontalLayout_2.addWidget(self.SOE_SelectAll)

        self.SOE_PlayAudio = QPushButton(self.SOE_SoundTypeBox)
        self.SOE_PlayAudio.setObjectName(u"SOE_PlayAudio")

        self.horizontalLayout_2.addWidget(self.SOE_PlayAudio)


        self.verticalLayout_43.addLayout(self.horizontalLayout_2)


        self.SOE_RightLayout.addWidget(self.SOE_SoundTypeBox)


        self.SOE_Lists.addLayout(self.SOE_RightLayout)


        self.verticalLayout_44.addLayout(self.SOE_Lists)

        self.SOE_Patch = QPushButton(self.SoundEditor)
        self.SOE_Patch.setObjectName(u"SOE_Patch")
        self.SOE_Patch.setMinimumSize(QSize(0, 45))
        self.SOE_Patch.setFont(font5)

        self.verticalLayout_44.addWidget(self.SOE_Patch)

        self.MainWidget.addWidget(self.SoundEditor)

        self.verticalLayout_17.addWidget(self.MainWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 869, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.MB_Options = QMenu(self.menubar)
        self.MB_Options.setObjectName(u"MB_Options")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.MB_Options.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.MB_LoadFile)
        self.menuFile.addAction(self.MB_LoadFolder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.MB_Dolphin)
        self.menuFile.addAction(self.MB_DolphinMenu)
        self.menuFile.addSeparator()
        self.MB_Options.addAction(self.MB_Settings)
        self.MB_Options.addSeparator()
        self.MB_Options.addAction(self.MB_DownloadSongs)
        self.MB_Options.addAction(self.MB_SaveFile)
        self.MB_Options.addSeparator()
        self.MB_Options.addAction(self.MB_Updates)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.MB_Help)
        self.menuHelp.addAction(self.MB_Discord)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.MB_Donate)

        self.retranslateUi(MainWindow)

        self.MainWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.MB_LoadFile.setText(QCoreApplication.translate("MainWindow", u"Load Wii Music File", None))
        self.MB_LoadFolder.setText(QCoreApplication.translate("MainWindow", u"Load Wii Music Folder", None))
        self.MB_Dolphin.setText(QCoreApplication.translate("MainWindow", u"Run Dolphin", None))
#if QT_CONFIG(shortcut)
        self.MB_Dolphin.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.MB_DolphinMenu.setText(QCoreApplication.translate("MainWindow", u"Run Dolphin (Menu)", None))
#if QT_CONFIG(tooltip)
        self.MB_DolphinMenu.setToolTip(QCoreApplication.translate("MainWindow", u"Run Dolphin (Menu)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.MB_DolphinMenu.setShortcut(QCoreApplication.translate("MainWindow", u"F6", None))
#endif // QT_CONFIG(shortcut)
        self.MB_Updates.setText(QCoreApplication.translate("MainWindow", u"Check for Updates", None))
        self.MB_Settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.MB_DownloadSongs.setText(QCoreApplication.translate("MainWindow", u"Download Pre-made Songs", None))
        self.MB_Help.setText(QCoreApplication.translate("MainWindow", u"Open Wiki", None))
        self.MB_SaveFolder.setText(QCoreApplication.translate("MainWindow", u"Open Save Folder", None))
        self.MB_SaveFile.setText(QCoreApplication.translate("MainWindow", u"Add 100% Save File to Dolphin", None))
        self.MB_Documentation.setText(QCoreApplication.translate("MainWindow", u"Game Documentation", None))
        self.MB_About.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.MB_Donate.setText(QCoreApplication.translate("MainWindow", u"Donate", None))
        self.MP_LoadedFile_Label.setText(QCoreApplication.translate("MainWindow", u"Currently loaded folder:", None))
        self.MP_LoadedFile_Path.setText(QCoreApplication.translate("MainWindow", u"No folder loaded", None))
        self.MP_Rom_Region_Label.setText(QCoreApplication.translate("MainWindow", u"Rom region:", None))
        self.MP_RomInfo_Language_Label.setText(QCoreApplication.translate("MainWindow", u"Rom langauge:", None))
        self.MP_SongEditor_Button.setText(QCoreApplication.translate("MainWindow", u"Song Editor", None))
        self.MP_StyleEditor_Button.setText(QCoreApplication.translate("MainWindow", u"Style Editor", None))
        self.MP_Advanced.setTitle(QCoreApplication.translate("MainWindow", u"Advanced features", None))
        self.MP_EditText_Button.setText(QCoreApplication.translate("MainWindow", u"Change All Text", None))
        self.MP_DefaultStyle_Button.setText(QCoreApplication.translate("MainWindow", u"Change Default Styles", None))
        self.MP_RemoveSong_Button.setText(QCoreApplication.translate("MainWindow", u"Remove Song", None))
        self.MP_Package.setTitle(QCoreApplication.translate("MainWindow", u"Package for Wii", None))
        self.MP_Riivolution_Button.setText(QCoreApplication.translate("MainWindow", u"Create Riivolution Patch", None))
        self.MP_PackRom_Button.setText(QCoreApplication.translate("MainWindow", u"Pack Rom Filesystem", None))
        self.MP_RomEditing.setTitle(QCoreApplication.translate("MainWindow", u"Reset, Import, and Export", None))
        self.MP_RevertChanges_Button.setText(QCoreApplication.translate("MainWindow", u"Revert Changes", None))
        self.MP_ImportFiles_Button.setText(QCoreApplication.translate("MainWindow", u"Import Files", None))
        self.MP_ExportFiles_Button.setText(QCoreApplication.translate("MainWindow", u"Export Files", None))
        self.MP_ImportChanges_Button.setText(QCoreApplication.translate("MainWindow", u"Import Changes", None))
        self.SE_Title.setText(QCoreApplication.translate("MainWindow", u"Song Editor", None))
        self.SE_Back_Button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.SE_Midi.setTitle(QCoreApplication.translate("MainWindow", u"Replace Song", None))
        self.SE_Midi_File_Score_Button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.SE_Midi_File_Score_Title.setText(QCoreApplication.translate("MainWindow", u"SCORE:", None))
        self.SE_Midi_File_Song_Title.setText(QCoreApplication.translate("MainWindow", u"SONG:", None))
        self.SE_Midi_File_Song_Button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.SE_Midi_File_Replace_Song.setText(QCoreApplication.translate("MainWindow", u"Replace SONG seperatly", None))
        self.SE_Midi_Tempo_Label.setText(QCoreApplication.translate("MainWindow", u"Tempo:", None))
        self.SE_Midi_Length_Label.setText(QCoreApplication.translate("MainWindow", u"Length:", None))
        self.SE_Midi_Length_Measures.setText(QCoreApplication.translate("MainWindow", u"Measures", None))
        self.SE_Midi_Length_Beats.setText(QCoreApplication.translate("MainWindow", u"Beats", None))
        self.SE_Midi_TimeSignature_Label.setText(QCoreApplication.translate("MainWindow", u"Time Signature:", None))
        self.SE_ChangeSongText.setTitle(QCoreApplication.translate("MainWindow", u"Change Song Text", None))
        self.SE_ChangeSongText_Name_Label.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.SE_ChangeSongText_Name_Input.setText("")
        self.SE_ChangeSongText_Genre_Label.setText(QCoreApplication.translate("MainWindow", u"Genre:", None))
        self.SE_ChangeSongText_Genre_Input.setText("")
        self.SE_ChangeSongText_Desc_Label.setText(QCoreApplication.translate("MainWindow", u"Description:", None))
        self.SE_Patch.setText(QCoreApplication.translate("MainWindow", u"Patch!", None))
        self.SE_SongToChangeBox.setTitle(QCoreApplication.translate("MainWindow", u"Song to change", None))
        self.SE_ResetButton.setText(QCoreApplication.translate("MainWindow", u"Reset to Default", None))
        self.SE_StyleBox.setTitle(QCoreApplication.translate("MainWindow", u"Style", None))
        self.SE_StyleText.setText("")
        self.SE_OpenStyleEditor.setText(QCoreApplication.translate("MainWindow", u"Edit in Style Editor", None))
        self.SE_OpenDefaultStyleEditor.setText(QCoreApplication.translate("MainWindow", u"Change Default Style", None))
        self.StE_Title_Label.setText(QCoreApplication.translate("MainWindow", u"Style Editor", None))
        self.StE_Back_Button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.StE_Parts.setTitle(QCoreApplication.translate("MainWindow", u"Parts", None))
        self.StE_Part_Bass_Label.setText(QCoreApplication.translate("MainWindow", u"Bass:", None))
        self.StE_Part_Percussion1_Label.setText(QCoreApplication.translate("MainWindow", u"Perc 1:", None))
        self.StE_Part_Harmony_Label.setText(QCoreApplication.translate("MainWindow", u"Harmony:", None))
        self.StE_Part_Chords_Label.setText(QCoreApplication.translate("MainWindow", u"Chords:", None))
        self.StE_Part_Percussion2_Label.setText(QCoreApplication.translate("MainWindow", u"Perc 2:", None))
        self.StE_Part_Melody_Label.setText(QCoreApplication.translate("MainWindow", u"Melody:", None))
        self.StE_ResetStyle.setText(QCoreApplication.translate("MainWindow", u"Reset to Default", None))
        self.StE_Patch.setText(QCoreApplication.translate("MainWindow", u"Patch!", None))
        self.StE_Instruments.setTitle(QCoreApplication.translate("MainWindow", u"Instruments", None))
        self.StE_PartSelector_Label.setText(QCoreApplication.translate("MainWindow", u"Part to Change:", None))
        self.StE_PartSelector.setItemText(0, QCoreApplication.translate("MainWindow", u"Melody", None))
        self.StE_PartSelector.setItemText(1, QCoreApplication.translate("MainWindow", u"Harmony", None))
        self.StE_PartSelector.setItemText(2, QCoreApplication.translate("MainWindow", u"Chords", None))
        self.StE_PartSelector.setItemText(3, QCoreApplication.translate("MainWindow", u"Bass", None))
        self.StE_PartSelector.setItemText(4, QCoreApplication.translate("MainWindow", u"Percussion 1", None))
        self.StE_PartSelector.setItemText(5, QCoreApplication.translate("MainWindow", u"Percussion 2", None))

        self.StE_Styles.setTitle(QCoreApplication.translate("MainWindow", u"Style to change", None))
        self.StE_ChangeStyleName_Label.setText(QCoreApplication.translate("MainWindow", u"Style Name:", None))
        self.StE_ChangeStyleName.setText("")
        self.TE_Title_Label.setText(QCoreApplication.translate("MainWindow", u"Text Editor", None))
        self.TE_Back_Button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.TE_OpenExternal.setText(QCoreApplication.translate("MainWindow", u"Open in External Editor", None))
        self.TE_Patch.setText(QCoreApplication.translate("MainWindow", u"Patch!", None))
        self.DS_Title_Label.setText(QCoreApplication.translate("MainWindow", u"Default Style Editor", None))
        self.DS_Back_Button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.DS_SongBox.setTitle(QCoreApplication.translate("MainWindow", u"Song List", None))
        self.DS_StyleBox.setTitle(QCoreApplication.translate("MainWindow", u"Style List", None))
        self.DS_Reset.setText(QCoreApplication.translate("MainWindow", u"Set to Default", None))
        self.DS_Patch.setText(QCoreApplication.translate("MainWindow", u"Patch!", None))
        self.RS_Title_Label.setText(QCoreApplication.translate("MainWindow", u"Remove Songs", None))
        self.RS_Back_Button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.RS_SongBox.setTitle(QCoreApplication.translate("MainWindow", u"Song List", None))
        self.RS_RemoveCustomSongs.setText(QCoreApplication.translate("MainWindow", u"Remove All Non-Custom Songs", None))
        self.RS_Deselect_Button.setText(QCoreApplication.translate("MainWindow", u"Deselect All", None))
        self.RS_Patch.setText(QCoreApplication.translate("MainWindow", u"Purge Songs!!!", None))
        self.SOE_Title_Label.setText(QCoreApplication.translate("MainWindow", u"Sound Editor", None))
        self.SOE_Back_Button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.SOE_SoundBox.setTitle(QCoreApplication.translate("MainWindow", u"Sound List", None))
        self.SOE_File.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.SOE_File_Browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.SOE_Loop.setTitle(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.SOE_LoopStartLabel.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.SOE_LoopEndLabel.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.SOE_LoopMesurementsLabel.setText(QCoreApplication.translate("MainWindow", u"Measurements:", None))
        self.SOE_LoopSeconds.setText(QCoreApplication.translate("MainWindow", u"Seconds", None))
        self.SOE_LoopSamples.setText(QCoreApplication.translate("MainWindow", u"Samples", None))
        self.SOE_SoundTypeBox.setTitle(QCoreApplication.translate("MainWindow", u"Sound Types", None))
        self.SOE_SelectAll.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
        self.SOE_PlayAudio.setText(QCoreApplication.translate("MainWindow", u"Play Audio", None))
        self.SOE_Patch.setText(QCoreApplication.translate("MainWindow", u"Patch!", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.MB_Options.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        pass
    # retranslateUi

