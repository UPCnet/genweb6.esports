# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from zope.interface import alsoProvides
import transaction
from plone.protect.interfaces import IDisableCSRFProtection
from DateTime import DateTime


class SetEqualDates(BrowserView):

    """ View used to set fecini field the same as effective Date """

    def __call__(self):

        alsoProvides(self.context, IDisableCSRFProtection)

        catalog = api.portal.get_tool('portal_catalog')
        params = {'portal_type': 'genweb.upc.documentimage',
                  'review_state': 'published'}

        brains = catalog.searchResults(**params)

        for brain in brains:
            obj = brain.getObject()
            effective = obj.effective()
            string_date = effective.strftime('%Y-%m-%d')
            value = DateTime(string_date).asdatetime()
            setattr(obj, 'fecini', value)
            
            obj.reindexObject()
            transaction.commit()
