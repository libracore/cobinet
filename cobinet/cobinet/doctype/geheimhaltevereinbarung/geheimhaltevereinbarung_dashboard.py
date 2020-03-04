from frappe import _

def get_data():
   return {
      'fieldname': 'geheimhaltevereinbarung',
      'transactions': [
         {
            'label': _('Zuordnungen'),
            'items': ['Zuordnung GHV']
         }
      ]
   }
