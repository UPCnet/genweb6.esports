# -*- coding: utf-8 -*-
from zope.interface import implementer
from plone.supermodel import model
from plone.dexterity.content import Container
from zope import schema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")


class ISyncFolder(model.Schema):
    """Dexterity-Schema for SyncFolder"""

    url = schema.TextLine(
        title=_(u"XML Source Url"),
        required=True,
    )

    importer = schema.TextLine(
        title=_(u"Importer class"),
        required=True,
    )


@implementer(ISyncFolder)
class SyncFolder(Container):
    """SyncFolder instance class"""
