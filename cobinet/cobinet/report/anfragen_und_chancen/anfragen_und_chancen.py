# Copyright (c) 2018-2020, libracore and contributors
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
        {"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "options": "Opportunity", "width": 75},
        {"label": _("To discuss"), "fieldname": "to_discuss", "fieldtype": "Data", "width": 300},
        {"label": _("Datum"), "fieldname": "transaction_date", "fieldtype": "Date", "width": 90},
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 80},
        {"label": _("Kundenname"), "fieldname": "customer_name", "fieldtype": "Data",  "width": 225},
        {"label": _("Wahrscheinlichkeit"), "fieldname": "probability", "fieldtype": "Percent",  "width": 75},
        {"label": _("Volume"), "fieldname": "volume", "fieldtype": "Currency", "width": 110},
        {"label": _(""), "fieldname": "blank", "fieldtype": "Data", "width": 10}
    ]
    
def get_data(filters):
    if not filters.customer:
        filters.customer = "%"
                    
    sql_query = """SELECT
             `name` AS `name`,
             `to_discuss` AS `to_discuss`,
             `transaction_date` AS `transaction_date`,
             `party_name` AS `customer`,
             `customer_name` AS `customer_name`,
             `wahrscheinlichkeit` AS `probability`,
             `volume` AS `volume`
         FROM `tabOpportunity`
         WHERE `party_name` LIKE '{customer}';
      """.format(customer=filters.customer)

    data = frappe.db.sql(sql_query, as_dict=1)

    return data
