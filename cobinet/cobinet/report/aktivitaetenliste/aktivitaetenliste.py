# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"label": _("Aktivität"), "fieldname": "activity", "fieldtype": "Link", "options": "Aktivitaet", "width": 40},
        {"label": _("Verantwortlich"), "fieldname": "verantwortlich", "fieldtype": "Link", "options": "User", "width": 40},
        {"label": _("Prio"), "fieldname": "prio", "fieldtype": "Select", "width": 50},
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 80},
        {"label": _("Kundenname"), "fieldname": "customer_name", "fieldtype": "Data",  "width": 100},
        {"label": _("Allg. Tel."), "fieldname": "tel", "fieldtype": "Data",  "width": 120},
        {"label": _("Kontakt"), "fieldname": "contact", "fieldtype": "Link", "options": "Contact", "width": 40},
        {"label": _("Kontaktperson"), "fieldname": "contact_person", "fieldtype": "Data", "width": 100},
        {"label": _("Phone"), "fieldname": "phone", "fieldtype": "Data", "width": 120},
        #{"label": _("Email"), "fieldname": "email", "fieldtype": "Data", "width": 100},
        {"label": _("Nähere Umschreibung"), "fieldname": "naehere_umschreibung", "fieldtype": "Data", "width": 100},
        {"label": _("Aufgabe"), "fieldname": "aufgabe", "fieldtype": "Data", "width": 750}
    ]
    
def get_data(filters):
    if not filters.verantwortlich:
        filters.verantwortlich = "%"
    if not filters.week:
        today = datetime.date.today()
        filters.week = int(today.strftime("%V"))
    if not filters.year:
        today = datetime.date.today()
        filters.year = int(today.strftime("%Y"))
    if not filters.prio:
        filters.prio = "%"
                    
    sql_query = """SELECT
             `name` AS `activity`,
             `verantwortlich` AS `verantwortlich`,
             `customer` AS `customer`,
             `customer_name` AS `customer_name`,
             `allgemeine_nummer` AS `tel`,
             `contact` AS `contact`,
             `contact_person` AS `contact_person`,
             `telefon` AS `phone`,
             `email` AS `email`,
             `naehere_umschreibung` AS `naehere_umschreibung`,
             `aufgabe` AS `aufgabe`,
             `prio` AS `prio`
         FROM `tabAktivitaet`
         WHERE `kw` = {week} 
            AND `erledigt` = 0
            AND (`verantwortlich` IS NULL OR `verantwortlich` LIKE '{verantwortlich}')
            AND `prio` LIKE '{prio}'
            AND `jahr` = {year}
         ;
      """.format(week=filters.week, verantwortlich=filters.verantwortlich, prio=filters.prio, year=filters.year)

    data = frappe.db.sql(sql_query, as_dict=1)

    return data
