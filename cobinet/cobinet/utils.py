# -*- coding: utf-8 -*-
# Copyright (c) 2019, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

# this function will link the address from a customer record to the contact
def load_address_to_contact():
    contacts = frappe.get_all("Contact", fields=['name'])
    for contact in contacts:
        # TODO: add address lookup
        sql_query = """SELECT `parent` FROM `tabDynamic Link` 
           WHERE `parenttype` = "Address" 
           AND `link_doctype` = "Customer" 
           AND `link_name` = (SELECT `link_name` 
              FROM `tabDynamic Link` 
              WHERE `parenttype` = "Contact" AND `parent` = "{0}");""".format(contact['name'])
        print(sql_query)
        address = frappe.db.sql(sql_query, as_dict=True)
        try:
            if address:
                contact_record = frappe.get_doc('Contact', contact)
                contact_record.adresse = address[0]['parent']
                contact_record.save()
                frappe.db.commit()
                print("Updated {0}".format(contact))
        except:
            print("Error updating {0}".format(contact))

# this function will return suitable suppliers for an item
@frappe.whitelist()
def get_suppliers(item_code):
    sql_query = """SELECT * FROM (SELECT
                    `tabSupplier`.`name`, `tabSupplier`.`supplier_name`, `tabSupplier Technologie`.`technologie`,
                    `tabSupplier`.`cobinet_member`
                   FROM `tabSupplier Technologie`
                   LEFT JOIN `tabSupplier` ON `tabSupplier`.`name` = `tabSupplier Technologie`.`parent`
                   WHERE `technologie` IN 
                     /* required technologies */
                     (SELECT `item_group` AS `technologie`
                       FROM `tabItem` 
                       WHERE `name` = '{item_code}'
                     UNION SELECT `technologie` 
                       FROM `tabSupplier Technologie`
                       WHERE `parenttype` = 'Item'
                         AND `parent` = '{item_code}')
                   GROUP BY `tabSupplier Technologie`.`parent`
                   HAVING COUNT(DISTINCT `tabSupplier Technologie`.`technologie`) = (
                     /* number of mandatory attributes */
                     SELECT COUNT(*) FROM (SELECT `item_group`  AS `technologie`
                       FROM `tabItem`
                       WHERE `name` = '{item_code}'
                     UNION SELECT `technologie`
                       FROM `tabSupplier Technologie`
                       WHERE `parenttype` = 'Item'
                         AND `parent` = '{item_code}') AS `tblCount`)) AS `suppliers`
                   ORDER BY `suppliers`.`supplier_name` ASC;""".format(item_code=item_code)
    supplier_matches = frappe.db.sql(sql_query, as_dict=True)
    return {'suppliers': supplier_matches }

@frappe.whitelist()
def get_suppliers_by_technology(technology):
    sql_query = """SELECT
                     `tabSupplier`.`name`, `tabSupplier`.`supplier_name`, `tabSupplier Technologie`.`technologie`
                   FROM `tabSupplier Technologie`
                   LEFT JOIN `tabSupplier` ON `tabSupplier`.`name` = `tabSupplier Technologie`.`parent`
                   WHERE
                       `technologie` = '{technology}';""".format(technology=technology)
    supplier_matches = frappe.db.sql(sql_query, as_dict=True)
    return {'suppliers': supplier_matches }

# this function is to correct an issue with the new data structure of the opportunity in v11.1.24 (customer reference missing)
def fetch_customer_for_opportunity():
    opportunities = frappe.get_all("Opportunity", fields=['name', 'customer_name'])
    for o in opportunities:
        if o['customer_name']:
            customer = frappe.get_all("Customer", filters={'customer_name': o['customer_name']}, fields=['name'])
            if customer:
                print("Customer: {0}".format(customer[0]['name']))
                opty = frappe.get_doc("Opportunity", o['name'])
                opty.party_name = customer[0]['name']
                opty.save()
                frappe.db.commit()
                print("Updated {0}".format(opty.name))
    return

def get_recursive_items(item_code):
    #root = frappe.get_doc("BOM", bom_root_item)
    #print("Name: {0}".format(root.name))
    #recursive_items = root.get_exploded_items()
    #recursive_items = root.get_child_exploded_items(root.name, 1)
    #print("{0}".format(recursive_items))
    recursive_items = get_child_items(item_code)
    print("{0}".format(recursive_items))
    return

@frappe.whitelist()
def get_child_items(item_code):
    default_bom = find_default_bom(item_code)
    children = []
    if default_bom:
        # item has a BOM, expand
        sql_query = """SELECT
                     `tabBOM Item`.`item_code` AS `item_code`
                   FROM `tabBOM Item`
                   WHERE
                       `parent` = '{bom}'
                    ORDER BY `idx` ASC;""".format(bom=default_bom)
        items = frappe.db.sql(sql_query, as_dict=True)
        # recursively check child items
        for child in items:
            # try to expand
            sub_children = get_child_items(child['item_code'])
            # if there are sub children, this is a BOM node
            if sub_children:
                child['is_bom'] = 1
            # append child node itself
            children.append(child)
            # add sub children (if available)
            for sub_child in sub_children:
                children.append(sub_child)
             
    return children
    
def find_default_bom(item_code):
    sql_query = """SELECT
                     `tabBOM`.`name`
                   FROM `tabBOM`
                   WHERE
                       `docstatus` = 1 
                       AND `is_default` = 1
                       AND `item` = '{item}';""".format(item=item_code)
    try:
        default_bom = frappe.db.sql(sql_query, as_dict=True)[0]['name']
    except:
        default_bom = None
    return default_bom
