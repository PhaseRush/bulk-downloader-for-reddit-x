#!/usr/bin/env python3

import configparser


class SiteAuthenticator:
    def __init__(self, cfg: configparser.ConfigParser):
        self.imgur_authentication = None
