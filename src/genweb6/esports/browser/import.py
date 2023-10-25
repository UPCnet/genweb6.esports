# -*- coding: utf-8 -*-
from urllib.parse import unquote

import bleach
import requests
import transaction
from DateTime import DateTime
from datetime import datetime
from genweb6.esports.keywords import IKeywordsCategorizationUtility
from genweb6.esports.utils import publish_object
from lxml import etree
from plone.dexterity.utils import createContentInContainer
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.interface import alsoProvides


class CleanSyncFolderView(BrowserView):
    """ Clear content from Sync Folders """

    def __call__(self):
        alsoProvides(self.context, IDisableCSRFProtection)
        self.clean_content()
        transaction.commit()

    def clean_content(self):
        for itemid in self.context.contentIds():
            self.context._delObject(itemid)

        return 'Cleaned'


class SyncContentView(BrowserView):
    """ Sync Content from Omesa data """
    """
    Directly handwriten over the content field 'importer'.
    This is set automatically when installing the package.
    """

    @property
    def generate_instance_importer(self):
        """ P.E: genweb6.esports.browser.InstalacioImporter """
        parts = self.context.importer.split('.')
        class_name = parts.pop()
        import_path = '.'.join(parts)
        module = __import__(import_path, fromlist=[class_name])
        klass = getattr(module, class_name)
        return klass

    def render_import(self):
        importer = self.generate_instance_importer(self.context, self.request)
        return importer.render()


class SyncAllContentView(BrowserView):
    """ Sync All Content from Omesa data """

    def __call__(self):
        alsoProvides(self.context, IDisableCSRFProtection)
        syncfolders = self.context.portal_catalog.searchResults(
            portal_type='SyncFolder', sort_on='reverse')
        view_urls = [a.getPath() for a in syncfolders]
        for view_url in view_urls:
            sync_content_view = self.context.restrictedTraverse(
                f'{view_url}/sync_content')
            sync_content_view.render_import()

        subjects_tool = getUtility(
            IKeywordsCategorizationUtility, 'portal_keywords_categorization')
        subjects_tool.update()

        self.request.response.redirect(self.context.absolute_url())
        transaction.commit()


class ImporterView(BrowserView):

    def __init__(self):
        self.ptype = 'Item'
        self.fields = dict()

    def clean(self):
        for item_id in self.context.contentIds():
            self.context._delObject(item_id)

    def get_XML(self):
        """  Get data in XML format from OMESA """

        data = requests.get(self.context.url)
        tree = etree.fromstring(data.content)
        self.xml = tree

    def get_tags(self, item):
        tags = [a.text for a in item.find(
            'etiquetas').findall('item') if a.text]
        return tuple(tags)

    # Start of methods - Fill object's data
    def set_string(self, value):
        return value

    def set_integer(self, value):
        return int(value)

    def set_date(self, value):
        date = ''

        #Parse dates so Plone can sort by them
        try:
            date_object = datetime.strptime(value, '%d/%m/%Y')
            parsed_date_string = date_object.strftime('%Y-%m-%d')
            date = parsed_date_string

        except ValueError:
            print('Incorrect date format')
            date = value
            
        return DateTime(date).asdatetime()

    def set_cdata(self, value):
        ALLOWED_TAGS = ['a', 'p', 'b', 'strong', 'br']
        return bleach.clean(value, strip=True, tags=ALLOWED_TAGS)

    def set_cdatadesc(self, value):
        """ Maintain iframe and maps """
        ALLOWED_TAGS = ['a', 'b', 'strong', 'br', 'iframe', 'p']
        ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title'],
            'acronym': ['title'],
            'abbr': ['title'],
            'iframe': ['src', 'height', 'width']}

        return bleach.clean(value, strip=True, tags=ALLOWED_TAGS,
                            attributes=ALLOWED_ATTRIBUTES)

    def set_cdatamaps(self, value):
        """ Maintain iframe and maps """
        ALLOWED_TAGS = ['a', 'b', 'strong', 'br', 'iframe']
        ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title'],
            'acronym': ['title'],
            'abbr': ['title'],
            'iframe': ['src', 'height', 'width']}

        return bleach.clean(value, strip=True, tags=ALLOWED_TAGS,
                            attributes=ALLOWED_ATTRIBUTES)

    def set_enlace(self, value):
        return unquote(value)

    def set_simple_value(self, value):
        values = []
        items = value.findall('item')

        for item in items:
            values.append({
                'item': item.text
            })

        return str(values)

    def set_etiquetas(self, value):
        return self.set_simple_value(value)

    # End of methods - Fill object's data

    def set_field_on_object(self, obj, field, fieldlistname='fields'):
        fields = getattr(self, fieldlistname)
        origin_field_name = field.tag

        if origin_field_name in fields:
            field_mapping = fields[origin_field_name]
            if field_mapping.get('value', 'text') == 'text':
                origin_field_value = field.text and field.text or ''
            else:
                origin_field_value = field

            setter = getattr(self, 'set_%s' % field_mapping['ftype'])
            _value = setter(origin_field_value)
            
            if origin_field_name == 'fecini':
                obj.setEffectiveDate(_value)
            
            setattr(obj, field_mapping['name'], _value)

    def render(self):
        self.get_XML()
        items = self.xml.findall('item')

        if items:
            self.clean()

        for item in items:
            title = item.findtext(self.filter_name, default=self.ptype)
            obj = createContentInContainer(self.context, self.ptype, title=title)
            fields = item.iterchildren()

            for field in fields:
                self.set_field_on_object(obj, field)

            obj.subject = self.get_tags(item)

            publish_object(obj)
            obj.reindexObject()
            transaction.commit()

            print('Imported %s at %s' %
                  (self.ptype, obj.absolute_url()))
        msg = (f"Importació de {self.ptype_literal} finalitzada, "
               f"s'han importat {len(items)} {self.ptype_literal}")
        self.context.plone_utils.addPortalMessage(
            msg)
        self.request.response.redirect(
            f'{self.context.absolute_url()}/folder_contents')


class ActivitatImporter(ImporterView):
    """ Activitat - Curs """

    ptype = 'Curs'
    ptype_literal = 'Cursos'
    filter_name = 'descripcion'

    # Activity fields
    fields = {
        'etiquetas': {'ftype': 'etiquetas', 'name': 'etiquetas', 'value': 'field'},
        'img': {'ftype': 'string', 'name': 'img'},
        'img_g': {'ftype': 'string', 'name': 'img_g'},
        'actividad': {'ftype': 'string', 'name': 'actividad'},
        'curso': {'ftype': 'string', 'name': 'curso'},
        'descripcion': {'ftype': 'string', 'name': 'descripcion'},
        'texper': {'ftype': 'string', 'name': 'texper'},
        'texdiasem': {'ftype': 'string', 'name': 'texdiasem'},
        'texhor': {'ftype': 'string', 'name': 'texhor'},
        'nombre': {'ftype': 'string', 'name': 'nombre'},
        'apellidos': {'ftype': 'string', 'name': 'apellidos'},
        'lugar': {'ftype': 'string', 'name': 'lugar'},
        'complejo': {'ftype': 'string', 'name': 'complejo'},
        'instalacion': {'ftype': 'string', 'name': 'instalacion'},
        'estado': {'ftype': 'string', 'name': 'estado'},
        'fecini': {'ftype': 'date', 'name': 'fecini'},
        'fecfin': {'ftype': 'date', 'name': 'fecfin'},
        'nivel': {'ftype': 'string', 'name': 'nivel'},
        'plazas': {'ftype': 'string', 'name': 'plazas'},
        'numcred': {'ftype': 'string', 'name': 'numcred'},
        'descrip': {'ftype': 'cdatadesc', 'name': 'descrip'},
        'enlace': {'ftype': 'enlace', 'name': 'enlace'},
        'docanexo': {'ftype': 'string', 'name': 'docanexo'},
        'tarifas': {'ftype': 'tarifas', 'name': 'tarifas', 'value': 'field'}
    }

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def set_tarifas(self, value):
        tarifas = []
        items = value.findall('item')

        for item in items:
            price = item.findtext('importe', default='0.0')
            price = 'GRATUÏT' if price == '0.0' else price + '€'

            tarifas.append({
                'descrip': item.findtext('descrip', default=''),
                'importe': price,
                'memoweb': item.findtext('memo', default=''),
                'inicio': item.findtext('fecini', default=''),
                'fin': item.findtext('fecfin', default='')
            })

        return str(tarifas)


class InstalacioImporter(ImporterView):
    """ Instal·lacions """

    ptype = 'Instalacio'
    ptype_literal = 'Instal·lacions'
    filter_name = 'denomins'

    # Instalation fields
    fields = {
        'etiquetas': {'ftype': 'etiquetas', 'name': 'etiquetas', 'value': 'field'},
        'img': {'ftype': 'string', 'name': 'imagen'},
        'img_g': {'ftype': 'string', 'name': 'imagen_grande'},
        'direc': {'ftype': 'string', 'name': 'direccion'},
        'cpostal': {'ftype': 'string', 'name': 'codigo_postal'},
        'poblacion': {'ftype': 'string', 'name': 'poblacion'},
        'provincia': {'ftype': 'string', 'name': 'provincia'},
        'telefono': {'ftype': 'string', 'name': 'telefono'},
        'email': {'ftype': 'string', 'name': 'email'},
        'carac': {'ftype': 'cdatamaps', 'name': 'detalles'},
        'denom': {'ftype': 'string', 'name': 'titulo2'},
        'img_ins': {'ftype': 'string', 'name': 'imagen_ins'},
        'img_g_ins': {'ftype': 'string', 'name': 'imagen_ins_grande'},
        'taris': {'ftype': 'tarifas', 'name': 'tarifas', 'value': 'field'},
        'enlace': {'ftype': 'enlace', 'name': 'enlace'},
        'obswebins': {'ftype': 'cdata', 'name': 'observaciones'},
        'docanexo': {'ftype': 'string', 'name': 'docanexo'},
        'deportes': {'ftype': 'deportes', 'name': 'deportes', 'value': 'field'}
    }

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def set_tarifas(self, value):
        tarifas = []
        items = value.findall('item')
        dates = ''

        for item in items:
            price = item.findtext('importe', default='0.0')
            price = 'GRATUÏT' if price == '0.0' else price + '€'

            since = item.findtext('desdefecha', default=None)
            until = item.findtext('hastafecha', default=None)

            if since is None and until is None:
                dates = False
            elif since is None:
                dates = f'Preus vàlids fins a {until}'
            elif until is None:
                dates = f'Preus vàlids des de {since}'
            else:
                dates = f'Preus vàlids des de {since} fins a {until}'

            tarifas.append({
                'descrip': item.findtext('descrip', default=''),
                'importe': price,
                'memoweb': item.findtext('memoweb', default=''),
                'dates': dates
            })

        return str(tarifas)

    def set_deportes(self, value):
        return self.set_simple_value(value)


class CompeticioImporter(ImporterView):
    """ Competicio """

    ptype = 'Competicio'
    ptype_literal = 'Competicions'
    filter_name = 'denom'

    # Competition fields
    fields = {
        'etiquetas': {'ftype': 'etiquetas', 'name': 'etiquetas', 'value': 'field'},
        'img_dep': {'ftype': 'string', 'name': 'img_dep'},
        'deporte': {'ftype': 'string', 'name': 'deporte'},
        'competi': {'ftype': 'string', 'name': 'competi'},
        'denom': {'ftype': 'string', 'name': 'denom'},
        'campeonato': {'ftype': 'string', 'name': 'campeonato'},
        'fase': {'ftype': 'string', 'name': 'fase'},
        'competicionie': {'ftype': 'string', 'name': 'competicionie'},
        'sexo': {'ftype': 'string', 'name': 'sexo'},
        'modalidad': {'ftype': 'string', 'name': 'modalidad'},
        'division': {'ftype': 'string', 'name': 'division'},
        'grupo': {'ftype': 'string', 'name': 'grupo'},
        'insta': {'ftype': 'string', 'name': 'insta'},
        'complejo': {'ftype': 'string', 'name': 'complejo'},
        'fecini': {'ftype': 'date', 'name': 'fecini'},
        'fecfin': {'ftype': 'date', 'name': 'fecfin'},
        'feciniins': {'ftype': 'string', 'name': 'feciniins'},
        'fecfinins': {'ftype': 'string', 'name': 'fecfinins'},
        'creditos': {'ftype': 'string', 'name': 'creditos'},
        'normativa': {'ftype': 'string', 'name': 'normativa'},
        'documentoanexo': {'ftype': 'string', 'name': 'documentoanexo'},
        'descripcion': {'ftype': 'string', 'name': 'descripcion'},
        'enlace': {'ftype': 'string', 'name': 'enlace'},
        'tarifas': {'ftype': 'tarifas', 'name': 'tarifas', 'value': 'field'}
    }

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def set_tarifas(self, value):
        tarifas = []
        items = value.findall('item')

        for item in items:
            tarifas.append({
                'importe': item.findtext('importe', default=False),
                'fianzacur': item.findtext('fianzacur', default=False),
                'impjugabo': item.findtext('impjugabo', default=False),
                'fianzajugabo': item.findtext('fianzajugabo', default=False),
                'impjugnoabo': item.findtext('impjugnoabo', default=False),
                'fianzajugnoabo': item.findtext('fianzajugnoabo', default=False),
                'impjugotro': item.findtext('impjugotro', default=False),
                'fianzajugotro': item.findtext('fianzajugotro', default=False),
            })
        return str(tarifas)
