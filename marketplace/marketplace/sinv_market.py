# Copyright (c) 2021, Marketplace and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date
import time
import datetime
from frappe.utils import flt, rounded, add_months,add_days, nowdate, getdate

@frappe.whitelist()
def gen_invoice(tanggal,com):
	try:
		data =frappe.db.get_list('Marketplace Invoice',filters={'sinv': '','date': tanggal,'company': com},fields=['*'],group_by = 'customer')
		# income_account = frappe.db.get_single_value('Setting Account', 'income_account')
		# cost_center = frappe.db.get_single_value('Setting Account', 'cost_center')
		# account_head = frappe.db.get_single_value('Setting Account', 'account_head')
		# description = frappe.db.get_single_value('Setting Account', 'description')
		income_account = frappe.get_value("Account Company List",{"name" : com}, "income_account")
		cost_center = frappe.get_value("Account Company List",{"name" : com}, "cost_center")
		# frappe.msgprint(cost_center)
		account_head = frappe.get_value("Account Company List",{"name" : com}, "account_head")
		description = frappe.get_value("Account Company List",{"name" : com}, "description")
		description_disc = frappe.get_value("Account Company List",{"name" : com}, "description_disc")
		diskon_account = frappe.get_value("Account Company List",{"name" : com}, "diskon_account")
		ns = ''
		if com == 'BB ONLINE':
			# frappe.msgprint('BB')
			ns = 'SINV-BBO.YY.MM.#####'
		if com == 'BM ONLINE':
			# frappe.msgprint('BM')
			ns = 'SINV-BMO.YY.MM.#####'

		if data:
			minv = []
			item = []
			qty = []
			total = []
			minv2=[]
			
			for i in data:
				# frappe.msgprint(i['name'])
				coba2 =frappe.db.get_list('Marketplace Invoice',filters={'customer': i['customer'],'date': tanggal,'company': com},fields=['*'])
				disc = []
				ongkir = []
				for c2 in coba2:
					minv2.append(c2['name'])
					disc.append(c2['total_diskon'])
					ongkir.append(c2['ongkir'])

				# frappe.msgprint(str(minv2))
				sum_disc = sum(disc)
				sum_ongkir = sum(ongkir)
				# frappe.msgprint(str(sum_disc))
				today = date.today()
				doc = frappe.new_doc('Sales Invoice')
				doc.set_posting_time = 1
				doc.posting_date = tanggal
				doc.naming_series = ns
				doc.company = com
				doc.customer = i['customer']
				doc.due_date = tanggal
				doc.tmp = str(minv2)
				doc.ignore_pricing_rule = 1
				doc.update_stock = 1
				# data_i =frappe.db.get_list('Marketplace Invoice',filters={'invoice_id': ''},fields=['*'])
				# for j in data_i:
				# 	minv.append(j['name'])

				coba = frappe.db.get_list('Marketplace Order',filters={'parent': ["in",minv2]},fields=['*'],group_by = 'item_code')
				for c in coba:
					row = doc.append('items', {})
					row.item_code = c['item_code']
					hitung = frappe.db.get_list('Marketplace Order',filters={'parent': ["in",minv2],'item_code': c['item_code']},fields=['*'])
					for h in hitung:
						qty.append(h['qty'])
						total.append(h['total'])
					
					# frappe.msgprint(str(qty))
					# frappe.msgprint(str(total))
					sum_qty = sum(qty)
					sum_total = sum(total)
					rate = sum_total/sum_qty
					row.qty = sum_qty
					row.price_list_rate = rate
					row.cost_center = cost_center
					# row.rate = rate
					qty = []
					total = []
					row.income_account = income_account
				doc.cost_center = cost_center
				# doc.apply_discount_on = 'Net Total'
				# doc.discount_amount = sum_disc
				rowt = doc.append('taxes', {})
				rowt.charge_type = 'Actual'
				rowt.account_head = account_head
				rowt.cost_center = cost_center
				rowt.description = description
				rowt.tax_amount = sum_ongkir
				# diskon
				rowt2 = doc.append('taxes', {})
				rowt2.charge_type = 'Actual'
				rowt2.account_head = diskon_account
				rowt2.cost_center = cost_center
				rowt2.description = description_disc
				rowt2.tax_amount = 0 - sum_disc
				# doc.docstatus = 1
				doc.flags.ignore_permission=True
				doc.save()
				doc.submit()

				coba3 = frappe.db.get_list('Marketplace Invoice',filters={'name': ["in",minv2]},fields=['*'])
				for c3 in coba3:
					doc2 = frappe.get_doc("Marketplace Invoice",c3['name'])
					tmp2 = frappe.get_value("Sales Invoice",{"tmp": str(minv2)}, "name")
					doc2.sinv = tmp2
					# doc2.docstatus = 1
					# doc2.db_update()
					# frappe.db.commit()
					doc2.flags.ignore_permission=True
					doc2.save()
				minv2=[]
				frappe.msgprint("Generate SINV Berhasil !")
		else:
			frappe.msgprint("Tidak ada data")
	except Exception as e:
		# frappe.msgprint(e)
		frappe.throw("Generate SINV Gagal !")

@frappe.whitelist()
def cancel_minv(doc,method):
	punctuations = '''!()[]{};:'"<>./?@#$%^&*_~'''
	no_punct = ""
	if doc.tmp:
		cek = doc.tmp
		for i in cek:
			if i not in punctuations:
				no_punct = no_punct + i
		x = no_punct.split(", ")
		# frappe.throw(str(x))
		for s in x:
			#frappe.msgprint(s)
			doci = frappe.get_doc("Marketplace Invoice",s)
			doci.sinv = ""
			doci.db_update()
			frappe.db.commit()

