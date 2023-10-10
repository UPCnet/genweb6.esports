# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from genweb6.esports.utils import get_list_from_string


class CursView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.base_url = 'https://esportsonline.upc.edu/'

    def get_credits(self):
        try:
            value = self.context.numcred.strip().replace(',', '.')
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

    def get_location(self):
        """ Adds comma to concatenation instalacion and complex"""
        location = []
        try:
            if self.context.lugar != '':
                location.append(self.context.lugar)
            if self.context.complejo != '':
                location.append(self.context.complejo)
            if self.context.instalacion != '':
                location.append(self.context.instalacion)

            if len(location) == 0:
                return None
            else:
                location = ', '.join(location)
                return location
        except Exception:
            return None

    def get_info(self):
        info = {
            'img': self.context.img,
            'img_url': self.base_url + self.context.img,
            'rates': get_list_from_string(self.context.tarifas),
            'activity': self.context.actividad,
            'description': self.context.descripcion,
            'course': self.context.curso,
            'texper': self.context.texper,
            'texdiasem': self.context.texdiasem,
            'texhor': self.context.texhor,
            'name': self.context.nombre,
            'lastnames': self.context.apellidos,
            'location': self.get_location(),
            'state': self.context.estado,
            'level': self.context.nivel,
            'link': self.context.enlace,
            'attachment': self.context.docanexo,
            'positions': self.context.plazas,
            'credits': self.get_credits(),
            'html_descrip': self.context.descrip,
        }

        return info
