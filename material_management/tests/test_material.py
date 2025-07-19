# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMaterial(TransactionCase):

    def setUp(self):
        super(TestMaterial, self).setUp()
        
        # Create test supplier
        self.supplier = self.env['material.supplier'].create({
            'name': 'Test Supplier',
            'email': 'test@supplier.com',
            'phone': '123456789',
            'address': 'Test Address'
        })

    def test_create_material_success(self):
        """Test successful material creation"""
        material = self.env['material.material'].create({
            'material_code': 'MAT001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'material_buy_price': 150.0,
            'supplier_id': self.supplier.id
        })
        
        self.assertTrue(material.id)
        self.assertEqual(material.material_code, 'MAT001')
        self.assertEqual(material.material_name, 'Test Material')
        self.assertEqual(material.material_type, 'fabric')
        self.assertEqual(material.material_buy_price, 150.0)
        self.assertEqual(material.supplier_id.id, self.supplier.id)

    def test_material_price_constraint(self):
        """Test material buy price constraint (minimum 100)"""
        import time
        unique_code = f'PRICE{str(int(time.time() * 1000))[-6:]}'
        
        from psycopg2.errors import CheckViolation
        with self.assertRaises(CheckViolation):
            with self.env.cr.savepoint():
                self.env['material.material'].create({
                    'material_code': unique_code,
                    'material_name': 'Test Material 2',
                    'material_type': 'jeans',
                    'material_buy_price': 50.0,  # Less than 100
                    'supplier_id': self.supplier.id
                })

    def test_material_code_unique_constraint(self):
        """Test material code uniqueness"""
        import time
        unique_code = f'MAT{str(int(time.time() * 1000))[-6:]}'
        
        # Create first material
        self.env['material.material'].create({
            'material_code': unique_code,
            'material_name': 'Test Material 3',
            'material_type': 'cotton',
            'material_buy_price': 120.0,
            'supplier_id': self.supplier.id
        })
        
        # Try to create second material with same code
        from psycopg2.errors import UniqueViolation
        with self.assertRaises(UniqueViolation):
            with self.env.cr.savepoint():
                self.env['material.material'].create({
                    'material_code': unique_code,  # Duplicate code
                    'material_name': 'Test Material 4',
                    'material_type': 'fabric',
                'material_buy_price': 130.0,
                'supplier_id': self.supplier.id
            })

    def test_material_code_validation(self):
        """Test material code validation (minimum 2 characters)"""
        with self.assertRaises(ValidationError):
            self.env['material.material'].create({
                'material_code': 'M',  # Too short
                'material_name': 'Test Material 5',
                'material_type': 'fabric',
                'material_buy_price': 110.0,
                'supplier_id': self.supplier.id
            })

    def test_required_fields(self):
        """Test that all required fields are enforced"""
        from psycopg2.errors import NotNullViolation
        import time
        
        # Test missing material_code with transaction handling
        with self.assertRaises(NotNullViolation):
            with self.env.cr.savepoint():
                self.env['material.material'].create({
                    'material_name': 'Test Material 6',
                    'material_type': 'fabric',
                    'material_buy_price': 110.0,
                    'supplier_id': self.supplier.id
                })
        
        # Test missing material_name with transaction handling
        with self.assertRaises(NotNullViolation):
            with self.env.cr.savepoint():
                unique_code = f'REQ{str(int(time.time() * 1000))[-6:]}'
                self.env['material.material'].create({
                    'material_code': unique_code,
                    'material_type': 'fabric',
                    'material_buy_price': 110.0,
                    'supplier_id': self.supplier.id
                })
        
        # Test missing material_type with transaction handling
        with self.assertRaises(NotNullViolation):
            with self.env.cr.savepoint():
                unique_code2 = f'REQ2{str(int(time.time() * 1000))[-6:]}'
                self.env['material.material'].create({
                    'material_code': unique_code2,
                    'material_name': 'Test Material 7',
                    'material_buy_price': 110.0,
                    'supplier_id': self.supplier.id
                })

    def test_material_update(self):
        """Test material update functionality"""
        material = self.env['material.material'].create({
            'material_code': 'MAT008',
            'material_name': 'Test Material 8',
            'material_type': 'fabric',
            'material_buy_price': 150.0,
            'supplier_id': self.supplier.id
        })
        
        # Update material
        material.write({
            'material_name': 'Updated Material Name',
            'material_buy_price': 200.0
        })
        
        self.assertEqual(material.material_name, 'Updated Material Name')
        self.assertEqual(material.material_buy_price, 200.0)

    def test_material_delete(self):
        """Test material deletion"""
        material = self.env['material.material'].create({
            'material_code': 'MAT009',
            'material_name': 'Test Material 9',
            'material_type': 'cotton',
            'material_buy_price': 140.0,
            'supplier_id': self.supplier.id
        })
        
        material_id = material.id
        material.unlink()
        
        # Verify material is deleted
        deleted_material = self.env['material.material'].browse(material_id)
        self.assertFalse(deleted_material.exists())

    def test_material_name_get(self):
        """Test material name_get method"""
        material = self.env['material.material'].create({
            'material_code': 'MAT010',
            'material_name': 'Test Material 10',
            'material_type': 'fabric',
            'material_buy_price': 160.0,
            'supplier_id': self.supplier.id
        })
        
        name_get_result = material.name_get()
        expected_name = '[MAT010] Test Material 10'
        self.assertEqual(name_get_result[0][1], expected_name)

    def test_material_filtering_by_type(self):
        """Test filtering materials by type"""
        # Create materials of different types with unique codes
        import time
        unique_suffix = str(int(time.time() * 1000))[-6:]  # Get unique suffix
        
        fabric_material = self.env['material.material'].create({
            'material_code': f'FAB{unique_suffix}',
            'material_name': 'Fabric Material',
            'material_type': 'fabric',
            'material_buy_price': 120.0,
            'supplier_id': self.supplier.id
        })
        
        jeans_material = self.env['material.material'].create({
            'material_code': f'JEA{unique_suffix}',
            'material_name': 'Jeans Material',
            'material_type': 'jeans',
            'material_buy_price': 130.0,
            'supplier_id': self.supplier.id
        })
        
        cotton_material = self.env['material.material'].create({
            'material_code': 'COT001',
            'material_name': 'Cotton Material',
            'material_type': 'cotton',
            'material_buy_price': 140.0,
            'supplier_id': self.supplier.id
        })
        
        # Test filtering by fabric
        fabric_materials = self.env['material.material'].search([('material_type', '=', 'fabric')])
        self.assertIn(fabric_material, fabric_materials)
        self.assertNotIn(jeans_material, fabric_materials)
        self.assertNotIn(cotton_material, fabric_materials)
        
        # Test filtering by jeans
        jeans_materials = self.env['material.material'].search([('material_type', '=', 'jeans')])
        self.assertIn(jeans_material, jeans_materials)
        self.assertNotIn(fabric_material, jeans_materials)
        self.assertNotIn(cotton_material, jeans_materials) 