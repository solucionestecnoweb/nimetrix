# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta
import base64
from io import StringIO
from odoo import api, fields, models
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning

class ReporteCategoria(models.TransientModel):
	_name = "stock.move.report.categoria"

	date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
	date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))
	category_id = fields.Many2one(comodel_name='product.category', string='Categoria')
	product = fields.Many2many(comodel_name='product.product', string='product')
	
	company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id.id)
	date_report = fields.Date(string='day', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))

	libro  = fields.Many2many(comodel_name='libro.inventario.categoria', string='Libro')
	
	def datos(self):
		temp_libro = self.env['libro.inventario.categoria'].search([])
		temp_line = self.env['libro.inventario'].search([])

		categoria =[]

		categoria.append(self.category_id)

		temp = self.env['product.category'].search([
			('parent_id','=',self.category_id.id)
		])

		for l in temp:
			categoria.append(l)

		for t in temp_libro:
			t.unlink()

		for t in temp_line:
    			t.unlink()

		
		for cat in categoria:
				
			cabezera = self.env['libro.inventario.categoria'].create({
				'name':cat.id,
			})

			self.product =  self.env['product.product'].search([
				('categ_id','=',cat.id),
				('type','=','product')
			])
			kardex = self.env['make.kardex.product'].create({
				'fini':self.date_from,
				'ffin':self.date_to,
			})
			for item in self.product:
				libro = self.env['libro.inventario'].create({ 
					'name': item.id,
					'libro':cabezera.id ,
					})
				libro.libro = cabezera.id
				linea = kardex.do_csvtoexcel_commercial_libro(item.id)
				inicial =  False
				
				saldo = 0
				saldo_total = 0
				last_price = 0

				for line in linea:
					saldo = saldo + line[10] - line[11]
					if inicial:
						libro.cantidad_inicial = line[10] if  line[10] > 0 else line[11]
					else :
						if line[10] > 0:
							if line[10] :
								libro.cantidad_entradas += line[10] if  line[10] > 0  else 0
							if line[12] :
								libro.costo_entradas += line[12] if line[12] > 0  else 0 
							if line[11] and  line[12]:	
								libro.total_bolivares_entradas += line[10] *  line[12]
						else :
							if line[11] :
								libro.cantidad_salidas += line[11]   if line[11] > 0  else 0
							if line[12] :
								libro.costo_salidas += line[12] if line[12] != None  else 0
							if line[11] and  line[12]:
								libro.total_bolivares_salida += line[11] *  line[12]


					ing = round((line[12] if line[12] and line[12]>0 else last_price) * line[10],2) if line[10] else 0
					sal = round(last_price * line[11],2) if line[11] else 0
					if line[13] == 1 or line[13] == None: #Stock pickin type == 1 == Ingreso
						saldo_total = saldo_total + ing - sal
						if line[14] and line[15] == False or line[14] and line[15] == True and x > 7:
							last_price = last_price
						else:
							last_price = saldo_total / saldo if saldo_total else 0
					else:
						saldo_total = saldo_total + ing - sal
					
				libro.total = saldo
				libro.promedio = last_price 
				libro.total_bolivares = saldo_total

		self.libro =  self.env['libro.inventario.categoria'].search([])

				
	def print_facturas(self):
		self.datos()
		return self.env.ref('libro_inventario.movimientos_categoria_libro').report_action(self)

class LibroVentasModelo(models.Model):
	_name = "libro.inventario.categoria" 
	
	name = fields.Many2one(comodel_name='product.category', string='Categoria')
	line_id = fields.One2many(comodel_name='libro.inventario', inverse_name='libro', string='Linea')
	

class LibroVentasModelo(models.Model):
	_name = "libro.inventario" 

	libro = fields.Many2one(comodel_name='libro.inventario.categoria', string='Categoria')
	
	name  = fields.Many2one(comodel_name='product.product', string='Producto')

	cantidad_inicial = fields.Float(string='Cantidad Incial')
	costo_intradas    = fields.Float(string='Costo de Inicial')
	total_bolivares_inicial   = fields.Float(string='Total Bolivares Inicial')

	category_id = fields.Many2one(comodel_name='product.category', string='Categoria')

	cantidad_entradas = fields.Float(string='Cantidad Entradas')
	costo_entradas    = fields.Float(string='Costo de Entradas')
	total_bolivares_entradas   = fields.Float(string='Total Bolivares ')

	cantidad_salidas  = fields.Float(string='Cantidad Salidas')
	costo_salidas     = fields.Float(string='Costo de Salidas')
	total_bolivares_salida     = fields.Float(string='Total Bolivares')

	total  = fields.Float(string='Total')
	promedio     = fields.Float(string='Promedio')
	total_bolivares     = fields.Float(string='Total Bolivares')
	
	
	
	

	

	
