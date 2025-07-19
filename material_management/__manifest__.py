{
    'name': 'Material Management',
    'version': '14.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Material Registration and Management System',
    'description': """
        Material Management System for Odoo 14
        =======================================
        
        🎯 Complete material registration system with REST API endpoints
        
        📋 IMPORTANT SETUP INSTRUCTIONS:
        ==============================
        
        ⚠️  CRITICAL: Must run Odoo with specific database parameter:
            python3 odoo-bin -c odoo.conf -d your_database_name --addons-path=addons,custom_addons
            
        📌 The '-d database_name' parameter is REQUIRED for custom module routes to work!
        
        🔧 Installation Steps:
        1. Copy module to custom_addons folder
        2. Start Odoo with database parameter (see above)
        3. Go to Apps menu → Update Apps List
        4. Search "Material Management" → Install
        5. Verify: Menu should appear & test API endpoint
        
        🔐 Authentication Note:
        - Currently uses auth='public' for testing/interview purposes
        - No session management required for API testing
        - For production: change to auth='user' in controllers/material_controller.py
        
                 📡 REST API with JSON-RPC Format:
         ==================================
         
         Materials:
         - GET /api/materials (get all + filtering)
         - GET /api/materials/<id> (get specific)
         - POST /api/materials (create)
         - PUT /api/materials/<id> (update)
         - DELETE /api/materials/<id> (delete)
         
         Suppliers:  
         - GET /api/suppliers (get all)
         - POST /api/suppliers (create)
         
         🎯 Best of Both Worlds:
         - Semantic HTTP methods (GET, POST, PUT, DELETE)
         - Structured JSON-RPC 2.0 request/response format
         
         🧪 Quick Test:
         curl -X GET "http://localhost:8069/api/materials" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{},"id":null}'
        
        📊 Data Requirements:
        ====================
        
        Material Fields (all required):
        - material_code: unique code (min 2 chars)
        - material_name: material name  
        - material_type: fabric/jeans/cotton
        - material_buy_price: minimum 100
        - supplier_id: existing supplier ID
        
        Supplier Fields:
        - name: required, unique
        - email, phone, address: optional
        
        ✅ Features Included:
        ====================
        - Complete CRUD operations
        - Material filtering by type
        - Price validation (min 100)
        - Unique constraints
        - REST API with JSON responses
        - Unit test coverage
        - Postman collection included
        
        📄 Files Included:
        - README.md (comprehensive guide)
        - Material_Management_API.postman_collection.json (import to Postman)
        - Complete MVC structure (Models, Views, Controllers)
        - Unit tests in tests/ folder
        
        🏆 Ready for production use with proper authentication setup!
    """,
    'author': 'Your Company',
    'website': 'https://www.rezadwiputra.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/supplier_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
} 