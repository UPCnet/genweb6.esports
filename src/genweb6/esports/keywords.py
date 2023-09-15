# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from lxml import etree
from OFS.SimpleItem import SimpleItem
from zope.component import getUtility
from zope.interface import Attribute, Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer
import requests


class IKeywordsCategorizationUtility(Interface):
    """ Utility to manage filters and tags that come from Omesa """

    categories = Attribute(u"keyword categories")


@implementer(IKeywordsCategorizationUtility)
class KeywordsCategorizationUtility(SimpleItem):
    categories = None
    filters = [
        'https://esportsonline.upc.edu/datos/pregen/xml/filtrosinstalaciones.xml',
        'https://esportsonline.upc.edu/datos/pregen/xml/filtroscursos.xml',
        'https://esportsonline.upc.edu/datos/pregen/xml/filtroscompeticiones.xml'
    ]

    filternames = {
        'tipologia': "Tipus d'Instal·lacions",
        'comp': 'Complexos esportius',
        'deportes': 'Esports en Instal·lacions',
        'campus': 'Campus',

        'bloque': "Blocs d'Activitats",
        'ambito': "Àmbits d'Activitats",
        'acti': 'Activitats',

        'tipcomp': 'Tipus de competicions',
        'cat': 'Categories de competició',
        'deporte': 'Esports de competició',
        'campeonatos': 'Campionats',
    }

    def __init__(self):
        self.categories = OOBTree()

    def update(self):
        self.categories = OOBTree()
        for url in self.filters:
            try:
                data = requests.get(url)
                tree = etree.fromstring(data.content)
                xml = tree
                if xml.tag != 'filtros':
                    filters = xml.findall('filtros')
                    xml = filters[0]

                for filtertype in xml.iterchildren():
                    filterid = filtertype.tag
                    current = self.categories.get(filterid, [])
                    for item in filtertype.findall('item'):
                        if item.text and item.text not in current:
                            current.append(item.text)
                    current.sort()
                    self.categories[filterid] = current
            except Exception:
                pass

    def keywords(self, checked=[]):
        factory = getUtility(IVocabularyFactory, 'plone.app.vocabularies.Keywords')
        vocabulary = factory(self)

        keywords_by_filter = []
        terms = []
        for a in vocabulary:
            terms.append(a.title)

        filter_terms = []
        filters_by_title = sorted(self.filternames.items(), key=lambda x: x[1])

        for filterid, filtertitle in filters_by_title:
            if len(self.categories[filterid]) > 0:
                keywords_by_filter.append({'title': filtertitle,
                                           'value': filterid,
                                           'header': True})
                for item in self.categories[filterid]:
                    filter_terms.append(item)
                    keywords_by_filter.append({'title': item,
                                               'value': item,
                                               'header': False,
                                               'checked': item in checked})

        total = set(terms)
        existents = set(filter_terms)
        altres = set(existents).symmetric_difference(set(total))
        if altres:
            altres = list(altres)
            altres.sort()
            keywords_by_filter.append({'title': 'Altres',
                                       'value': 'altres',
                                       'header': True})
            for item in altres:
                keywords_by_filter.append({'title': item,
                                           'value': item,
                                           'header': False,
                                           'checked': item in checked})
        return keywords_by_filter
