# -*- coding: utf-8 -*-
from zope import schema
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IActivitatAgenda(model.Schema):
    """Dexterity-Schema for ActivitatAgenda"""

    descripcioPublica = RichText(
        title=_(u"Descripció pública"),
        description=_(u"Descripció de l'activitat que es veurà al crear l'agenda"),
        required=True,
    )

    texturl = schema.TextLine(
        title=_(u"Text url"),
        description=_(u"Text de la url"),
        required=True,
    )

    url = schema.TextLine(
        title=_(u"URL"),
        description=_(u"URL que cal obrir"),
        required=True,
    )

    new_window = schema.Bool(
        title=_(u"Obrir en finestra nova"),
        description=_(u"Marcar la opció se voleu que s'obri en una finestra nova"),
        required=True,
    )

    picture = NamedImage(
        title=_(u"Imatge"),
        description=_(u"Si us plau, pujeu una imatge descriptiva"),
        required=False,
    )


@implementer(IActivitatAgenda)
class ActivitatAgenda(Container):
    """ActivitatAgenda instance class"""