# -*- coding: utf-8 -*-
# Copyright (c) 2021, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AnmeldungKundenevent(Document):
    def before_save(self): 
        self.ganzer_name = "{0} {1}".format((self.vorname or ""), (self.nachname or ""))
        return

