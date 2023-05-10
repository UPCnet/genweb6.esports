# -*- coding: utf-8 -*-
from zope import schema
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDestacat(model.Schema):
    """Dexterity-Schema for Destacat"""

    check = schema.Bool(
        title=_(u"No mostrar títol al destacat"),
        description=_(u"Si està seleccionat, no es mostra el títol al destacat."),
        required=False,
        default=False)

    text = RichText(
        title=_(u"Text"),
        description=_(u"The displayed text"),
        required=False,
    )

    check_ombrejada = schema.Bool(
        title=_(u"No mostrar part ombrejada del text"),
        description=_(u"Si està seleccionat, no es mostra la part ombrejada al destacat ni el seu text."),
        required=False,
        default=False)

    check_readmore = schema.Bool(
        title=_(u"No mostrar el text 'Llegir més'"),
        description=_(u"Si està seleccionat, no es mostra l'enllac al llegir més."),
        required=False,
        default=False)

    picture = NamedImage(
        title=_(u"Picture"),
        description=_(u"Please upload an image"),
        required=True,
    )

    url = schema.TextLine(
        title=_(u"url"),
        description=_(u"URL pel link de més informació"),
        required=True,
    )

@implementer(IDestacat)
class Destacat(Container):
    """Destacat instance class"""

