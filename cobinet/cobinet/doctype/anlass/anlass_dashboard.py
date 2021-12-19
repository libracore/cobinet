from frappe import _

def get_data():
   return {
      'fieldname': 'event',
      'transactions': [
         {
            'label': _('Anmeldungen'),
            'items': ['Anmeldung Kundenevent']
         }
      ]
   }
