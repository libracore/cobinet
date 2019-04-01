// Copyright (c) 2019, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Preisangebot', {
	refresh: function(frm) {
        create_line_chart(frm);
        
        frm.add_custom_button(__("Calculate Model"), function() {
            calculate_model(frm);
        });
	},
    item: function(frm) {
        update_title(frm);
    },
    supplier: function(frm) {
        update_title(frm);
    }
});

function update_title(frm) {
    if ((frm.doc.item) && (frm.doc.supplier)) {
        cur_frm.set_value('title', frm.doc.item + " - " + frm.doc.supplier);
    }
}

function calculate_model(frm) {
    // aggregate values
    var qtys = [];
    var totals = [];
    frm.doc.individual_prices.forEach(function(entry) {
        if (entry.qty != null) {
            qtys.push(entry.qty);
            if (entry.rate != null) {
                totals.push(entry.total);
            } else {
                totals.push(0);
            }
        }
    });
    // compute average values
    if (qtys.length > 0) {
        var avg_qty = avg(qtys);
        console.log("avg_qty: " + avg_qty);
        var avg_total = avg(totals);
        console.log("avg_total: " + avg_total + "(" + totals + ")");
        // compute sum of squares
        var sxy = 0.0;
        var sxx = 0.0;
        for( var i = 0; i < qtys.length; i++ ){
            sxy += (qtys[i] - avg_qty) * (totals[i] - avg_total);
            sxx += (qtys[i] - avg_qty) * (qtys[i] - avg_qty); 
        } 
        console.log("sxy: " + sxy);
        console.log("sxx: " + sxx);
        // compute slope
        var b = sxy / sxx;
        console.log("b: " + b);
        // compute axis offset
        var a = avg_total - (b * avg_qty);
        console.log("a: " + a);
        // set values to form
        cur_frm.set_value('onetime_cost', a);
        cur_frm.set_value('per_unit_cost', b);
        frappe.show_alert( __("Linear price model computed.") );
        // update chart
        create_line_chart(frm);
    } else {
        frappe.show_alert( __("No values found.") );
    }
}

function avg(values) {
    var sum = 0.0;
    for( var i = 0; i < values.length; i++ ){
        sum += values[i]; 
    }

    var avg = sum / values.length;
    return avg;
}

function create_line_chart(frm) {
    // aggregate values from individual points
    var qtys = [];
    var individual_totals = [];
    var calulated_totals = [];
    frm.doc.individual_prices.forEach(function(entry) {
        if (entry.qty != null) {
            qtys.push(entry.qty);
            if (entry.total != null) {
                individual_totals.push(entry.total);
            } else {
                individual_totals.push(0);
            }
            if ((frm.doc.onetime_cost) && (frm.doc.per_unit_cost)) {
                calulated_totals.push(frm.doc.onetime_cost + (entry.qty * frm.doc.per_unit_cost));
            } else {
                calulated_totals.push(0);
            }
        }
    });

    // generate chart
    var parent = document.querySelectorAll('[data-fieldname="price_chart_html"]')[0];
    let chart = new Chart( parent, {
    data: {
      labels: qtys,
      datasets: [
        {
          name: __("Indicidual Prices"), 
          type: 'line',
          values: individual_totals
        },
        {
          name: __("Price Model"), 
          type: 'line',
          values: calulated_totals
        }
      ]
    },

    title: __("Price Chart"),
    type: 'axis-mixed', 
    height: 250,
    colors: ['#002269', '#ff8300']
  });
}

frappe.ui.form.on('Preisangebot Preis', {
	qty: function(frm, cdt, cdn) {
        calculate_total(frm, cdt, cdn);
	},
    rate: function(frm, cdt, cdn) {
        calculate_total(frm, cdt, cdn);
    }
});

function calculate_total(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, 'total', child.qty * child.rate);
}
