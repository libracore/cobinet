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
        {"label": _("Formel"), "fieldname": "formel", "fieldtype": "Data", "width": 100},
        {"label": _("Nr"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 50},
        {"label": _("Kundenname"), "fieldname": "customer_name", "fieldtype": "Data", "width": 120},
        {"label": _("Homepage"), "fieldname": "homepage", "fieldtype": "Data", "width": 150},
        {"label": _("Standard Email"), "fieldname": "email", "fieldtype": "Data",  "width": 150},
        {"label": _("Telefonnummer Zentrale"), "fieldname": "phone", "fieldtype": "Data",  "width": 150},
        {"label": _("Adresse"), "fieldname": "address_line1", "fieldtype": "Data", "width": 200},
        {"label": _("Zusatzadresse"), "fieldname": "address_line2", "fieldtype": "Data", "width": 200},
        {"label": _("PLZ"), "fieldname": "pincode", "fieldtype": "Data", "width": 50},
        {"label": _("Ort"), "fieldname": "city", "fieldtype": "Data", "width": 150},
        {"label": _("Kontakt"), "fieldname": "contact", "fieldtype": "Link", "options": "Contact", "width": 50},
        {"label": _("Vorname"), "fieldname": "first_name", "fieldtype": "Data", "width": 100},
        {"label": _("Nachname"), "fieldname": "last_name", "fieldtype": "Data", "width": 100},
        {"label": _("Email"), "fieldname": "contact_email", "fieldtype": "Data", "width": 100},
        {"label": _("Telefon"), "fieldname": "contact_phone", "fieldtype": "Data", "width": 100},
        {"label": _("Mobile"), "fieldname": "contact_mobile", "fieldtype": "Data", "width": 100},
        {"label": _("Bezeichnug"), "fieldname": "bezeichnung", "fieldtype": "Data", "width": 150},
        {"label": _("Anrede"), "fieldname": "salutation", "fieldtype": "Data", "width": 50},
        {"label": _("Interner Status"), "fieldname": "interner_status", "fieldtype": "Data", "width": 100},
        {"label": _("Branche"), "fieldname": "branche", "fieldtype": "Link", "options": "Branche", "width": 250},
        {"label": _("Nähere Umschreibung"), "fieldname": "naehere_umschreibung", "fieldtype": "Small Text", "width": 250},        
    ]
    
def get_data(filters):
            
    sql_query = """SELECT 
          CONCAT("=Kundendatenbank!A", (CAST(SUBSTRING(`tabCustomer`.`name`, 3, 4) AS INT) + 2))  AS `formel`,
          `tabCustomer`.`name` AS `customer`,
          `tabCustomer`.`customer_name` AS `customer_name`,
          `tabCustomer`.`website` AS `homepage`,
          `tabAddress`.`email_id` AS `email`,
          `tabAddress`.`phone` AS `phone`,
          `tabAddress`.`address_line1` AS `address_line1`,
          `tabAddress`.`address_line2` AS `address_line2`,
          `tabAddress`.`pincode` AS `pincode`,
          `tabAddress`.`city` AS `city`,
          `tabContact`.`name` AS `contact`,
          `tabContact`.`first_name` AS `first_name`,
          `tabContact`.`last_name` AS `last_name`,
          `tabContact`.`email_id` AS `contact_email`,
          `tabContact`.`phone` As `contact_phone`,
          `tabContact`.`mobile_no` AS `contact_mobile`,
          `tabContact`.`bezeichnung` AS `bezeichnung`,
          `tabContact`.`salutation` AS `salutation`,
          `tabContact`.`interner_status` AS `interner_status`,
          `tabCustomer`.`branche` AS `branche`,
          `tabCustomer`.`naehere_umschreibung` AS `naehere_umschreibung`
        FROM `tabCustomer`
        JOIN `tabDynamic Link` AS `DL1` ON (`tabCustomer`.`name` = `DL1`.`link_name` AND `DL1`.`link_doctype` = 'Customer' AND `DL1`.`parenttype` = 'Contact')
        LEFT JOIN `tabContact` ON `DL1`.`parent` = `tabContact`.`name`
        JOIN `tabDynamic Link` AS `DL2` ON (`tabCustomer`.`name` = `DL2`.`link_name` AND `DL2`.`link_doctype` = 'Customer' AND `DL2`.`parenttype` = 'Address')
        LEFT JOIN `tabAddress` ON `DL2`.`parent` = `tabAddress`.`name`
        ORDER BY `tabCustomer`.`name` ASC;
      """

    data = frappe.db.sql(sql_query, as_dict=1)

    return data
