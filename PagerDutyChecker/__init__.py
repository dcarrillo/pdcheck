import webbrowser
from os import path
from typing import Dict, List

from PySide2 import QtCore, QtGui, QtWidgets

import pdpyras


BASEDIR, _ = path.split(path.realpath(__file__))


class Resources():
    ALERT_ICON = path.join(BASEDIR, '../resources/pd_alert.png')
    ACK_ICON = path.join(BASEDIR, '../resources/pd_ack.png')
    OK_ICON = path.join(BASEDIR, '../resources/pd_ok.png')


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None, conf: Dict = dict()):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon(Resources.OK_ICON), parent)
        self.setToolTip('PagerDuty Check')
        self.conf = conf
        self.menu = QtWidgets.QMenu(parent)
        self.add_exit_menu_item()
        self.update_incidents()

    def add_exit_menu_item(self) -> None:
        self.menu.addSeparator()
        exit_item = self.menu.addAction('Exit')
        exit_item.triggered.connect(self.exit)
        self.setContextMenu(self.menu)

    def update_incidents(self) -> None:
        incidents = self._check_pager_duty()
        incidents.sort(key=lambda k: k['status'])

        icon = QtGui.QIcon(Resources.OK_ICON)
        self.menu.clear()
        for incident in incidents:
            print(incident)
            if incident['status'] == 'acknowledged':
                icon = QtGui.QIcon(Resources.ACK_ICON)
            else:
                icon = QtGui.QIcon(Resources.ALERT_ICON)

            action = self.menu.addAction(icon, f'{incident["created_at"]} {incident["title"]}')
            action.triggered.connect(
                lambda f=webbrowser.open, url=incident['html_url']: webbrowser.open(url)
            )

        self.add_exit_menu_item()
        self.setIcon(icon)

    def _check_pager_duty(self) -> List:
        pd_session = pdpyras.APISession(self.conf['pd_api_key'])
        incidents = pd_session.list_all('incidents',
                                        params={
                                            'team_ids[]': self.conf['pd_teams'],
                                            'user_ids[]': self.conf['pd_users'],
                                            'statuses[]': ['triggered', 'acknowledged']
                                        })

        return incidents

    def exit(self) -> None:
        self.hide()
        QtCore.QCoreApplication.exit()
