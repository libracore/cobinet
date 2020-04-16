# -*- coding: utf-8 -*-
# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime

class Aktivitaet(Document):
	pass

"""
This function will move all current open activities to the next week
"""
def move_activities_to_next_week():
    # prepare date ranges
    today = datetime.date.today()
    week = int(today.strftime("%V"))
    year = int(today.strftime("%Y"))
    next_date = today + datetime.timedelta(days=4)
    next_week = int(next_date.strftime("%V"))
    next_year = int(next_date.strftime("%Y"))
        
    activities = frappe.get_all("Aktivitaet", filters={'kw': week, 'erledigt': 0}, fields=['name'])
    for a in activities:
        activity = frappe.get_doc("Aktivitaet", a['name'])
        activity.kw = next_week
        activity.year = next_year
        activity.save()
    
    frappe.db.commit()
    return
