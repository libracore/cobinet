# -*- coding: utf-8 -*-
# Copyright (c) 2021, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Anlass(Document):
    pass


@frappe.whitelist(allow_guest=True)
def get_events():
    #events = frappe.get_all("Anlass", filters={'active': 1}, 
    #    fields=['name', 'with_subscription', 'title', 'location', 'date', 'time', 'description', 'attachments']
    #)
    events = frappe.db.sql("""
        SELECT 
            `name`, 
            `with_subscription`, 
            `title`, 
            `location`, 
            `date`, 
            `time`, 
            `description`, 
            (SELECT `file_url` 
             FROM `tabFile` 
             WHERE `attached_to_doctype` = "Anlass" 
               AND `attached_to_name` = `tabAnlass`.`name`
             LIMIT 1) AS `attachment`
        FROM `tabAnlass`
        WHERE `active` = 1
        ORDER BY `date` ASC;
        """, as_dict=True)
        
    data = {
        'events': events
    }
    
    html = frappe.render_template('cobinet/templates/includes/event.html', data)
    
    return html
