# -*- coding: utf-8 -*-
# Copyright (c) 2019, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
import datetime

class Preisangebot(Document):
    def validate(self):
        # make sure validity is longer than requested from request
        request_name = frappe.get_value("Item", self.item, "von_anfrage")
        if request_name:
            requested_min_validity = frappe.get_value("Anfrage", request_name, "quotation_min_validity_date")
            if requested_min_validity and self.valid_until:
                if datetime.datetime.strptime(self.valid_until, "%Y-%m-%d").date() < requested_min_validity:
                    frappe.throw( _("Please make sure that the offer is valid at least until {0}.").format(requested_min_validity) )
                    
        return
    
    def before_save(self):
        # set default validity range 90 days
        if not self.valid_until:
            self.valid_until = datetime.date.today() + datetime.timedelta(days=90)
        return
        
    def get_supplier(self, user):
        # find contact record
        contact_matches = frappe.get_all("Contact", filters={'user': user}, fields=['name'])
        if contact_matches:
            # find linked customer:
            supplier_matches = frappe.get_all("Dynamic Link", 
                filters={'parenttype': 'Contact', 'parent': contact_matches[0]['name'], 'link_doctype': 'Supplier'}, 
                fields=['link_name'])
            if supplier_matches:
                supplier = frappe.get_doc("Supplier", supplier_matches[0]['link_name'])
                self.supplier = supplier.name
                self.supplier_name = supplier.supplier_name
                return { 'supplier': supplier.name, 'supplier_name': supplier.supplier_name }
        return None

    def on_submit(self):
        # check if there is a ToDo open
        todos = frappe.get_all("ToDo", filters={'owner': self.owner, 'reference_type': 'Item', 'reference_name': self.item}, fields=['name'])
        if todos:
            # close ToDo
            record = frappe.get_doc("ToDo", todos[0]['name'])
            record.status = "Closed"
            record.save()
        return

"""
 This function is to ignore a proposed price quote, e.g. from the quotation view
"""
@frappe.whitelist()
def ignore_offer(offer_name):
    preisangebot = frappe.get_doc("Preisangebot", offer_name)
    try:
        preisangebot.ignore = 1
        preisangebot.save()
        return True
    except:
        return False
