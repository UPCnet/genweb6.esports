from Products.Five.browser import BrowserView
from genweb6.esports.utils import get_list_from_string



class InstalacioView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.base_url = 'https://esportsonline.upc.edu/'

        
    def check_rates_title(self):
        """ Check if there is any rate available """
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
        
    def get_tags(self):
        try:
            return eval(self.context.etiquetas)
        except:
            return []
        
    def get_info(self):
        info = {
            'img': self.context.imagen,
            'img_url': self.base_url + self.context.imagen,
            'inst_img': self.context.imagen_ins,
            'inst_img_url': self.base_url + self.context.imagen_ins,
            'title': self.context.title,
            'title2': self.context.titulo2,
            'address': self.context.direccion,
            'postcode': self.context.codigo_postal,
            'city': self.context.poblacion,
            'province': self.context.provincia,
            'phone': self.context.telefono,
            'mail': self.context.email,
            'link': self.context.enlace,
            'attachment': self.context.docanexo,
            'rates': get_list_from_string(self.context.tarifas),
            'rates_title': self.check_rates_title(),
            'observations': self.context.observaciones,
            'sports': get_list_from_string(self.context.deportes),
            'details': self.context.detalles,
        }

        return info