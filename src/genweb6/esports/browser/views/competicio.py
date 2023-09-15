# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from zope.component.hooks import getSite
from genweb6.esports.utils import get_list_from_string


class CompeticioView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.base_url = 'https://esportsonline.upc.edu/'

    def portal_url(self):
        return getSite().absolute_url()

    def check_rates_title(self):
        try:
            rates = get_list_from_string(self.context.tarifas)
            if not rates:
                return False

            rate = rates[0]
            if any(value is not False for value in rate.keys()):
                return True

            return False
        except Exception:
            return False

    def get_credits(self):
        try:
            value = self.context.creditos.strip().replace(',', '.')
            if value == '0.00':
                return None
            else:
                credit_value = str(int(float(value)))
        except Exception:
            credit_value = 'H'

        if credit_value == 'H':
            return None
        else:
            return credit_value + 'ETCS'

    def parse_location(self):
        """ Adds comma to concatenation instalacion and complex"""
        try:
            installation = self.context.installation
            complex = self.context.complex
            location = None
            if installation and complex:
                location = installation + ', ' + complex
            if installation and not complex:
                location = installation
            if not installation and complex:
                location = complex
            if not installation and not complex:
                location = None

            return location

        except Exception:
            return None

    def get_info(self):
        """ Get needed info in the template """
        info = {
            'sport_img': self.context.img_dep,
            'sport_img_url': self.base_url + self.context.img_dep,
            'sport': self.context.deporte,
            'sport_description': self.context.denom,
            'competition': self.context.competi,
            'championship': self.context.campeonato,
            'competition_type': self.context.competicionie,
            'gender': self.context.sexo,
            'modality': self.context.modalidad,
            'division': self.context.division,
            'group': self.context.grupo,
            'location': self.parse_location(),
            'phase': self.context.fase,
            'start_date': self.context.fecini,
            'end_date': self.context.fecfin,
            'link': self.context.enlace,
            'rules': self.context.normativa,
            'attachment': self.context.documentoanexo,
            'inst_start_date': self.context.feciniins,
            'inst_end_date': self.context.fecfinins,
            'credits': self.get_credits(),
            'rates': get_list_from_string(self.context.tarifas),
            'rates_title': self.check_rates_title(),
            'description': self.context.descripcion,
        }
        return info
