# -*- coding: utf-8 -*-
from zope import schema
from genweb6.esports.content.interfaces import IOmesaContent
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")
from plone.dexterity.content import Container
from zope.interface import implementer


class ICurs(IOmesaContent):
    """Dexterity-Schema for Curs (Activitat)"""

    etiquetas = schema.TextLine(
        title=_(u"Etiquetas"),
        required=False,
    )

    img = schema.TextLine(
        title=_(u"Imagen"),
        required=False,
    )

    img_g = schema.TextLine(
        title=_(u"Imagen grande"),
        required=False,
    )

    curso = schema.TextLine(
        title=_(u"Curso"),
        required=False,
    )

    descripcion = schema.TextLine(
        title=_(u"Título 2"),
        required=False,
    )

    texper = schema.TextLine(
        title=_(u"Fechas"),
        required=False,
    )

    texdiasem = schema.TextLine(
        title=_(u"Dias semana"),
        required=False,
    )

    texhor = schema.TextLine(
        title=_(u"Horas"),
        required=False,
    )

    nombre = schema.TextLine(
        title=_(u"Nombre"),
        required=False,
    )

    apellidos = schema.TextLine(
        title=_(u"Apellidos"),
        required=False,
    )

    lugar = schema.TextLine(
        title=_(u"Lugar"),
        required=False,
    )

    complejo = schema.TextLine(
        title=_(u"Complejo"),
        required=False,
    )

    instalacion = schema.TextLine(
        title=_(u"Instalación"),
        required=False,
    )

    estado = schema.TextLine(
        title=_(u"Estado"),
        required=False,
    )

    fecini = schema.TextLine(
        title=_(u"Fecha inicio"),
        required=False,
    )

    fecfin = schema.TextLine(
        title=_(u"Fecha final"),
        required=False,
    )

    nivel = schema.TextLine(
        title=_(u"Nivel"),
        required=False,
    )

    plazas = schema.TextLine(
        title=_(u"Plazas"),
        required=False,
    )

    numcred = schema.TextLine(
        title=_(u"Créditos"),
        required=False,
    )

    descrip = schema.TextLine(
        title=_(u"Descripción html"),
        required=False,
    )

    enlace = schema.TextLine(
        title=_(u"Enlace"),
        required=False,
    )

    tarifas = schema.TextLine(
        title=_(u"Tarifas"),
        required=False,
    )


@implementer(ICurs)
class Curs(Container):
    """Curs instance class"""