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
        {"label": _("Betreff"), "fieldname": "betreff", "fieldtype": "Data", "width": 150},
        {"label": _("Angebotstermin"), "fieldname": "angebotstermin", "fieldtype": "date", "width": 90},
        {"label": _("Anfrage 1"), "fieldname": "anfrage_1", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 2"), "fieldname": "anfrage_2", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 3"), "fieldname": "anfrage_3", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 4"), "fieldname": "anfrage_4", "fieldtype": "data", "width": 150},
        {"label": _("Anfrage 5"), "fieldname": "anfrage_5", "fieldtype": "data", "width": 150},
    ]
    
def get_data(filters):                   
    sql_query = """SELECT
             `party_name` AS `customer`,
             `customer_name` AS `customer_name`,
             `name` AS `opportunity`,
             IFNULL(`betreff`, "-") AS `betreff`,
             `angebotstermin` AS `angebotstermin`,
             IFNULL((SELECT 
               IF(`status` = "Offen", CONCAT("<span style='color: orange;'>", `supplier_name`, ": ", `status`, "</span>"),
               IF(`status` = "Angeboten", CONCAT("<span style='color: green;'>", `supplier_name`, ": ", `status`, "</span>"),
               CONCAT("<span style='color: red;'>", `supplier_name`, ": ", `status`, "</span>")))
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 1), "-") AS `anfrage_1`,
              IFNULL((SELECT 
               IF(`status` = "Offen", CONCAT("<span style='color: orange;'>", `supplier_name`, ": ", `status`, "</span>"),
               IF(`status` = "Angeboten", CONCAT("<span style='color: green;'>", `supplier_name`, ": ", `status`, "</span>"),
               CONCAT("<span style='color: red;'>", `supplier_name`, ": ", `status`, "</span>")))
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 2), "-") AS `anfrage_2`,
              IFNULL((SELECT 
               IF(`status` = "Offen", CONCAT("<span style='color: orange;'>", `supplier_name`, ": ", `status`, "</span>"),
               IF(`status` = "Angeboten", CONCAT("<span style='color: green;'>", `supplier_name`, ": ", `status`, "</span>"),
               CONCAT("<span style='color: red;'>", `supplier_name`, ": ", `status`, "</span>")))
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 3), "-") AS `anfrage_3`,
              IFNULL((SELECT 
               IF(`status` = "Offen", CONCAT("<span style='color: orange;'>", `supplier_name`, ": ", `status`, "</span>"),
               IF(`status` = "Angeboten", CONCAT("<span style='color: green;'>", `supplier_name`, ": ", `status`, "</span>"),
               CONCAT("<span style='color: red;'>", `supplier_name`, ": ", `status`, "</span>")))
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 4), "-") AS `anfrage_4`,
              IFNULL((SELECT 
               IF(`status` = "Offen", CONCAT("<span style='color: orange;'>", `supplier_name`, ": ", `status`, "</span>"),
               IF(`status` = "Angeboten", CONCAT("<span style='color: green;'>", `supplier_name`, ": ", `status`, "</span>"),
               CONCAT("<span style='color: red;'>", `supplier_name`, ": ", `status`, "</span>")))
              FROM `tabOpportunity Anfrage`
              WHERE `parent` = `tabOpportunity`.`name` AND `idx` = 5), "-") AS `anfrage_5`
         FROM `tabOpportunity`
         WHERE `status` = "Open"
         ORDER BY `angebotstermin` ASC;
      """

    data = frappe.db.sql(sql_query, as_dict=1)

    return data

