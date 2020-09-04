from os import path

from PySide2 import QtCore, QtGui, QtWidgets


BASEDIR, _ = path.split(path.realpath(__file__))


class Resources():
    ALERT_ICON = path.join(BASEDIR, '../resources/pd_alert.png')
    ACK_ICON = path.join(BASEDIR, '../resources/pd_ack.png')
    OK_ICON = path.join(BASEDIR, '../resources/pd_ok2.png')


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon(Resources.OK_ICON), parent)
        self.setToolTip('PagerDuty Check')
        self.menu = QtWidgets.QMenu(parent)
        self.add_exit_menu_item()

    def add_exit_menu_item(self) -> None:
        self.menu.addSeparator()
        exit_item = self.menu.addAction('Exit')
        exit_item.triggered.connect(self.exit)
        self.setContextMenu(self.menu)

    def exit(self) -> None:
        self.hide()
        QtCore.QCoreApplication.exit()


class Check():
