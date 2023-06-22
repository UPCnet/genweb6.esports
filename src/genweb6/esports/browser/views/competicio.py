from Products.Five.browser import BrowserView
from zope.component.hooks import getSite


class CompeticioView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.base_url = 'https://esportsonline.upc.edu/'

    def portal_url(self):
        return getSite().absolute_url()

    def tarifas(self):
        try:
            return eval(self.context.tarifas)
        except:
            return []

    def tarifas_title(self):
        try:
            values = self.tarifas()
            if values[0]['importe'] is False and \
               values[0]['fianzacur'] is False and \
               values[0]['impjugabo'] is False and \
               values[0]['fianzajugabo'] is False and \
               values[0]['impjugnoabo'] is False and \
               values[0]['fianzajugnoabo'] is False and \
               values[0]['impjugotro'] is False and \
               values[0]['fianzajugotro'] is False:
                return False
            else:
                return True
        except:
            return False
        
    def credits(self):
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

    def lugar(self):
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
        return {
            'img_dep': self.context.img_dep,
            'img_dep_url': self.base_url + self.context.img_dep,
            'deporte': self.context.deporte,
            'denom': self.context.denom,
            'competi': self.context.competi,
            'campeonato': self.context.campeonato,
            'competicionie': self.context.competicionie,
            'sexo': self.context.sexo,
            'modalidad': self.context.modalidad,
            'division': self.context.division,
            'grupo': self.context.grupo,
            'lugar': self.lugar(),
            'fase': self.context.fase,
            'fecini': self.context.fecini,
            'fecfin': self.context.fecfin,
            'enlace': self.context.enlace,
            'normativa': self.context.normativa,
            'documentoanexo': self.context.documentoanexo,
            'feciniins': self.context.feciniins,
            'fecfinins': self.context.fecfinins,
            'creditos': self.credits(),
            'tarifas': self.tarifas(),
            'descripcion': self.context.descripcion,
        }