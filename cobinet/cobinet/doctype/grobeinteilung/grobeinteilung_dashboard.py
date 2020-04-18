from frappe import _

def get_data():
   return {
      'fieldname': 'grobeinteilung',
      'transactions': [
         {
            'label': _('Customer'),
            'items': ['Customer']
         },
         {
            'label': _('Aktivitaet'),
            'items': ['Aktivitaet']
         }
      ]
   }
