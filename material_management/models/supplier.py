# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Supplier(models.Model):
    _name = 'material.supplier'
    _description = 'Material Supplier'
    _order = 'name'

    name = fields.Char(
        string='Supplier Name', 
        required=True, 
        help="Name of the supplier"
    )
    email = fields.Char(
        string='Email',
        help="Supplier email address"
    )
    phone = fields.Char(
        string='Phone',
        help="Supplier phone number"
    )
    address = fields.Text(
        string='Address',
        help="Supplier address"
    )

    # Add SQL constraint for unique name
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Supplier name already exists. Please use a unique supplier name.')
    ]

    @api.constrains('name')
    def _check_supplier_name(self):
        """Validate supplier name is not empty"""
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("Supplier name is required. Please provide a supplier name.")

    def name_get(self):
        """Override name_get to provide better display names"""
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result 