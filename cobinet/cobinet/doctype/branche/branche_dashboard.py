from frappe import _

def get_data():
   return {
      'fieldname': 'branche',
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
