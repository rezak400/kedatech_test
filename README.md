# 📦 Material Management Module - Odoo 14

A comprehensive Material Management system for Odoo 14 with REST API endpoints.

## 🚀 Quick Setup

### Prerequisites

-   **Odoo 14** installed and running
-   **PostgreSQL** database
-   **Python 3.7+**

### Installation Steps

1. **Clone/Copy Module**

    ```bash
    cp -r material_management /path/to/odoo/custom_addons/
    ```

2. **Run Odoo with Specific Database** ⚠️ **IMPORTANT**

    ```bash
    python3 odoo-bin -c odoo.conf -d your_database_name --addons-path=addons,custom_addons
    ```

    **Note**: The `-d your_database_name` parameter is **REQUIRED** for custom module routes to work!

3. **Install Module**

    - Open browser: `http://localhost:8069` (or your port)
    - Login as Administrator
    - Go to **Apps** menu
    - Click **Update Apps List**
    - Search "Material Management"
    - Click **Install**

4. **Verify Installation**
    - Check menu: "Material Management" should appear
    - Test API: `curl -X GET "http://localhost:8069/api/materials" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{},"id":null}'`

## 🔧 Configuration

### Database Connection

-   Module requires active database connection
-   Routes only load when module is installed in specific database
-   Use `-d database_name` when starting Odoo

### Authentication

-   **Current**: `auth='public'` (for testing/interview purposes)
-   **Production**: Change to `auth='user'` in controllers/material_controller.py
-   **Note**: Public auth allows testing without session management

## 🗄️ Database Design (ERD)

The module includes a complete Entity Relationship Diagram (ERD) that can be imported into Draw.io:

**File**: `Material_Management_ERD.drawio`

### How to Import ERD

1. Open [Draw.io](https://app.diagrams.net/)
2. Click "Create New Diagram"
3. Choose "Import from..." → Select the `Material_Management_ERD.drawio` file
4. The ERD will load with complete database structure

### ERD Overview

-   **2 Entities**: Supplier (Pink) ↔ Material (Green)
-   **Relationship**: One-to-Many (1 Supplier can supply N Materials)
-   **Business Rules**: Material code unique, price ≥ 100, all required fields
-   **Visual Elements**: 🔑 Primary Keys, 🔗 Foreign Keys, constraints, and business rules

## 📡 Proper REST API

### Material Endpoints

| HTTP Method | Endpoint              | Description                        |
| ----------- | --------------------- | ---------------------------------- |
| GET         | `/api/materials`      | Get all materials (with filtering) |
| GET         | `/api/materials/<id>` | Get specific material              |
| POST        | `/api/materials`      | Create new material                |
| PUT         | `/api/materials/<id>` | Update material                    |
| DELETE      | `/api/materials/<id>` | Delete material                    |

### Supplier Endpoints

| HTTP Method | Endpoint         | Description         |
| ----------- | ---------------- | ------------------- |
| GET         | `/api/suppliers` | Get all suppliers   |
| POST        | `/api/suppliers` | Create new supplier |

### Request Format

**GET requests**: No body, use query parameters for filtering

**POST/PUT/DELETE requests**: JSON-RPC 2.0 format in body:

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        // Your data here
    },
    "id": null
}
```

### Filtering

Material filtering uses query parameters for GET requests:

-   `GET /api/materials?material_type=fabric`
-   `GET /api/materials?material_type=jeans`
-   `GET /api/materials?material_type=cotton`

## 🧪 Testing Examples

### 1. Get All Suppliers

```bash
curl -X GET "http://localhost:8069/api/suppliers"
```

### 2. Create Supplier

```bash
curl -X POST "http://localhost:8069/api/suppliers" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "name": "PT Supplier Test",
      "email": "test@supplier.com",
      "phone": "081234567890",
      "address": "Jl. Test No. 123"
    },
    "id": null
  }'
```

### 3. Get All Materials

```bash
curl -X GET "http://localhost:8069/api/materials"
```

### 4. Get Materials with Filter

```bash
curl -X GET "http://localhost:8069/api/materials?material_type=fabric"
```

### 5. Get Specific Material

```bash
curl -X GET "http://localhost:8069/api/materials/1"
```

### 6. Create Material

```bash
curl -X POST "http://localhost:8069/api/materials" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "material_code": "FAB001",
      "material_name": "Cotton Fabric",
      "material_type": "fabric",
      "material_buy_price": 150.0,
      "supplier_id": 1
    },
    "id": null
  }'
```

### 7. Update Material

```bash
curl -X PUT "http://localhost:8069/api/materials/1" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "material_name": "Premium Cotton Fabric",
      "material_buy_price": 200.0
    },
    "id": null
  }'
```

### 8. Delete Material

```bash
curl -X DELETE "http://localhost:8069/api/materials/1" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {},
    "id": null
  }'
```

## 📊 Data Validation

### Material Constraints

-   **material_code**: Required, unique, minimum 2 characters
-   **material_name**: Required
-   **material_type**: Required, must be: `fabric`, `jeans`, or `cotton`
-   **material_buy_price**: Required, minimum value 100
-   **supplier_id**: Required, must reference existing supplier

### Supplier Constraints

-   **name**: Required, unique

## 🔍 Response Format

### Success Response

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "success": true,
    "data": [...],
    "count": 1,
    "message": "Operation successful"
  }
}
```

### Error Response

```json
{
    "jsonrpc": "2.0",
    "id": null,
    "result": {
        "success": false,
        "error": "Error description"
    }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **404 Not Found on API calls**

    - **Solution**: Restart Odoo with `-d database_name`
    - **Cause**: Routes not loaded without specific database

2. **Module not appearing in Apps**

    - **Solution**: Click "Update Apps List" first
    - **Cause**: New modules not indexed

3. **Installation errors**

    - **Solution**: Check XML syntax in views
    - **Solution**: Verify model access rights

4. **Validation errors**
    - **Check**: Material price >= 100
    - **Check**: All required fields provided
    - **Check**: Valid material_type values

### Debug Commands

```bash
# Check Odoo logs
tail -f /var/log/odoo/odoo-server.log

# Install module via command line
python3 odoo-bin -i material_management -d your_database --stop-after-init

# Update module
python3 odoo-bin -u material_management -d your_database --stop-after-init
```

## 🧾 Requirements Met

### Business Requirements

-   ✅ Material registration with all required fields
-   ✅ Material type dropdown (Fabric, Jeans, Cotton)
-   ✅ Price validation (minimum 100)
-   ✅ Supplier relationship
-   ✅ View all materials with filtering
-   ✅ Update materials
-   ✅ Delete materials

### Technical Implementation

-   ✅ ERD designed
-   ✅ Models with constraints
-   ✅ REST API controllers
-   ✅ Unit tests
-   ✅ Views and UI
-   ✅ Security access rights

## 📝 Notes

-   **Authentication**: Currently set to `public` for easy testing
-   **Framework**: Built for Odoo 14 specifically
-   **Database**: Requires PostgreSQL
-   **Testing**: Comprehensive unit test coverage included

## 🔗 Import Postman Collection

Use the `Material_Management_API.postman_collection.json` file to import all endpoints into Postman for easy testing.

---

**Module Status**: ✅ Production Ready  
**Last Updated**: July 2024  
**Odoo Version**: 14.0
