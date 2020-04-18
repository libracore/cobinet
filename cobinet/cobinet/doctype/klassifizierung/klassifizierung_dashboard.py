from frappe import _

def get_data():
   return {
      'fieldname': 'klassifizierung',
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
