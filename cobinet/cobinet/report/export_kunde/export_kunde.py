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
        {"label": _("Nr"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 50},
        {"label": _("Kundenname"), "fieldname": "customer_name", "fieldtype": "Data", "width": 120},
        {"label": _("Homepage"), "fieldname": "homepage", "fieldtype": "Data", "width": 100},
        {"label": _("E-Mail-Adresse"), "fieldname": "email", "fieldtype": "Data",  "width": 100},
        {"label": _("Telefonnummer"), "fieldname": "phone", "fieldtype": "Data",  "width": 120},
        {"label": _("Adresse"), "fieldname": "address_line1", "fieldtype": "Data", "width": 120},
        {"label": _("PLZ"), "fieldname": "pincode", "fieldtype": "Data", "width": 60},
        {"label": _("Ort"), "fieldname": "city", "fieldtype": "Data", "width": 100},
        {"label": _("Klassifizierung generell"), "fieldname": "klassifizierung", "fieldtype": "Link", "options": "Klassifizierung", "width": 100},
        {"label": _("Status generell"), "fieldname": "status", "fieldtype": "Link", "options": "Status", "width": 100},
        {"label": _("Grobeinteilung"), "fieldname": "grobeinteilung", "fieldtype": "Link", "options": "Grobeinteilung", "width": 250},
        {"label": _("Branche"), "fieldname": "branche", "fieldtype": "Link", "options": "Branche", "width": 250},
        {"label": _("Nähere Umschreibung"), "fieldname": "naehere_umschreibung", "fieldtype": "Small Text", "width": 250},        
    ]
    
def get_data(filters):
            
    sql_query = """SELECT
             `tabCustomer`.`name` AS `customer`,
             `tabCustomer`.`customer_name` AS `customer_name`,
             `tabCustomer`.`website` AS `homepage`,
             `tabAddress`.`email_id` AS `email`,
             `tabAddress`.`phone` AS `phone`,
             `tabAddress`.`address_line1` AS `address_line1`,
             `tabAddress`.`pincode` AS `pincode`,
             `tabAddress`.`city` AS `city`,
             `tabCustomer`.`klassifizierung` AS `klassifizierung`,
             `tabCustomer`.`status` AS `status`,
             `tabCustomer`.`grobeinteilung` AS `grobeinteilung`,
             `tabCustomer`.`branche` AS `branche`,
             `tabCustomer`.`naehere_umschreibung` AS `naehere_umschreibung`
         FROM `tabCustomer`
         LEFT JOIN `tabDynamic Link` ON (
             `tabDynamic Link`.`link_doctype` = "Customer" 
             AND `tabDynamic Link`.`parenttype` = "Address"
             AND `tabDynamic Link`.`link_name` = `tabCustomer`.`name`)
         LEFT JOIN `tabAddress` ON `tabAddress`.`name` = `tabDynamic Link`.`parent`
         WHERE `tabCustomer`.`disabled` = 0;
      """

    data = frappe.db.sql(sql_query, as_dict=1)

    return data
