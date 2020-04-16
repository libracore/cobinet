// Copyright (c) 2020, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Aktivtätenliste"] = {
	"filters": [
        {
			"fieldname":"verantwortlich",
			"label": __("Verantwortlich"),
			"fieldtype": "Link",
			"options": "User"
        },
        {
			"fieldname":"week",
			"label": __("KW"),
			"fieldtype": "Int",
			"default": getWeekNumber(new Date()),
            "reqd": 1
        }
	]
};

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
