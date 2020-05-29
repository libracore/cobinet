from frappe import _

def get_data():
   return {
      'fieldname': 'activity',
      'transactions': [
         {
            'label': _('Sales'),
            'items': ['Opportunity']
         }
      ]
   }
