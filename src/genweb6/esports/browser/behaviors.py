# -*- coding: utf-8 -*-
from zope import schema
from plone.namedfile.field import NamedImage
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")
from plone.supermodel import model
from plone.app.textfield import RichText
from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider


@provider(IFormFieldProvider)
class IRichDescription(model.Schema):
    """Add tags to content
    """

    rich_description = RichText(
        title=u"Descripció amb format",
        description=u"Descripció amb format utilitzada per algunes vistes",
        required=True,
    )


@provider(IFormFieldProvider)
class ICheckImage(model.Schema):
    """Add tags to content
    """

    check = schema.Bool(
        title=_(u"No mostrar títol"),
        description=_(u"Si està seleccionat, no es mostra el títol."),
        required=False,
        default=False)

    picture = NamedImage(
        title=_(u"Imatge per mostrar com a títol"),
        description=_(u"Afegeix imatge"),
        required=False,
    )
