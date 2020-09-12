#!/usr/bin/env python3

import logging
import sys
from logging.handlers import RotatingFileHandler
from os import getenv, makedirs, path

import PagerDutyChecker as pdc

from PySide2 import QtCore, QtWidgets

import yaml

BASEDIR, _ = path.split(path.realpath(__file__))

if not path.exists(f'{BASEDIR}/logs'):
    makedirs(f'{BASEDIR}/logs')

handler = RotatingFileHandler(path.join(BASEDIR, 'logs/pdcheck.log'), 'a', 1024 * 1024 * 4, 5)
handler.setFormatter(logging.Formatter('-- %(levelname)s -- %(asctime)s %(message)s'))
logger = logging.getLogger('pdcheck')
logger.addHandler(handler)


def main():
    conf_file = path.join(BASEDIR, 'pdcheck.yml')

    try:
        with open(conf_file, 'r') as config_file:
            conf = yaml.load(config_file, Loader=yaml.SafeLoader)

        try:
            logger.setLevel(conf['log_level'].upper())
        except KeyError:
            logger.setLevel('INFO')

        conf['interval'] = conf['interval'] if 'interval' in conf else 30
        conf['pd_teams'] = conf['pd_teams'] if 'pd_teams' in conf else None
        conf['pd_users'] = conf['pd_users'] if 'pd_users' in conf else None

        if getenv('PD_API_KEY'):
            conf['pd_api_key'] = getenv('PD_API_KEY')
        elif 'pd_api_key' not in conf:
            raise ValueError('Pagerduty API key has to be provided')

    except (IOError, yaml.YAMLError, ValueError) as e:
        print(e)
        logger.error(e)
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    logger.info('Starting pdcheck')
    tray_app = pdc.TrayIcon(widget, conf)
    tray_app.show()

    timer = QtCore.QTimer(widget)
    timer.setInterval(conf['interval'] * 1000)
    timer.timeout.connect(tray_app.update_incidents)
    timer.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
