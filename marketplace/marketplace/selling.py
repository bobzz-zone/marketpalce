# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from datetime import date
import datetime
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from frappe.utils import cint, flt, getdate, add_days, cstr, nowdate, get_link_to_form, formatdate
from erpnext.accounts.utils import get_account_currency

# ACC-SINV-2021-00017-8
def custom_get_gl_entries(self, warehouse_account=None):
	frappe.msgprint("Masuk custom_get_gl_entries")
	from erpnext.accounts.general_ledger import merge_similar_entries

	gl_entries = []

	make_customer_gl_entry_custom(self, gl_entries)
	# make_disc_gl_entry_custom(self, gl_entries)
	# make_disc_gl_entry_lawan_custom(self, gl_entries)

	self.make_tax_gl_entries(gl_entries)
	self.make_internal_transfer_gl_entries(gl_entries)

	self.make_item_gl_entries(gl_entries)

	# merge gl entries before adding pos entries
	gl_entries = merge_similar_entries(gl_entries)

	self.make_loyalty_point_redemption_gle(gl_entries)
	self.make_pos_gl_entries(gl_entries)
	self.make_gle_for_change_amount(gl_entries)

	self.make_write_off_gl_entry(gl_entries)
	self.make_gle_for_rounding_adjustment(gl_entries)

	return gl_entries

def make_customer_gl_entry_custom(self, gl_entries):
		# Checked both rounding_adjustment and rounded_total
		# because rounded_total had value even before introcution of posting GLE based on rounded total
		frappe.msgprint(self.cost_center)
		grand_total = self.rounded_total if (self.rounding_adjustment and self.rounded_total) else self.grand_total
		if grand_total and not self.is_internal_transfer():
			# Didnot use base_grand_total to book rounding loss gle
			grand_total_in_company_currency = flt(grand_total * self.conversion_rate,
				self.precision("grand_total"))

			gl_entries.append(
				self.get_gl_dict({
					"account": self.debit_to,
					"party_type": "Customer",
					"party": self.customer,
					"due_date": self.due_date,
					"against": self.against_income_account,
					"debit": grand_total_in_company_currency,
					"debit_in_account_currency": grand_total_in_company_currency \
						if self.party_account_currency==self.company_currency else grand_total,
					"against_voucher": self.return_against if cint(self.is_return) and self.return_against else self.name,
					"against_voucher_type": self.doctype,
					"cost_center": self.cost_center,
					"project": self.project,
					# "remarks": "coba Lutfi xxxx!"
				}, self.party_account_currency, item=self)
			)


def make_disc_gl_entry_custom(self, gl_entries):
	# diskon_account = frappe.db.get_single_value('Setting Account', 'diskon_account')
	diskon_account = frappe.get_value("Account Company List",{"name" : self.company}, "diskon_account")

	gl_entries.append(
		self.get_gl_dict({
			"account": diskon_account,
			"party_type": "Customer",
			"party": self.customer,
			"due_date": self.due_date,
			"against": self.against_income_account,
			"debit": self.discount_amount,
			"debit_in_account_currency": self.discount_amount,
			"against_voucher": self.return_against if cint(self.is_return) and self.return_against else self.name,
			"against_voucher_type": self.doctype,
			"cost_center": self.cost_center,
			"project": self.project
			# "remarks": "coba Lutfi yyyyy!"
		}, self.party_account_currency, item=self)
	)

def make_disc_gl_entry_lawan_custom(self, gl_entries):
	# income_account = frappe.db.get_single_value('Setting Account', 'income_account')
	income_account = frappe.get_value("Account Company List",{"name" : self.company}, "income_account")
	
	gl_entries.append(
		self.get_gl_dict({
			"account": income_account,
			"party_type": "Customer",
			"party": self.customer,
			"due_date": self.due_date,
			"against": self.against_income_account,
			"credit": self.discount_amount,
			"credit_in_account_currency": self.discount_amount,
			"against_voucher": self.return_against if cint(self.is_return) and self.return_against else self.name,
			"against_voucher_type": self.doctype,
			"cost_center": self.cost_center,
			"project": self.project
			# "remarks": "coba Lutfi zzz!"
		}, self.party_account_currency, item=self)
	)


@frappe.whitelist()
def overide_make_gl(self,method):
	# frappe.msgprint('coba')
	SalesInvoice.get_gl_entries = custom_get_gl_entries


