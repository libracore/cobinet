# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Anfrage(Document):
    def before_save(this):
        # make sure customer field is set
        if not this.kunde:
            # find contact record
            contact_matches = frappe.get_all("Contact", filters={'user': this.owner}, fields=['name'])
            if contact_matches:
                # find linked customer:
                customer_matches = frappe.get_all("Dynamic Link", filters={'parenttype': 'Contact', 'parent': contact_matches[0]['name'], 'link_doctype': 'Customer'}, fields=['link_name'])
                if customer_matches:
                    customer = frappe.get_doc("Customer", customer_matches[0]['link_name'])
                    this.kunde = customer.name
                    this.kundenname = customer.customer_name
        return
        
	pass
