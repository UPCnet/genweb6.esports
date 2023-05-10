# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView

class SyncContentView(BrowserView):
    """ Sync Content from Omesa data """

    def __call__(self):
        pass

class CleanSyncFolderView(BrowserView):
    """ Clear content from Sync Folders """

    def __call__(self):
        pass


class SyncAllContentView(BrowserView):
    """ Sync All Content from Omesa data """

    def __call__(self):
        pass