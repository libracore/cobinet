# -*- coding: utf-8 -*-
# Copyright (c) 2019, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

# this function will link the address from a customer record to the contact
def load_address_to_contact():
    contacts = frappe.get_all("Contact", fields=['name'])
    for contact in contacts:
        # TODO: add address lookup
        sql_query = """SELECT `parent` FROM `tabDynamic Link` 
           WHERE `parenttype` = "Address" 
           AND `link_doctype` = "Customer" 
           AND `link_name` = (SELECT `link_name` 
              FROM `tabDynamic Link` 
              WHERE `parenttype` = "Contact" AND `parent` = "{0}");""".format(contact['name'])
        print(sql_query)
        address = frappe.db.sql(sql_query, as_dict=True)
        try:
            if address:
                contact_record = frappe.get_doc('Contact', contact)
                contact_record.adresse = address[0]['parent']
                contact_record.save()
                frappe.db.commit()
                print("Updated {0}".format(contact))
        except:
            print("Error updating {0}".format(contact))

