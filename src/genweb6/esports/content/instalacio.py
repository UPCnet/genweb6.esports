# -*- coding: utf-8 -*-
from zope import schema
from genweb6.esports.content.interfaces import IOmesaContent
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")
from plone.dexterity.content import Container
from zope.interface import implementer



class IInstalacio(IOmesaContent):
    """Dexterity-Schema for Instal·lació"""

    tarifas = schema.TextLine(
        title=_(u"Tarifas"),
        required=False
    )

    etiquetas = schema.TextLine(
        title=_(u"Etiquetas"),
        required=False
    )

    docanexo = schema.TextLine(
        title=_(u"docanexo"),
        required=False
    )

    deportes = schema.TextLine(
        title=_(u"deportes"),
        required=False
    )

    direccion = schema.TextLine(
        title=_(u"Dirección"),
        required=False,
    )

    codigo_postal = schema.TextLine(
        title=_(u"Código postal"),
        required=False,
    )

    poblacion = schema.TextLine(
        title=_(u"Población"),
        required=False,
    )

    provincia = schema.TextLine(
        title=_(u"Província"),
        required=False,
    )

    telefono = schema.TextLine(
        title=_(u"Teléfono"),
        required=False,
    )

    email = schema.TextLine(
        title=_(u"Email"),
        required=False,
    )

    detalles = schema.TextLine(
        title=_(u"Detalles"),
        required=False,
    )

    titulo2 = schema.TextLine(
        title=_(u"Título 2"),
        required=False,
    )

    imagen = schema.TextLine(
        title=_(u"Imagen"),
        required=False
    )

    imagen_grande = schema.TextLine(
        title=_(u"Imagen grande"),
        required=False
    )

    imagen_ins = schema.TextLine(
        title=_(u"Imagen instalación"),
        required=False
    )

    imagen_ins_grande = schema.TextLine(
        title=_(u"Imagen instalación grande"),
        required=False
    )

    enlace = schema.TextLine(
        title=_(u"Enlace"),
        required=False
    )

    observaciones = schema.TextLine(
        title=_(u"Observaciones"),
        required=False
    )

@implementer(IInstalacio)
class Instalacio(Container):
    """Instalacio instance class"""