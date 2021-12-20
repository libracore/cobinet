# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, libracore and contributors
# For license information, please see license.txt
#
# Call from
#   /api/method/cobinet.cobinet.calendar.get_event?event=<event_name>
#
# Returned is an iCalendar feed (read only)
#

# imports
from __future__ import unicode_literals
import frappe
from frappe import _
from icalendar import Calendar, Event, Todo
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_event(event):
    frappe.local.response.filename = "calendar.ics"
    calendar = create_event(event)
    if calendar:
        frappe.local.response.filecontent = calendar.to_ical()
    else:
        frappe.local.response.filecontent = "Oops, an error occurred."
    frappe.local.response.type = "download"

def create_event(event):
    # initialise calendar
    cal = Calendar()

    # set properties
    cal.add('prodid', '-//cobinet//libracore//')
    cal.add('version', '1.0')

    # get event data
    if not frappe.db.exists("Anlass", event):
        return None
    anlass = frappe.get_doc("Anlass", event)
    
    from_date = datetime.strptime("{0} 00:00".format(anlass.date), "%Y-%m-%d %H:%M")
    to_date = datetime.strptime("{0} 23:59".format(anlass.date), "%Y-%m-%d %H:%M")
    time_fragments = (anlass.time or "").split(" ")
    if len(time_fragments) >= 2:
        from_time = time_fragments[0]
        to_time = time_fragments[-1]
        try:
            from_date = datetime.strptime("{0} {1}".format(anlass.date, from_time), "%Y-%m-%d %H:%M")
        except:
            pass
        try:
            to_date = datetime.strptime("{0} {1}".format(anlass.date, to_time), "%Y-%m-%d %H:%M")
        except:
            pass
        
    
    # create event
    event = Event()
    event.add('summary', anlass.title)
    event.add('dtstart', from_date)
    event.add('dtend', to_date)
    event.add('dtstamp', anlass.modified)
    event.add('description', anlass.description)
    # add to calendar
    cal.add_component(event)
    
    # return calendar object
    return cal
