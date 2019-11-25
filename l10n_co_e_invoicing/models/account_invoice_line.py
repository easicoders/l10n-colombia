# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@joanmarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def _get_invoice_lines_taxes(self, tax, invoice_line_taxes_total):
        tax_code = tax.tax_group_id.tax_group_type_id.code
        tax_name = tax.tax_group_id.tax_group_type_id.name
        tax_percent = '{:.2f}'.format(tax.amount or 0)

        if tax_code not in invoice_line_taxes_total:
            invoice_line_taxes_total[tax_code] = {}
            invoice_line_taxes_total[tax_code]['total'] = 0
            invoice_line_taxes_total[tax_code]['name'] = tax_name
            invoice_line_taxes_total[tax_code]['taxes'] = {}

        if tax_percent not in invoice_line_taxes_total[tax_code]['taxes']:
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent] = {}
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['base'] = 0
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['amount'] = 0

        invoice_line_taxes_total[tax_code]['total'] += (
            self.price_subtotal * tax.amount / 100)
        invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['base'] += (
            self.price_subtotal)
        invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['amount'] += (
            self.price_subtotal * tax.amount / 100)

        return invoice_line_taxes_total