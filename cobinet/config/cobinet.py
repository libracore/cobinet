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
                    "name": "Contact",
                    "label": _("Contact"),
                    "description": _("Contact")
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
                },
                {
                    "type": "doctype",
                    "name": "Item",
                    "label": _("Item"),
                    "description": _("Item")
                },
                {
                    "type": "doctype",
                    "name": "Geheimhaltevereinbarung",
                    "label": _("Geheimhaltevereinbarung"),
                    "description": _("Geheimhaltevereinbarung")
                },
                {
                    "type": "report",
                    "name": "Uebersicht GHV",
                    "label": _("Uebersicht GHV"),
                    "doctype": "Geheimhaltevereinbarung",
                    "is_query_report": True
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
                   },
                   {
                       "type": "doctype",
                       "name": "Quotation",
                       "label": _("Quotation"),
                       "description": _("Quotation")
                   },
                   {
                       "type": "doctype",
                       "name": "Supplier Quotation",
                       "label": _("Supplier Quotation"),
                       "description": _("Supplier Quotation")
                   },
                   {
                       "type": "doctype",
                       "name": "Supplier",
                       "label": _("Supplier"),
                       "description": _("Supplier")
                   }
            ]
        },
        {
            "label": _("Marketing"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Web Page",
                       "label": _("Web Page"),
                       "description": _("Web Page")
                   },
                   {
                       "type": "doctype",
                       "name": "Newsletter",
                       "label": _("Newsletter"),
                       "description": _("Newsletter")
                   },
                   {
                       "type": "doctype",
                       "name": "File",
                       "label": _("File"),
                       "description": _("File")
                   },
                   {
                       "type": "doctype",
                       "name": "Website Settings",
                       "label": _("Website Settings"),
                       "description": _("Website Settings")
                   }
            ]
        },
        {
            "label": _("Aktivitäten"),
            "icon": "fa fa-bolt",
            "items": [
                {
                    "type": "doctype",
                    "name": "Aktivitaet",
                    "label": _("Aktivitaet"),
                    "description": _("Aktivitaet")
                },
                {
                    "type": "report",
                    "name": "Aktivitaetenliste",
                    "label": _("Aktivitaetenliste"),
                    "doctype": "Aktivitaet",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Export Kunde",
                    "label": _("Export Kunde"),
                    "doctype": "Customer",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Export Adressliste voll",
                    "label": _("Export Adressliste voll"),
                    "doctype": "Customer",
                    "is_query_report": True
                }
            ]
        }
    ]
