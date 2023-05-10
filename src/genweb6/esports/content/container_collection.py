# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zExceptions import NotFound
from copy import deepcopy
#from plone.app.collection.collection import Collection
#from plone.app.collection.interfaces import ICollection
from plone.app.contenttypes.content import Collection, ICollection
from plone.app.querystring.querybuilder import QueryBuilder
from Acquisition import aq_parent


class ContainerCollection(Container, Collection):
    """
    A collection that can contain other collections
    """

    def results(self, batch=True, b_start=0, b_size=None, inherit=False, extra=[]):
        querybuilder = QueryBuilder(self, self.REQUEST)
        sort_order = 'reverse' if self.sort_reversed else 'ascending'
        if not b_size:
            b_size = self.item_count
        query = isinstance(self.query, list) and deepcopy(self.query) or []
        if inherit:
            parent = aq_parent(self)
            if ICollection.providedBy(parent):
                query += parent.query and deepcopy(parent.query) or []
                inparent = aq_parent(self)
                if ICollection.providedBy(inparent):
                    query += inparent.query and deepcopy(inparent.query) or []
        query = query + extra

        res = querybuilder(
            query=query,
            batch=batch, b_start=b_start, b_size=b_size,
            sort_on=self.sort_on, sort_order=sort_order,
            limit=self.limit)
        return res

    def queryCatalog(self, *args, **kwargs):

        return self.results(**kwargs)

    def __getitem__(self, name):
        banned = [
            "main_template",
            "portal_membership",
            "portal_properties",
            "global_cache_settings",
            "displayContentsTab",
            "global_statusmessage",
            "portal_properties",
            "plone_utils"
        ]
        if name not in banned:
            query = [{u'i': u'id', u'o': u'plone.app.querystring.operation.selection.is', u'v': name}]
            results = [a for a in self.results(extra=query)]
            if results:
                return results[0].getObject()
            else:
                raise NotFound
        else:
            raise NotFound
