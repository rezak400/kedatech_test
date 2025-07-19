# -*- coding: utf-8 -*-

import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError
from psycopg2 import IntegrityError

_logger = logging.getLogger(__name__)



class MaterialController(http.Controller):

    @http.route('/api/materials', type='http', auth='public', methods=['GET'], csrf=False)
    def get_materials(self, material_type=None, **kwargs):
        """Get all materials with optional filtering by material_type via query parameters"""
        try:
            domain = []
            
            # Filter by material type if provided via query parameter
            if material_type:
                domain.append(('material_type', '=', material_type))
            
            materials = request.env['material.material'].sudo().search(domain)
            
            result = []
            for material in materials:
                result.append({
                    'id': material.id,
                    'material_code': material.material_code,
                    'material_name': material.material_name,
                    'material_type': material.material_type,
                    'material_buy_price': material.material_buy_price,
                    'supplier_id': material.supplier_id.id,
                    'supplier_name': material.supplier_id.name,
                })
            
            response_data = {
                'success': True,
                'data': result,
                'count': len(result)
            }
            
            return request.make_response(
                json.dumps(response_data),
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            _logger.error("Error getting materials: %s", str(e))
            response_data = {
                'success': False,
                'error': str(e)
            }
            return request.make_response(
                json.dumps(response_data),
                status=500,
                headers={'Content-Type': 'application/json'}
            )

    @http.route('/api/materials/<int:material_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_material(self, material_id, **kwargs):
        """Get a specific material by ID"""
        try:
            material = request.env['material.material'].sudo().browse(material_id)
            if not material.exists():
                response_data = {
                    'success': False,
                    'error': 'Material not found'
                }
                return request.make_response(
                    json.dumps(response_data),
                    status=404,
                    headers={'Content-Type': 'application/json'}
                )
            
            result = {
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier_id': material.supplier_id.id,
                'supplier_name': material.supplier_id.name,
            }
            
            response_data = {
                'success': True,
                'data': result
            }
            
            return request.make_response(
                json.dumps(response_data),
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            _logger.error("Error getting material %s: %s", material_id, str(e))
            response_data = {
                'success': False,
                'error': str(e)
            }
            return request.make_response(
                json.dumps(response_data),
                status=500,
                headers={'Content-Type': 'application/json'}
            )

    @http.route('/api/materials', type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        """Create a new material"""
        try:
            # Get JSON data from request - handle both params and direct format
            raw_data = request.jsonrequest
            data = raw_data.get('params', raw_data) if 'params' in raw_data else raw_data
            
            # Validate required fields
            required_fields = ['material_code', 'material_name', 'material_type', 'material_buy_price', 'supplier_id']
            for field in required_fields:
                if field not in data:
                    return {
                        'success': False,
                        'error': f'Missing required field: {field}',
                        'error_code': 400
                    }
            
            # Create material
            material = request.env['material.material'].sudo().create(data)
            
            result = {
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier_id': material.supplier_id.id,
                'supplier_name': material.supplier_id.name,
            }
            
            return {
                'success': True,
                'message': 'Material created successfully',
                'data': result
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': 400
            }
        except IntegrityError as e:
            error_msg = str(e)
            # Convert PostgreSQL constraint violations to user-friendly messages
            if 'material_buy_price_positive' in error_msg:
                user_friendly_msg = "Material buy price must be at least 100. Please enter a valid price (≥ 100)."
            elif 'material_code_unique' in error_msg:
                user_friendly_msg = "Material code already exists. Please use a unique material code."
            else:
                user_friendly_msg = "Data integrity constraint violation. Please check your input values."
            
            _logger.warning("Integrity constraint violation: %s", error_msg)
            return {
                'success': False,
                'error': user_friendly_msg,
                'error_code': 400
            }
        except Exception as e:
            _logger.error("Error creating material: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'error_code': 500
            }

    @http.route('/api/materials/<int:material_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        """Update an existing material"""
        try:
            material = request.env['material.material'].sudo().browse(material_id)
            if not material.exists():
                return {
                    'success': False,
                    'error': 'Material not found',
                    'error_code': 404
                }
            
            # Get JSON data from request - handle both params and direct format
            raw_data = request.jsonrequest
            data = raw_data.get('params', raw_data) if 'params' in raw_data else raw_data
            
            # Update material
            material.write(data)
            
            result = {
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier_id': material.supplier_id.id,
                'supplier_name': material.supplier_id.name,
            }
            
            return {
                'success': True,
                'message': 'Material updated successfully',
                'data': result
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': 400
            }
        except IntegrityError as e:
            error_msg = str(e)
            # Convert PostgreSQL constraint violations to user-friendly messages
            if 'material_buy_price_positive' in error_msg:
                user_friendly_msg = "Material buy price must be at least 100. Please enter a valid price (≥ 100)."
            elif 'material_code_unique' in error_msg:
                user_friendly_msg = "Material code already exists. Please use a unique material code."
            else:
                user_friendly_msg = "Data integrity constraint violation. Please check your input values."
            
            _logger.warning("Integrity constraint violation: %s", error_msg)
            return {
                'success': False,
                'error': user_friendly_msg,
                'error_code': 400
            }
        except Exception as e:
            _logger.error("Error updating material %s: %s", material_id, str(e))
            return {
                'success': False,
                'error': str(e),
                'error_code': 500
            }

    @http.route('/api/materials/<int:material_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        """Delete a material"""
        try:
            material = request.env['material.material'].sudo().browse(material_id)
            if not material.exists():
                return {
                    'success': False,
                    'error': 'Material not found',
                    'error_code': 404
                }
            
            material.unlink()
            
            return {
                'success': True,
                'message': 'Material deleted successfully'
            }
            
        except Exception as e:
            _logger.error("Error deleting material %s: %s", material_id, str(e))
            return {
                'success': False,
                'error': str(e),
                'error_code': 500
            }

    @http.route('/api/suppliers', type='http', auth='public', methods=['GET'], csrf=False)
    def get_suppliers(self, **kwargs):
        """Get all suppliers"""
        try:
            suppliers = request.env['material.supplier'].sudo().search([])
            
            result = []
            for supplier in suppliers:
                result.append({
                    'id': supplier.id,
                    'name': supplier.name,
                    'email': supplier.email,
                    'phone': supplier.phone,
                    'address': supplier.address,
                })
            
            response_data = {
                'success': True,
                'data': result,
                'count': len(result)
            }
            
            return request.make_response(
                json.dumps(response_data),
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            _logger.error("Error getting suppliers: %s", str(e))
            response_data = {
                'success': False,
                'error': str(e)
            }
            return request.make_response(
                json.dumps(response_data),
                status=500,
                headers={'Content-Type': 'application/json'}
            )

    @http.route('/api/suppliers', type='json', auth='public', methods=['POST'], csrf=False)
    def create_supplier(self, **kwargs):
        """Create a new supplier"""
        try:
            # Get JSON data from request - handle both params and direct format
            raw_data = request.jsonrequest
            data = raw_data.get('params', raw_data) if 'params' in raw_data else raw_data
            
            # Validate required fields
            if 'name' not in data:
                return {
                    'success': False,
                    'error': 'Missing required field: name',
                    'error_code': 400
                }
            
            # Create supplier
            supplier = request.env['material.supplier'].sudo().create(data)
            
            result = {
                'id': supplier.id,
                'name': supplier.name,
                'email': supplier.email,
                'phone': supplier.phone,
                'address': supplier.address,
            }
            
            return {
                'success': True,
                'message': 'Supplier created successfully',
                'data': result
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': 400
            }
        except IntegrityError as e:
            error_msg = str(e)
            # Convert PostgreSQL constraint violations to user-friendly messages
            if 'supplier_name_unique' in error_msg:
                user_friendly_msg = "Supplier name already exists. Please use a unique supplier name."
            else:
                user_friendly_msg = "Data integrity constraint violation. Please check your input values."
            
            _logger.warning("Integrity constraint violation: %s", error_msg)
            return {
                'success': False,
                'error': user_friendly_msg,
                'error_code': 400
            }
        except Exception as e:
            _logger.error("Error creating supplier: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'error_code': 500
            } 