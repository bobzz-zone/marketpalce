from erpnext.accounts.doctype.gl_entry.gl_entry import update_outstanding_amt
import frappe

def fix():
	# PE-BBO211100371
	# PE-BBO211100372
	# PE-BBO211100373
	# PE-BBO211100374
	# PE-BBO211100375
	# PE-BBO211100376
	# PE-BBO211100377
	# PE-BBO211100378
	# PE-BBO211100379
	# PE-BBO211100380
	# PE-BBO211100381
	# PE-BBO211100383-1
	# PE-BBO211100382
	list_sinv = [
		"SINV-BBO211000487",
		"SINV-BBO211000547",
		"SINV-BBO211000554",
		"SINV-BBO211100004",
		"SINV-BBO211100427",
		"SINV-BBO211100429"]

	list_sinv = ["SINV-BBO211000547"]

	for sinv_no in list_sinv:
		sinv = frappe.get_doc("Sales Invoice", sinv_no)
		# repair_gl_entry("Sales Invoice", sinv_no)
		update_outstanding_amt(sinv.debit_to, "Customer", "Xuping Shopee Mall", "Sales Invoice", sinv.name)



def cancel():
	file = open("/home/frappe/frappe-bench/apps/marketplace/marketplace/list_pe.txt").readlines()
	# file = open("/home/frappe/frappe-bench/apps/marketplace/marketplace/list_sinv.txt").readlines()
	# file = open("/home/frappe/frappe-bench/apps/sync_tax/sync_tax/sync_tax/patch/sync_list.txt").readlines()
	list_doc = [frappe._dict({"name":row.strip()}) for row in file]

	for doc in list_doc:
		frappe.get_doc("Payment Entry",doc.name).cancel()

@frappe.whitelist()
def repair_gl_entry(doctype,docname):
	# account_editor = frappe.db.get_single_value("Accounts Settings","frozen_accounts_modifier")
	# frappe.db.set_value("Singles","Accounts Settings","frozen_accounts_modifier","")
	# frappe.db.commit()

	# frappe.db.set_value("Stock Settings","Stock Settings", "allow_negative_stock", 1)
	docu = frappe.get_doc(doctype, docname)
	# print(docu.sync_sumber_name)
	# delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(docname))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))

	# docu.update_stock_ledger()
	docu.make_gl_entries()
	# print("Membenarkan LEDGER dari {} - DONE ".format(docname))
	frappe.db.commit()
	# frappe.db.set_value("Accounts Settings","frozen_accounts_modifier",account_editor)
	# frappe.db.set_value("Stock Settings", "Stock Settings","allow_negative_stock", 0)