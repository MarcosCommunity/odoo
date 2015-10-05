# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2015 Marcos Organizador de Negocios SRL http://marcos.do
#    Write by Eneldo Serrata (eneldo@marcos.do)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, orm, fields
import openerp.addons.decimal_precision as dp

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = ['sale.order']

    def _discount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            tot_disc = 0.0
            for line in order.order_line:
                tot_disc += line.disc_line
            res[order.id] = tot_disc
        return res

    def _total_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            tot_all = 0.0
            for line in order.order_line:
                tot_all += line.total_line
            res[order.id] = tot_all
        return res

    _columns = {
        'disc_total': fields.function(_discount_all, string='Descuento', type="float", digits_compute= dp.get_precision('Account'), store=True),
        'total_b4_disc':fields.function(_total_all, string='Sin descuento', type="float", digits_compute= dp.get_precision('Account'), store=True),
    }



class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = ['sale.order.line']

    def _discount_line (self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            discount = line.price_unit * ((line.discount or 0.0)/100.0) * line.product_uom_qty
            res[line.id] = discount
        return res

    def _total_line(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
           total = line.price_unit * line.product_uom_qty
           res[line.id] = total
        return res

    _columns = {
        'disc_line': fields.function(_discount_line, string='Desc', type="float", digits_compute= dp.get_precision('Account'), store=True),
        'total_line':fields.function(_total_line, string='Total', type="float", digits_compute= dp.get_precision('Account'), store=True),
    }