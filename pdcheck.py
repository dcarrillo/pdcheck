#!/usr/bin/env python3

import sys
import webbrowser
from os import getenv, path
from typing import Dict

import PagerDutyChecker as pdc

from PySide2 import QtCore, QtGui, QtWidgets

import pdpyras

import yaml


def check_pager_duty(*, tray_icon: QtWidgets.QSystemTrayIcon, conf: Dict) -> None:
    pd_session = pdpyras.APISession(conf['pd_api_key'])
    incidents = pd_session.list_all('incidents',
                                    params={
                                        'team_ids[]': conf['pd_teams'],
                                        'user_ids[]': conf['pd_users'],
                                        'statuses[]': ['triggered', 'acknowledged']
                                    })
    if incidents:
        tray_icon.menu.clear()
        icon = QtGui.QIcon(pdc.Resources.OK_ICON)
        incidents.sort(key=lambda k: k['status'])
        for incident in incidents:
            print(incident)
            if incident['status'] == 'acknowledged':
                icon = QtGui.QIcon(pdc.Resources.ACK_ICON)
            else:
                icon = QtGui.QIcon(pdc.Resources.ALERT_ICON)

            action = tray_icon.menu.addAction(icon, f'{incident["created_at"]} {incident["title"]}')
            action.triggered.connect(
                lambda f=webbrowser.open, url=incident['html_url']: webbrowser.open(url)
            )

        tray_icon.add_exit_menu_item()
        QtWidgets.QSystemTrayIcon.setIcon(tray_icon, icon)


def main():
    BASEDIR, _ = path.split(path.realpath(__file__))

    conf_file = path.join(BASEDIR, 'pdcheck.yml')

    try:
        with open(conf_file, 'r') as config_file:
            conf = yaml.load(config_file, Loader=yaml.SafeLoader)

        conf['interval'] = conf['interval'] if 'interval' in conf else 30000
        conf['pd_teams'] = conf['pd_teams'] if 'pd_teams' in conf else None
        conf['pd_users'] = conf['pd_users'] if 'pd_users' in conf else None

        if getenv('PD_API_KEY'):
            conf['pd_api_key'] = getenv('PD_API_KEY')
        elif 'pd_api_key' not in conf:
            raise ValueError('Pagerduty API key has to be provided')

    except (IOError, yaml.YAMLError, ValueError) as e:
        print(f'Error reading config file {conf_file}:\n{e}')
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    tray_icon = pdc.SystemTrayIcon(widget)
    tray_icon.show()

    check_pager_duty(tray_icon=tray_icon, conf=conf)

    timer = QtCore.QTimer(widget)
    timer.setInterval(conf['interval'])
    timer.timeout.connect(lambda t=tray_icon: check_pager_duty(
        tray_icon=tray_icon, conf=conf))
    timer.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
