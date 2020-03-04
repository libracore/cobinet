/* add Preisangebot to supplier dashboard, only works for v11 and above */
try {
    cur_frm.dashboard.add_transactions([
        {
            'label': 'Cobinet',
            'items': ['Geheimhaltevereinbarung']
        }
    ]);
} catch { /* do nothing for older versions */ }
