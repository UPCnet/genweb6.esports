# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from plone.app.contenttypes.browser.collection import CollectionView


class EsportsCollectionView(CollectionView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def portal_url(self):
        return getSite().absolute_url()

    def get_info(self):
        """ Get needed info in the template """

        text = '' if not self.context.text else self.context.text.output
        info = {
            'title': self.context.Title(),
            'text': text,
        }
        return info

    def get_items(self):
        results = self.results()
        items = []
        remote_url = 'https://esportsonline.upc.edu/'
        for res in results:
            obj = res.getObject()
            img = ''

            if hasattr(obj, 'image'):
                img = obj.absolute_url() + '/@@images/image'
            elif hasattr(obj, 'img'):
                img = remote_url + getattr(obj, 'img')
            elif hasattr(obj, 'img_dep'):
                img = remote_url + getattr(obj, 'img_dep')
            elif hasattr(obj, 'imagen'):
                img = remote_url + getattr(obj, 'imagen')
            
            items.append(
                {'title': obj.Title(),
                 'image': img, 'url': obj.absolute_url(),
                 'omesa_link': '' if not hasattr(obj, 'enlace') else obj.enlace,
                 'dates': '' if not hasattr(obj, 'texper') else obj.texper,
                 'portal_type': obj.portal_type,})

        return items

    def results(self, **kwargs):
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)
        results = self.collection_behavior.results(**kwargs)
        """ for item in batch: item.getObject() """
        return results
