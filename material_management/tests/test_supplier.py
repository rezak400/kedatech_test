# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestSupplier(TransactionCase):

    def test_create_supplier_success(self):
        """Test successful supplier creation"""
        supplier = self.env['material.supplier'].create({
            'name': 'Test Supplier',
            'email': 'test@supplier.com',
            'phone': '123456789',
            'address': 'Test Address'
        })
        
        self.assertTrue(supplier.id)
        self.assertEqual(supplier.name, 'Test Supplier')
        self.assertEqual(supplier.email, 'test@supplier.com')
        self.assertEqual(supplier.phone, '123456789')
        self.assertEqual(supplier.address, 'Test Address')

    def test_supplier_name_required(self):
        """Test that supplier name is required"""
        from psycopg2.errors import NotNullViolation
        with self.assertRaises(NotNullViolation):
            with self.env.cr.savepoint():
                self.env['material.supplier'].create({
                    'email': 'test@supplier.com',
                    'phone': '123456789',
                    'address': 'Test Address'
                })

    def test_supplier_name_unique_constraint(self):
        """Test supplier name uniqueness"""
        import time
        unique_name = f'Unique Supplier {str(int(time.time() * 1000))[-6:]}'
        
        # Create first supplier
        self.env['material.supplier'].create({
            'name': unique_name,
            'email': 'unique@supplier.com'
        })
        
        # Try to create second supplier with same name
        from psycopg2.errors import UniqueViolation
        with self.assertRaises(UniqueViolation):
            with self.env.cr.savepoint():
                self.env['material.supplier'].create({
                    'name': unique_name,  # Duplicate name
                    'email': 'another@supplier.com'
                })

    def test_supplier_name_get(self):
        """Test supplier name_get method"""
        supplier = self.env['material.supplier'].create({
            'name': 'Name Get Supplier',
            'email': 'nameget@supplier.com'
        })
        
        name_get_result = supplier.name_get()
        self.assertEqual(name_get_result[0][1], 'Name Get Supplier')

    def test_supplier_update(self):
        """Test supplier update functionality"""
        supplier = self.env['material.supplier'].create({
            'name': 'Update Supplier',
            'email': 'update@supplier.com',
            'phone': '111111111'
        })
        
        # Update supplier
        supplier.write({
            'email': 'updated@supplier.com',
            'phone': '222222222',
            'address': 'Updated Address'
        })
        
        self.assertEqual(supplier.email, 'updated@supplier.com')
        self.assertEqual(supplier.phone, '222222222')
        self.assertEqual(supplier.address, 'Updated Address')

    def test_supplier_delete(self):
        """Test supplier deletion"""
        supplier = self.env['material.supplier'].create({
            'name': 'Delete Supplier',
            'email': 'delete@supplier.com'
        })
        
        supplier_id = supplier.id
        supplier.unlink()
        
        # Verify supplier is deleted
        deleted_supplier = self.env['material.supplier'].browse(supplier_id)
        self.assertFalse(deleted_supplier.exists())

    def test_supplier_optional_fields(self):
        """Test that email, phone, and address are optional"""
        supplier = self.env['material.supplier'].create({
            'name': 'Minimal Supplier'
        })
        
        self.assertTrue(supplier.id)
        self.assertEqual(supplier.name, 'Minimal Supplier')
        self.assertFalse(supplier.email)
        self.assertFalse(supplier.phone)
        self.assertFalse(supplier.address) 