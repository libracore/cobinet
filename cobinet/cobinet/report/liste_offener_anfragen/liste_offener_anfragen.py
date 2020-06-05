# Copyright (c) 2020, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 55},
        {"label": _("Customer name"), "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": _("Opportunity"), "fieldname": "opportunity", "fieldtype": "Link", "options": "Opportunity", "width": 75},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 75},
        {"label": _("Betreff"), "fieldname": "betreff", "fieldtype": "Data", "width": 150},
        {"label": _("Wiedervorlage"), "fieldname": "next_contact", "fieldtype": "Data", "width": 75},
        {"label": _("Angebotstermin"), "fieldname": "angebotstermin", "fieldtype": "date", "width": 90},
        # {"label": _("Anfragetext"), "fieldname": "anfragetext", "fieldtype": "Small Text", "width": 100},
        {"label": _("Anfrage 1"), "fieldname": "anfrage_1", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 2"), "fieldname": "anfrage_2", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 3"), "fieldname": "anfrage_3", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 4"), "fieldname": "anfrage_4", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 5"), "fieldname": "anfrage_5", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 6"), "fieldname": "anfrage_6", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 7"), "fieldname": "anfrage_7", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 8"), "fieldname": "anfrage_8", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 9"), "fieldname": "anfrage_9", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 10"), "fieldname": "anfrage_10", "fieldtype": "data", "width": 150}
    ]
    
def get_data(filters):                   
    sql_query = """SELECT
             `party_name` AS `customer`,
             `customer_name` AS `customer_name`,
             `name` AS `opportunity`,
             IFNULL(`betreff`, "-") AS `betreff`,
             `angebotstermin` AS `angebotstermin`,
             `status` AS `status`,
             IFNULL(`to_discuss`, "-") AS `anfragetext`,
             IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
               FROM `tabOpportunity Anfrage`
               WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 1), "-") AS `anfrage_1`,
             IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
               FROM `tabOpportunity Anfrage`
               WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 2), "-") AS `anfrage_2`,
             IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
               FROM `tabOpportunity Anfrage`
               WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 3), "-") AS `anfrage_3`,
             IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
               FROM `tabOpportunity Anfrage`
               WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 4), "-") AS `anfrage_4`,
             IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 5), "-") AS `anfrage_5`,
              IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 6), "-") AS `anfrage_6`,
              IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 7), "-") AS `anfrage_7`,
              IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 8), "-") AS `anfrage_8`,
              IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 9), "-") AS `anfrage_9`,
              IFNULL((SELECT 
               CONCAT("<span style='color: ", 
                 IF(`status` = "Offen", "blue",
                  IF(`status` = "Angeboten", "green", "red")
                 ), "; background-color: ",
                 IF(`selected` = "Ausgewählt", "#DAF7A6",
                  IF(`selected` = "Abgesagt", "#FFE5CC", "white")
                 ), "; '>", 
                 `supplier_name`, ": ", `status`, " / ", `selected`, "</span>")
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 10), "-") AS `anfrage_10`,
              (SELECT CONCAT(`jahr`, " / ", `kw`) 
               FROM `tabAktivitaet` 
               WHERE `opportunity` = `tabOpportunity`.`name` LIMIT 1) AS `next_contact`
         FROM `tabOpportunity`
         WHERE `status` IN ("Open", "Replied", "Quotation")
         ORDER BY `name` DESC;
      """

    data = frappe.db.sql(sql_query, as_dict=1)

    return data

