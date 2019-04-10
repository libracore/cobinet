# -*- coding: utf-8 -*-
# Copyright (c) 2019, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Preisangebot(Document):
    def validate(self):
        
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
