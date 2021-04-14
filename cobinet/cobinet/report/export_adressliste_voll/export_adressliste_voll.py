# Copyright (c) 2020-2021, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
import json

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"label": _("Formel"), "fieldname": "formel", "fieldtype": "Data", "width": 100},
        {"label": _("Nr"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 55},
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
          `tUAdr`.`email_id` AS `email`,
          `tUAdr`.`phone` AS `phone`,
          `tUAdr`.`address_line1` AS `address_line1`,
          `tUAdr`.`address_line2` AS `address_line2`,
          `tUAdr`.`pincode` AS `pincode`,
          `tUAdr`.`city` AS `city`,
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
        LEFT JOIN (
            SELECT *
            FROM (
              SELECT 
                `tabAddress`.`email_id` AS `email_id`,
                `tabAddress`.`phone` AS `phone`,
                `tabAddress`.`address_line1` AS `address_line1`,
                `tabAddress`.`address_line2` AS `address_line2`,
                `tabAddress`.`pincode` AS `pincode`,
                `tabAddress`.`city` AS `city`,
                `tDL`.`link_name` AS `customer`
              FROM `tabAddress`
              LEFT JOIN `tabDynamic Link` AS `tDL` ON (
                `tabAddress`.`name` = `tDL`.`parent` 
                AND `tDL`.`link_doctype` = 'Customer' 
                AND `tDL`.`parenttype` = 'Address'
              )
              ORDER BY `tabAddress`.`is_primary_address` DESC
            ) AS `tAdr`
            GROUP BY `tAdr`.`customer`
        ) AS `tUAdr` ON `tabCustomer`.`name` = `tUAdr`.`customer`
        ORDER BY `tabCustomer`.`name` ASC;
      """

    data = frappe.db.sql(sql_query, as_dict=1)

    return data

"""
CobiExport: allow to create a complete export object
"""
@frappe.whitelist()
def customer_export(customer, with_details=False):
    customer = frappe.get_doc("Customer", customer)
    data = {
        'customer': customer.as_dict(),
        'contacts': [],
        'addresses': []
    }
    contact_links = frappe.get_all("Dynamic Link", filters={'link_name': customer.name, 'link_doctype': 'Customer', 'parenttype': 'Contact'}, fields=['parent'])
    # fetch linked records
    for l in contact_links:
        contact = frappe.get_doc("Contact", l['parent'])
        data['contacts'].append(contact.as_dict())
    address_links = frappe.get_all("Dynamic Link", filters={'link_name': customer.name, 'link_doctype': 'Customer', 'parenttype': 'Address'}, fields=['parent'])
    for l in address_links:
        address = frappe.get_doc("Address", l['parent'])
        data['addresses'].append(address.as_dict())
    # remove details unless selected
    if not with_details:
        data['customer']['customer_details'] = None
    return json.dumps(data, default=str)
