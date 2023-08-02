# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import implementer
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider
from plone.supermodel import model
from plone.namedfile.field import NamedImage
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")


@provider(IFormFieldProvider)
class ILeadImage(model.Schema):
    """Adds lead image"""

    picture = NamedImage(
        title=_(u"Lead Image"),
        description=_(u"Afegeix imatge"),
        required=False,
    )


@implementer(ILeadImage)
class LeadImage(object):
    adapts(ILeadImage)

    def __init__(self, context):
        self.context = context

    def _set_picture(self, value):
        self.context.picture = value

    def _get_picture(self):
        return getattr(self.context, 'picture', None)

    picture = property(_get_picture, _set_picture)
