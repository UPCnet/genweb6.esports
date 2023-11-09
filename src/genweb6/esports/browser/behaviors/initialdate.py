# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IInitialDate(model.Schema):
    """ Set initial date to activities. """

    fecini = schema.Datetime(
        title="Data d'inici",
        description="Data d'inici de l'activitat",
        required=False,
    )


@implementer(IInitialDate)
class InitialDate(object):

    def __init__(self, context):
        self.context = context

    def _set_fecini(self, value):
        self.context.fecini = value

    def _get_fecini(self):
        return getattr(self.context, 'fecini', self.context.fecini)

    fecini = property(_get_fecini, _set_fecini)
