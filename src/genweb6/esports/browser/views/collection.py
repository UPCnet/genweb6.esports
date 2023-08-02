from Products.Five.browser import BrowserView
from zope.component.hooks import getSite


class CollectionView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def portal_url(self):
        return getSite().absolute_url()

    def get_info(self):
        """ Get needed info in the template """
        #import ipdb; ipdb.set_trace()
        leadimage = '' if not self.context.picture else self.context.absolute_url() + '/@@images/picture'
        text = '' if not self.context.text else self.context.text.output
        info = {
            'title': self.context.Title(),
            'leadimage': leadimage,
            'text': text,
        }
        return info