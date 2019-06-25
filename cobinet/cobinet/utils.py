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
    return recursive_items

"""
    This function will check the offers for each BOM item recursively
    -item_code: item code for the base item
    -qty: number of units
"""
@frappe.whitelist()
def get_child_items_with_offer(item_code, qty):
    default_bom = find_default_bom(item_code)
    if default_bom:
        # children = get_child_items_with_offer_from_bom(item_code, default_bom, qty)
        children = build_bom_list_with_offer(item_code, default_bom, qty)
    else:
        children = None
    return children
    
def get_child_items_with_offer_from_bom(item_code, bom_no, qty):
    children = []
    # find BOM items with qty and sub-BOMs
    sql_query = """SELECT
                 `tabBOM Item`.`item_code` AS `item_code`,
                 `tabBOM Item`.`qty` AS `qty`,
                 IFNULL(`tabBOM Item`.`bom_no`, '') AS `bom_no`
               FROM `tabBOM Item`
               WHERE
                   `parent` = '{bom}'
               ORDER BY `idx` ASC;""".format(bom=bom_no)
    items = frappe.db.sql(sql_query, as_dict=True)
    # recursively check child items
    for child in items:
        # try to expand
        if child['bom_no'] != "":
            sub_children = get_child_items_with_offer_from_bom(child['item_code'], child['bom_no'], qty)
        else:
            sub_children = []
        # append child node itself
        child['parent'] = item_code
        children.append(child)
        # add sub children (if available)
        for sub_child in sub_children:
            sub_child['parent'] = child['item_code']
            children.append(sub_child)
    # compute best rates (backwards)
    for child in children[::-1]:
        child['offer'] = get_best_offer(child['item_code'], (float(qty) * float(child['qty'])))
        # compensate rate to be per unit
        child['offer']['rate'] = float(child['offer']['rate']) / float(qty)
        if child['bom_no'] != "":
            # compute BOM rate from children (include BOM assembly cost if available)
            if child['offer']['rate']:
                bom_rate = child['offer']['rate']
            else:
                bom_rate = 0.0
            for bom_child in children:
                if bom_child['parent'] == child['item_code']:
                    bom_rate += bom_child['offer']['rate'] * bom_child['qty']
            child['rate'] = bom_rate
       
    return children

def build_bom_list_with_offer(item_code, bom_no, qty):
    consolidated_bom_items = build_bom_item_list(item_code, bom_no, qty)
    # add offer for each item
    for item in consolidated_bom_items:
        item['offer'] = get_best_offer(item['item_code'], (float(qty) * float(item['qty'])))
        # compensate rate to be per unit
        item['offer']['rate'] = float(item['offer']['rate']) / float(qty)
    return consolidated_bom_items
"""
This function build an item list with quantity per item
"""
def build_bom_item_list(item_code, bom_no, qty):
    item_list = recursive_get_bom_item_list(item_code, bom_no, qty)
    # consolidate list: filter out duplicates
    unique_items = []
    for item in item_list:
        if item['item_code'] not in unique_items:
            unique_items.append(item['item_code'])
    consolidated_children = []
    for item in unique_items:
        consolidated_item = {
            'qty': 0,
            'item_code': item
        }
        for child in item_list:
            if child['item_code'] == item:
                consolidated_item['bom_no'] = child['bom_no']
                consolidated_item['qty'] = consolidated_item['qty'] + child['qty']
        consolidated_children.append(consolidated_item)
    return consolidated_children
        
def recursive_get_bom_item_list(item_code, bom_no, qty, multiplier=1):
    children = []
    # find BOM items with qty and sub-BOMs
    sql_query = """SELECT
                 `tabBOM Item`.`item_code` AS `item_code`,
                 ({multiplier} * `tabBOM Item`.`qty`) AS `qty`,
                 IFNULL(`tabBOM Item`.`bom_no`, '') AS `bom_no`
               FROM `tabBOM Item`
               WHERE
                   `parent` = '{bom}'
               ORDER BY `idx` ASC;""".format(bom=bom_no, multiplier=multiplier)
    items = frappe.db.sql(sql_query, as_dict=True)
    # build BOM item list
    for child in items:
        # try to expand
        if child['bom_no'] != "":
            sub_children = recursive_get_bom_item_list(
                child['item_code'], child['bom_no'], qty, child['qty'] * multiplier)
        else:
            sub_children = []     
        # append child node itself
        child['parent'] = item_code
        children.append(child)
        # add sub children (if available)
        for sub_child in sub_children:
            sub_child['parent'] = child['item_code']
            children.append(sub_child) 
    return children
        
"""
    This function will return a list of all items (recursively through the BOM) of an item
"""
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

""" 
    This function will return the best offer for an item
"""
def get_best_offer(item_code, qty):
    # get valid prices for this item/qty, first is cheapest offer
    qty = float(qty)
    sql_query = """SELECT
                 (`tabPreisangebot`.`onetime_cost` 
                  + `tabPreisangebot`.`external_onetime_cost`
                  + `tabPreisangebot`.`perbatch_cost`
                  + {qty} * `tabPreisangebot`.`per_unit_cost`) AS `rate`,
                 `tabPreisangebot`.`supplier` AS `supplier`,
                 `tabPreisangebot`.`supplier_name` AS `supplier_name`,
                 `tabPreisangebot`.`name` AS `reference`,
                 `tabPreisangebot`.`conditions` AS `conditions`,
                 (SELECT COUNT(`name`) FROM `tabPreisangebot`                
                  WHERE
                    `docstatus` = 1
                    AND (`valid_until` IS NULL OR `valid_until` >= CURDATE())
                    AND `item` = '{item}'
                    AND {qty} >= `minimum_qty`
                    AND `ignore` = 0) AS `count`,
                 {qty} AS `qty`
               FROM `tabPreisangebot`
               WHERE
                   `docstatus` = 1
                   AND (`valid_until` IS NULL OR `valid_until` >= CURDATE())
                   AND `item` = '{item}'
                   AND {qty} >= `minimum_qty`
                   AND `ignore` = 0
               ORDER BY `rate` ASC
               LIMIT 1;""".format(item=item_code, qty=qty)
    try:
        best_offer = frappe.db.sql(sql_query, as_dict=True)[0]
    except Exception as e:
        best_offer = {'rate': 0, 'supplier': None, 'supplier_name': None, 'reference': None, 'conditions': None, 'error': e}
    return best_offer
