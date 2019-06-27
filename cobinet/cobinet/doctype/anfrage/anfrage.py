# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime

class Anfrage(Document):
    def before_save(self):
        # make sure customer field is set
        if not self.kunde:
            # find contact record
            contact_matches = frappe.get_all("Contact", filters={'user': self.owner}, fields=['name'])
            if contact_matches:
                # find linked customer:
                customer_matches = frappe.get_all("Dynamic Link", filters={'parenttype': 'Contact', 'parent': contact_matches[0]['name'], 'link_doctype': 'Customer'}, fields=['link_name'])
                if customer_matches:
                    customer = frappe.get_doc("Customer", customer_matches[0]['link_name'])
                    self.kunde = customer.name
                    self.kundenname = customer.customer_name
        # set default min quotation validity date
        if not self.quotation_min_validity_date:
            self.quotation_min_validity_date = datetime.date.today() + datetime.timedelta(days=90)
        return
        
    def after_insert(self):
        # after a new record has been inserted, create a linked opportunity
        new_opty = frappe.get_doc({
            "doctype": "Opportunity",
            "enquiry_from": "Customer",
            "opportunity_from": "Customer",     # v11 compatibility
            "customer": self.kunde,
            "party_name": self.kunde,           # v11 compatibility
            "von_anfrage": self.name
        })
        new_opty.insert()
        return
        
    pass
