# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'

    kardex_price_unit = fields.Float(string='Kardex Price Unit', default=0) # digits=(total, decimal)

    def _create_in_svl(self, forced_quantity=None):
        res = super(StockMove, self)._create_in_svl()
        for valuation in res:
            # Si existen ajustes de inventario inicial
            if valuation.stock_move_id.inventory_id:
                for line in valuation.stock_move_id.inventory_id.line_ids:
                    if line.product_id == valuation.product_id and line.location_id == valuation.stock_move_id.location_dest_id and line.is_initial:
                        valuation.update({
                            'unit_cost': line.initial_cost,
                            'value': line.initial_cost * valuation.quantity,
                            'remaining_value': line.initial_cost * valuation.quantity
                            })
                        line.product_id.standard_price = line.initial_cost
            else:
                if valuation.stock_move_id.purchase_line_id:
                    price_unit = valuation.stock_move_id.purchase_line_id.price_unit
                else:
                    if valuation.stock_move_id.origin_returned_move_id:
                        vl = self.env['stock.valuation.layer'].search([('stock_move_id','=', valuation.stock_move_id.origin_returned_move_id.id),('product_id','=',valuation.stock_move_id.product_id.id)])
                        price_unit = vl.unit_cost
                    else:
                        # TODO pensar como hacer para mover productos de una almacen a otro
                        # que pueden tener costo valorizados distintos
                        price_unit = valuation.stock_move_id.product_id.standard_price
                if valuation.stock_move_id.purchase_line_id.currency_id and valuation.stock_move_id.purchase_line_id.currency_id != self.env.user.company_id.currency_id:
                    rate = valuation.currency_id._get_conversion_rate(valuation.stock_move_id.purchase_line_id.currency_id, self.env.user.company_id.currency_id, self.env.user.company_id, valuation.stock_move_id.picking_id.kardex_date if valuation.stock_move_id.picking_id.use_kardex_date else valuation.stock_move_id.picking_id.scheduled_date)
                    if valuation.stock_move_id.picking_id.invoice_id: # or valuation.stock_move_id.picking_id.invoice_id_purchase:
                        # if valuation.stock_move_id.picking_id.invoice_id:
                        if valuation.stock_move_id.picking_id.invoice_id.tc_per:
                            price_unit = price_unit * valuation.stock_move_id.picking_id.invoice_id.currency_rate
                        else:
                            price_unit = price_unit * rate
                    else:
                        price_unit = price_unit * rate
                valuation.update({
                    'unit_cost': price_unit,
                    'value': price_unit * valuation.quantity,
                    'remaining_value': price_unit * valuation.quantity  
                })
        return res