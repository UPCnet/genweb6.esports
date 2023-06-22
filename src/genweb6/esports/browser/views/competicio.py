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
        except:
            return False
        
    def get_credits(self):
        try:
            value = self.context.creditos.strip().replace(',', '.')
            if value == '0.00':
                return None
            else:
                credit_value = str(int(float(value)))
        except:
            credit_value = 'H'

        if credit_value == 'H':
            return None
        else:
            return credit_value + 'ETCS'

    def parse_location(self):
        """ Adds comma to concatenation instalacion and complex"""
        try:
            insta = self.context.insta
            complejo = self.context.complejo
            lugar = None
            if insta and complejo:
                lugar = insta + ', ' + complejo
            if insta and not complejo:
                lugar = insta
            if not insta and complejo:
                lugar = complejo
            if not insta and not complejo:
                lugar = None

            return lugar

        except:
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