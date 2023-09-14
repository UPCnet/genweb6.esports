# -*- coding: utf-8 -*-
from plone import schema
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from plone.namedfile.field import NamedImage
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")


class IBannerEsports(model.Schema):
    """Dexterity-Schema for BannerEsports"""

    url = schema.TextLine(
        title=_(u"URL"),
        description=_(u"URL que cal obrir"),
        required=True,
    )

    new_window = schema.Bool(
        title=_(u"Obrir en finestra nova"),
        description=_(u"Marcar la opció se voleu que s'obri en una finestra nova"),
        required=False,
    )

    picture = NamedImage(
        title=_(u"Imatge"),
        description=_(u"Si us plau, pujeu una imatge descriptiva"),
        required=False,
    )


@implementer(IBannerEsports)
class BannerEsports(Container):
    """BannerEsports instance class"""
