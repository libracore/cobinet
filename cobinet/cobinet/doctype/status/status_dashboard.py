from frappe import _

def get_data():
   return {
      'fieldname': 'status',
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
