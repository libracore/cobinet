# -*- coding: utf-8 -*-
# Copyright (c) 2019, libracore and contributors
# For license information, please see license.txt
"""
    Manual tests
    
    bench execute cobinet.cobinet.utils.get_recursive_items --kwargs "{'item_code': '1234'}"
    bench execute cobinet.cobinet.utils.get_best_offer --kwargs "{'item_code': '1234', 'qty': 1}"
    bench execute cobinet.cobinet.utils.get_child_items_with_offer --kwargs "{'item_code': '1234', 'qty': 1}"
    bench execute cobinet.cobinet.utils.build_bom_item_list --kwargs "{'item_code': '1234', 'qty': 1, 'bom_no': 'BOM-1234-001-2'}"
    
"""

import frappe
from cobinet.cobinet.utils import build_bom_item_list, build_bom_list_with_offer


def test_build_bom_list():
    items = build_bom_item_list(item_code='1234', qty=1, bom_no='BOM-1234-001-3')
    for item in items:
        print("Item {item} - BOM {bom} - QTY {qty}".format(item=item['item_code'], bom=item['bom_no'], qty=item['qty']))
    return

def test_bom_with_offer():
    items = build_bom_list_with_offer(item_code='1234', qty=1, bom_no='BOM-1234-001-3')
    for item in items:
        print("Item {item} - BOM {bom} - QTY {qty} - Rate {rate}".format(
        item=item['item_code'], bom=item['bom_no'], qty=item['qty'], rate=item['offer']['rate']))
    return
