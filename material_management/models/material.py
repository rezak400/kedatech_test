# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = 'material.material'
    _description = 'Material'
    _order = 'material_code'
    _rec_name = 'material_name'

    # Required fields per requirement
    material_code = fields.Char(
        string='Material Code',
        required=True,
        help="Unique code for the material"
    )
    material_name = fields.Char(
        string='Material Name',
        required=True,
        help="Name of the material"
    )
    material_type = fields.Selection(
        [
            ('fabric', 'Fabric'),
            ('jeans', 'Jeans'),
            ('cotton', 'Cotton'),
        ],
        string='Material Type',
        required=True,
        help="Type of material"
    )
    material_buy_price = fields.Float(
        string='Material Buy Price',
        required=True,
        help="Purchase price of the material (minimum 100)"
    )
    supplier_id = fields.Many2one(
        'material.supplier',
        string='Supplier',
        required=True,
        help="Related supplier for this material"
    )

    # SQL constraints
    _sql_constraints = [
        ('material_code_unique', 'UNIQUE(material_code)', 'Material code already exists. Please use a unique material code.'),
        ('material_buy_price_positive', 'CHECK(material_buy_price >= 100)', 'Material buy price must be at least 100. Please enter a valid price (≥ 100).')
    ]

    @api.constrains('material_buy_price')
    def _check_material_buy_price(self):
        """Validate that material buy price is not less than 100"""
        for record in self:
            if record.material_buy_price < 100:
                raise ValidationError("Material buy price must be at least 100. Please enter a valid price (≥ 100).")

    @api.constrains('material_code')
    def _check_material_code(self):
        """Validate material code is not empty and has minimum length"""
        for record in self:
            if not record.material_code or len(record.material_code.strip()) < 2:
                raise ValidationError("Material code must be at least 2 characters long. Please provide a valid material code.")

    @api.constrains('material_type')
    def _check_material_type(self):
        """Validate material type is one of the allowed values"""
        valid_types = ['fabric', 'jeans', 'cotton']
        for record in self:
            if record.material_type not in valid_types:
                raise ValidationError(f"Invalid material type '{record.material_type}'. Please select from: fabric, jeans, or cotton.")

    @api.constrains('supplier_id')
    def _check_supplier_id(self):
        """Validate supplier exists"""
        for record in self:
            if not record.supplier_id or not record.supplier_id.exists():
                raise ValidationError("Invalid supplier selected. Please choose a valid supplier.")

    def name_get(self):
        """Override name_get to show material code and name"""
        result = []
        for record in self:
            name = '[%s] %s' % (record.material_code, record.material_name)
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Override name_search to search by code and name"""
        args = args or []
        if name:
            domain = ['|', ('material_code', operator, name), ('material_name', operator, name)]
            records = self.search(domain + args, limit=limit)
            return records.name_get()
        return super(Material, self).name_search(name, args, operator, limit) 