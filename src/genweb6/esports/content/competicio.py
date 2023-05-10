# -*- coding: utf-8 -*-
from zope import schema
from genweb6.esports.content.interfaces import IOmesaContent
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")
from plone.dexterity.content import Container
from zope.interface import implementer

class ICompeticio(IOmesaContent):
    """Dexterity-Schema for Competicio"""

    etiquetas = schema.TextLine(
        title=_(u"Etiquetas"),
        required=False,
    )

    img_dep = schema.TextLine(
        title=_(u"Imagen"),
        required=False
    )

    deporte = schema.TextLine(
        title=_(u"Deporte"),
        required=False
    )

    competi = schema.TextLine(
        title=_(u"Competición"),
        required=False
    )

    denom = schema.TextLine(
        title=_(u"Título 2"),
        required=False
    )

    campeonato = schema.TextLine(
        title=_(u"Campeonato"),
        required=False
    )

    fase = schema.TextLine(
        title=_(u"Fase"),
        required=False
    )

    competicionie = schema.TextLine(
        title=_(u"Tipo competición"),
        required=False
    )

    sexo = schema.TextLine(
        title=_(u"Sexo"),
        required=False
    )

    modalidad = schema.TextLine(
        title=_(u"Modalidad"),
        required=False
    )

    division = schema.TextLine(
        title=_(u"División"),
        required=False
    )

    grupo = schema.TextLine(
        title=_(u"Grupo"),
        required=False
    )

    lugar = schema.TextLine(
        title=_(u"Lugar"),
        required=False
    )

    complejo = schema.TextLine(
        title=_(u"Complejo"),
        required=False
    )

    insta = schema.TextLine(
        title=_(u"Instalación"),
        required=False
    )

    fecini = schema.TextLine(
        title=_(u"Fecha inicio"),
        required=False
    )

    fecfin = schema.TextLine(
        title=_(u"Fecha final"),
        required=False
    )

    feciniins = schema.TextLine(
        title=_(u"Fecha inicio 2"),
        required=False
    )

    fecfinins = schema.TextLine(
        title=_(u"Fecha final 2"),
        required=False
    )

    creditos = schema.TextLine(
        title=_(u"Créditos"),
        required=False
    )

    normativa = schema.TextLine(
        title=_(u"Normativa"),
        required=False
    )

    documentoanexo = schema.TextLine(
        title=_(u"Documento anexo"),
        required=False
    )

    descripcion = schema.TextLine(
        title=_(u"Descripción"),
        required=False
    )

    enlace = schema.TextLine(
        title=_(u"Enlace"),
        required=False
    )

    tarifas = schema.TextLine(
        title=_(u"Tarifas"),
        required=False
    )

@implementer(ICompeticio)
class Competicio(Container):
    """Competicio instance class"""
