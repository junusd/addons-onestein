# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        """Override, button Validate on invoices."""
        res = super(AccountInvoice, self).action_move_create()
        for rec in self:
            rec.invoice_line_ids.compute_spread_board()
        return res

    @api.multi
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for line in res:
            invl_id = line.get('invl_id')
            invl = self.env['account.invoice.line'].browse(invl_id)
            if invl.spread_account_id:
                line['account_id'] = invl.spread_account_id.id
        return res
