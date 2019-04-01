from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
        {
            "label": _("Verkauf"),
            "icon": "fa fa-bank",
            "items": [
                {
                    "type": "doctype",
                    "name": "Customer",
                    "label": _("Customer"),
                    "description": _("Customer")
                },
                {
                    "type": "doctype",
                    "name": "Opportunity",
                    "label": _("Opportunity"),
                    "description": _("Opportunity")
                },
                {
                    "type": "doctype",
                    "name": "Quotation",
                    "label": _("Quotation"),
                    "description": _("Quotation")
                }
            ]
        },
        {
            "label": _("Cobisoft"),
            "icon": "fa fa-wrench",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Neuanmeldung",
                       "label": _("Neuanmeldung"),
                       "description": _("Neuanmeldung")
                   },
                   {
                       "type": "doctype",
                       "name": "Anfrage",
                       "label": _("Anfrage"),
                       "description": _("Anfrage")
                   }
            ]
        },
        {
            "label": _("Quotations"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Preisangebot",
                       "label": _("Preisangebot"),
                       "description": _("Preisangebot")
                   }
            ]
        }
    ]
