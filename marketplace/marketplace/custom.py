from __future__ import unicode_literals

import pandas as pd
import frappe
from erpnext.accounts.doctype.gl_entry.gl_entry import update_outstanding_amt
from frappe.utils import cint, cstr, formatdate, flt, getdate, nowdate, get_link_to_form
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals
from erpnext.accounts.general_ledger import make_gl_entries
# from opl_document.sinv import validate_rounding

def repair_gl_entry(doctype,docname):
	frappe.db.set_value("Stock Settings","","allow_negative_stock",1)
	
	frappe.db.sql("""DELETE FROM `tabGL Entry` where voucher_no="{}" """.format(docname))
	frappe.db.sql("""DELETE FROM `tabStock Ledger Entry` where voucher_no="{}" """.format(docname))

	doc = frappe.get_doc(doctype,docname)
	print(doc.doctype)
	print(doc.name)
	doc.update_stock_ledger()
	doc.make_gl_entries()
	frappe.db.set_value("Stock Settings","","allow_negative_stock",0)
	
	frappe.db.commit()

def repair_gl_entry_custom():
	col = ["Name","Type"]
	data = pd.read_excel (r'/home/frappe/frappe-bench/apps/marketplace/marketplace/marketplace/patch_data/tes_ste_mai.xls') 
	df = pd.DataFrame(data, columns= col)
	
	# print(str(df[col[0]][0]))
	for idx in range(len(df)):
		frappe.db.set_value("Stock Settings","","allow_negative_stock",1)
	
		frappe.db.sql("""DELETE FROM `tabGL Entry` where voucher_no="{}" """.format(df[col[0]][idx]))
		frappe.db.sql("""DELETE FROM `tabStock Ledger Entry` where voucher_no="{}" """.format(df[col[0]][idx]))

		doc = frappe.get_doc(df[col[1]][idx],df[col[0]][idx])
		print(doc.doctype)
		print(doc.name)
		doc.update_stock_ledger()
		doc.make_gl_entries()
		frappe.db.set_value("Stock Settings","","allow_negative_stock",0)
		
		frappe.db.commit()
		

	print("Sudah selesai !")


def patch_stocks():

	# col = ["Name","Type"]
	# data = pd.read_excel (r'/home/frappe/frappe-bench/apps/marketplace/marketplace/marketplace/patch_data/tes_ste_mai.xls') 
	# df = pd.DataFrame(data, columns= col)

	# for idx in range(len(df)):

	# item_code = df[col[0]][idx]
	item_code = "DC 505 / VLP - PCS"
	list_tx = frappe.db.sql("""
			SELECT
				voucher_no, voucher_type
			FROM `tabStock Ledger Entry`
			WHERE item_code = "{}"
			AND warehouse = "{}"
			ORDER BY posting_date
		""".format(item_code,"Stores - BBO"),as_dict=1)
	print(item_code)
	for tx in list_tx:
		frappe.db.set_value("Stock Settings","","allow_negative_stock",1)

		frappe.db.sql("""DELETE FROM `tabGL Entry` where voucher_no="{}" """.format(tx.voucher_no))
		frappe.db.sql("""DELETE FROM `tabStock Ledger Entry` where voucher_no="{}" """.format(tx.voucher_no))

		# print(doc.doctype)
		# print(doc.name)

		doc = frappe.get_doc(tx.voucher_type, tx.voucher_no)
		doc.update_stock_ledger()
		doc.make_gl_entries()
		frappe.db.set_value("Stock Settings","","allow_negative_stock",0)
		
		frappe.db.commit()

def test_patch():
	frappe.db.set_value("Stock Settings","","allow_negative_stock",1)
	
	ste = frappe.get_doc("Stock Entry","STE-BBO220500039")
	
	for item in ste.items:
		if item.item_code not in ["HCD 501 / GL - TR - PCS","HCD 501 / GL - BWT - PCS","HCD 505 / SL - NVT - PCS"]:
			# list_vouchers = frappe.db.get_all("Stock Ledger Entry", {"item_code":item.item_code,"warehouse":item.s_warehouse},"voucher_no")
			list_vouchers = frappe.db.sql("""
							SELECT DISTINCT voucher_no 
							FROM `tabStock Ledger Entry`
							where item_code = "{}"  
							and warehouse = "{}"
							""".format(item.item_code, item.s_warehouse),as_dict=1)
			
			print(item.item_code)
			for voucher in list_vouchers:
				doc = voucher.voucher_no
				print(doc)

				doctype = ""
				if "SINV" in doc:
					doctype = "Sales Invoice"

				if "STE" in doc:
					doctype = "Stock Entry"

				if "PREC" in doc:
					doctype = "Purchase Receipt"

				docstatus = frappe.get_value(doctype,doc,"docstatus")
				if docstatus == 1:
					repair_gl_entry(doctype,doc)
	frappe.db.set_value("Stock Settings","","allow_negative_stock",0)