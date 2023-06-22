# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from plone.dexterity.utils import createContentInContainer
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from genweb6.esports.utils import publish_object


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "genweb6.esports:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["genweb6.esports.upgrades"]


DATA = [
    {'id': 'instalacions', 'title': 'Instal·lacions',
     'importer': 'genweb6.esports.browser.import.InstalacioImporter',
     'xml': 'https://esportsonline.upc.edu/datos/pregen/xml/instalaciones.xml'},
    {'id': 'cursos', 'title': 'Cursos',
     'importer': 'genweb6.esports.browser.import.ActivitatImporter',
     'xml': 'https://esportsonline.upc.edu/datos/pregen/xml/cursos.xml'},
    {'id': 'competicions', 'title': 'Competicions',
     'importer': 'genweb6.esports.browser.import.CompeticioImporter',
     'xml': 'https://esportsonline.upc.edu/datos/pregen/xml/competiciones.xml'}]


def post_install(context):
    """Post install script"""
    alsoProvides(context, IDisableCSRFProtection)

    portal_url = api.portal.get_tool('portal_url')
    site = portal_url.getPortalObject()

    # TODO: Set 'gestio' container directly above Site root path, since there's no Multilingual in Esports.
    path = f'/{site.getPhysicalPath()[1]}/ca'
    ca_container = site.unrestrictedTraverse(path)
    ids = ca_container.objectIds()

    # Avoid process if 'gestio' folder already exists.
    if 'gestio' in ids:
        return

    gestio_container = createContentInContainer(ca_container, 'Folder', title='Gestió')
    publish_object(gestio_container) 

    for item in DATA:
        obj = createContentInContainer(gestio_container, 'SyncFolder',
                                 title=item['title'], id=item['id'], importer=item['importer'], url=item['xml'])
        publish_object(obj)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    alsoProvides(context, IDisableCSRFProtection)

    portal_url = api.portal.get_tool('portal_url')
    site = portal_url.getPortalObject()

    # TODO: Set 'gestio' container directly above Site root path, since there's no Multilingual in Esports.
    path = f'/{site.getPhysicalPath()[1]}/ca'
    ca_container = site.unrestrictedTraverse(path)
    ids = ca_container.objectIds()

    # Avoid process if 'gestio' folder already exists.
    if 'gestio' in ids:
        return

    gestio_container = createContentInContainer(ca_container, 'Folder', title='Gestió')
    publish_object(gestio_container)

    for item in DATA:
        obj = createContentInContainer(gestio_container, 'SyncFolder',
                                 title=item['title'], id=item['id'], importer=item['importer'], url=item['xml'])
        publish_object(obj)

 

