// Copyright (c) 2018-2020, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Anfragen und Chancen"] = {
	"filters": [
        {
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
        }
	]
};
