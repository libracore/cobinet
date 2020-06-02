// Copyright (c) 2020, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Aktivitaet', {
	refresh: function(frm) {
        if (frm.doc.__islocal) {
            // new file, set defaults
            var year = new Date().getFullYear()
            var kw = getWeekNumber(new Date());
            cur_frm.set_value('jahr', year);
            cur_frm.set_value('kw', kw);
            
        }
        
        // link field filters
        cur_frm.fields_dict['contact'].get_query = function(doc) {
          return {
            filters: {
        	  "link_doctype": "Customer",
        	  "link_name": frm.doc.customer
            }
          }
        };
	},
    customer: function(frm) {
        if (frm.doc.customer) {
            // fetch customer details
            frappe.call({
                method: 'erpnextswiss.scripts.crm_tools.get_primary_customer_address',
                args: {
                    customer: frm.doc.customer
                },
                callback: function(r) {
                    if(r.message) {
                        var address = r.message;
                        cur_frm.set_value('allgemeine_nummer', address.phone);
                    } 
                }
            });
            frappe.call({
                method: 'erpnextswiss.scripts.crm_tools.get_primary_customer_contact',
                args: {
                    customer: frm.doc.customer
                },
                callback: function(r) {
                    if(r.message) {
                        var contact = r.message;
                        set_contact(contact);
                    } 
                }
            });
        }
    },
    contact: function(frm) {
        if (frm.doc.contact) {
            frappe.call({
                "method": "frappe.client.get",
                "args": {
                    "doctype": "Contact",
                    "name": frm.doc.contact
                },
                "callback": function(response) {
                    var contact = response.message;
                    set_contact(contact);
                }
            });
        }
    },
    opportunity: function(frm) {
        // update prevdoc reference to keep apportunity dashboard working 
        cur_frm.set_value('prevdoc_docname', frm.doc.opportunity);
        // fetch customer from opportunity (allows routing)
        if (frm.doc.opportunity) {
            frappe.call({
               method: "frappe.client.get",
               args: {
                    "doctype": "Opportunity",
                    "name": frm.doc.opportunity
               },
               callback: function(response) {
                    var opportunity = response.message;
                    if (opportunity) {
                       cur_frm.set_value('customer', opportunity.party_name);
                    }
               }
            });
        }
    }
});

function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7);
    // Return array of year and week number
    return weekNo;
}

function set_contact(contact) {
    cur_frm.set_value('contact', contact.name);
    cur_frm.set_value('telefon', contact.phone);
    cur_frm.set_value('mobile_no', contact.mobile_no);
    cur_frm.set_value('email', contact.email_id);
    cur_frm.set_value('contact_person', (contact.first_name||"") + " " + (contact.last_name||""));
    cur_frm.set_value('funktion', contact.designation);
}
