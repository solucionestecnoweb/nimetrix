# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product/Material Internal Requisitions by Employees/Users',
    'version': '2.3.1',
    'price': 99.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """This module allow your employees/users to create Internal Requisitions.""",
    'description': """
    Material Internal Requisitions
    This module allowed internal requisition of employee.
​Internal_Requisition_Via_iProcurement
Internal Requisitions
Internal Requisition
iProcurement
Inter-Organization Shipping Network
Online Requisitions
Issue Enforcement
Inventory Replenishment Requisitions
Replenishment Requisitions
MRP Generated Requisitions
generated Requisitions
Internal Sales Orders
Complete Requisitions Status Visibility
Using Internal Requisitions
purchase requisitions
replenishment requisitions
employee Requisition
employee Internal Requisition
user Requisition
stock Requisition
inventory Requisition
warehouse Requisition
factory Requisition
department Requisition
manager Requisition
Submit requisition
Create Internal Orders
Internal Orders
product Requisition
item Requisition
material Requisition
product Requisitions
item Requisitions
material Requisitions
products Requisitions
Internal Requisition Process
Approving or Denying the Internal Requisition
Denying Internal Requisition​
construction management
real estate management
construction app

    """,
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'http://www.probuse.com',
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpg'],
    # 'live_test_url': 'https://youtu.be/giqUttgLE9E',
    'live_test_url': 'https://youtu.be/Z4UzyTYiVvM',
    'category': 'Warehouse',
    'depends': [
                'stock',
                'hr',
                'analytic'
                ],
    'data':[
        'security/ir.model.access.csv',
        'security/multi_company_security.xml',
        'security/requisition_security.xml',
        'data/requisition_sequence.xml',
        'data/employee_approval_template.xml',
        'data/confirm_template.xml',
        'report/requisition_report.xml',
        'views/requisition_view.xml',
        'views/hr_employee_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
