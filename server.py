#!/usr/bin/env python3
"""
Auto Parts Inventory MCP Server
Main entry point for the MCP server
"""

import json
import logging
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from database import Database
from models import Product, Order, Customer, OrderItem

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Initialize database
db = Database(config['database']['path'])

# Create MCP server
app = Server("auto-parts-inventory")


# ====================================
# Product Management Tools
# ====================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        # Products
        Tool(
            name="add_product",
            description="Add a new product to inventory",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Product name"},
                    "category": {"type": "string", "description": "Product category"},
                    "price": {"type": "number", "description": "Selling price"},
                    "cost": {"type": "number", "description": "Cost price"},
                    "quantity": {"type": "integer", "description": "Initial quantity"},
                    "supplier": {"type": "string", "description": "Supplier name (optional)"},
                    "min_stock": {"type": "integer", "description": "Minimum stock level (optional)"},
                },
                "required": ["name", "category", "price", "cost", "quantity"],
            },
        ),
        Tool(
            name="search_products",
            description="Search for products by name or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "category": {"type": "string", "description": "Filter by category (optional)"},
                    "in_stock_only": {"type": "boolean", "description": "Show only in-stock products (optional)"},
                },
            },
        ),
        Tool(
            name="update_stock",
            description="Update product stock quantity",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "description": "Product ID"},
                    "quantity": {"type": "integer", "description": "Quantity to add/subtract/set"},
                    "operation": {"type": "string", "enum": ["add", "subtract", "set"], "description": "Operation type"},
                },
                "required": ["product_id", "quantity"],
            },
        ),
        Tool(
            name="get_low_stock",
            description="Get products with low stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "threshold": {"type": "integer", "description": "Stock threshold (optional)"},
                },
            },
        ),
        
        # Orders
        Tool(
            name="create_order",
            description="Create a new order",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Customer name"},
                    "customer_phone": {"type": "string", "description": "Customer phone"},
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "integer"},
                                "quantity": {"type": "integer"},
                            },
                            "required": ["product_id", "quantity"],
                        },
                        "description": "List of products",
                    },
                    "discount": {"type": "number", "description": "Discount amount (optional)"},
                    "notes": {"type": "string", "description": "Order notes (optional)"},
                },
                "required": ["customer_name", "customer_phone", "products"],
            },
        ),
        Tool(
            name="get_order",
            description="Get order details by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "Order ID"},
                },
                "required": ["order_id"],
            },
        ),
        
        # Customers
        Tool(
            name="add_customer",
            description="Add a new customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Customer name"},
                    "phone": {"type": "string", "description": "Phone number"},
                    "whatsapp": {"type": "string", "description": "WhatsApp number (optional)"},
                    "address": {"type": "string", "description": "Address (optional)"},
                    "notes": {"type": "string", "description": "Notes (optional)"},
                },
                "required": ["name", "phone"],
            },
        ),
        Tool(
            name="get_customer_history",
            description="Get customer order history",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer", "description": "Customer ID"},
                },
                "required": ["customer_id"],
            },
        ),
        
        # Reports
        Tool(
            name="daily_sales_report",
            description="Get daily sales report",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD, optional - defaults to today)"},
                },
            },
        ),
        Tool(
            name="best_selling_products",
            description="Get best selling products",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of products to return (optional)"},
                    "period": {"type": "string", "description": "Time period (optional)"},
                },
            },
        ),
        Tool(
            name="inventory_value_report",
            description="Get current inventory value report",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    try:
        # Product Management
        if name == "add_product":
            product_id = db.add_product(arguments)
            product = db.get_product(product_id)
            
            return [TextContent(
                type="text",
                text=f"""✅ تم إضافة المنتج بنجاح!

📦 المنتج: {product['name']}
🏷️ التصنيف: {product['category']}
💰 السعر: {product['price']:.2f} {config['invoice']['currency']}
📊 الكمية: {product['quantity']} قطعة
🔖 التكلفة: {product['cost']:.2f} {config['invoice']['currency']}
📌 الحد الأدنى: {product['min_stock']} قطع

ID: {product_id}"""
            )]
        
        elif name == "search_products":
            products = db.search_products(
                query=arguments.get('query', ''),
                category=arguments.get('category', ''),
                in_stock_only=arguments.get('in_stock_only', False)
            )
            
            if not products:
                return [TextContent(
                    type="text",
                    text="❌ لم يتم العثور على منتجات"
                )]
            
            result = f"📦 تم العثور على {len(products)} منتج:\n\n"
            for p in products[:10]:
                result += f"🔹 {p['name']}\n"
                result += f"   التصنيف: {p['category']}\n"
                result += f"   السعر: {p['price']:.2f} {config['invoice']['currency']}\n"
                result += f"   الكمية: {p['quantity']} قطعة\n"
                result += f"   ID: {p['id']}\n\n"
            
            if len(products) > 10:
                result += f"... و {len(products) - 10} منتج آخر"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "update_stock":
            success = db.update_stock(
                product_id=arguments['product_id'],
                quantity=arguments['quantity'],
                operation=arguments.get('operation', 'set')
            )
            
            if success:
                product = db.get_product(arguments['product_id'])
                return [TextContent(
                    type="text",
                    text=f"""✅ تم تحديث المخزون بنجاح!

📦 المنتج: {product['name']}
📊 الكمية الجديدة: {product['quantity']} قطعة
💰 قيمة المخزون: {product['quantity'] * product['cost']:.2f} {config['invoice']['currency']}"""
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ فشل تحديث المخزون. تحقق من ID المنتج."
                )]
        
        elif name == "get_low_stock":
            products = db.get_low_stock_products(
                threshold=arguments.get('threshold')
            )
            
            if not products:
                return [TextContent(
                    type="text",
                    text="✅ جميع المنتجات متوفرة بكميات كافية!"
                )]
            
            result = f"⚠️ تنبيه: {len(products)} منتج قارب على النفاد:\n\n"
            for p in products:
                result += f"🔴 {p['name']}\n"
                result += f"   الكمية المتبقية: {p['quantity']} قطعة\n"
                result += f"   الحد الأدنى: {p['min_stock']} قطع\n"
                result += f"   ID: {p['id']}\n\n"
            
            return [TextContent(type="text", text=result)]
        
        # Order Management
        elif name == "create_order":
            # Get customer or create new
            customer = db.get_customer_by_phone(arguments['customer_phone'])
            customer_id = customer['id'] if customer else None
            
            # Calculate order totals
            items = []
            subtotal = 0
            
            for item_data in arguments['products']:
                product = db.get_product(item_data['product_id'])
                if not product:
                    return [TextContent(
                        type="text",
                        text=f"❌ المنتج ID {item_data['product_id']} غير موجود"
                    )]
                
                if product['quantity'] < item_data['quantity']:
                    return [TextContent(
                        type="text",
                        text=f"❌ كمية غير كافية للمنتج: {product['name']}\n" +
                             f"المتوفر: {product['quantity']} قطعة\n" +
                             f"المطلوب: {item_data['quantity']} قطعة"
                    )]
                
                item_total = product['price'] * item_data['quantity']
                items.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'quantity': item_data['quantity'],
                    'unit_price': product['price'],
                    'total_price': item_total
                })
                subtotal += item_total
            
            discount = arguments.get('discount', 0)
            tax = subtotal * config['invoice']['tax_rate']
            total = subtotal - discount + tax
            
            order_data = {
                'customer_id': customer_id,
                'customer_name': arguments['customer_name'],
                'customer_phone': arguments['customer_phone'],
                'customer_whatsapp': arguments.get('customer_whatsapp'),
                'items': items,
                'subtotal': subtotal,
                'discount': discount,
                'tax': tax,
                'total': total,
                'notes': arguments.get('notes')
            }
            
            order_id = db.create_order(order_data)
            
            result = f"""✅ تم إنشاء الطلب #{order_id} بنجاح!

👤 العميل: {arguments['customer_name']}
📱 الهاتف: {arguments['customer_phone']}

📦 المنتجات:
"""
            for item in items:
                result += f"  • {item['product_name']} × {item['quantity']} = {item['total_price']:.2f} {config['invoice']['currency']}\n"
            
            result += f"""
💵 المجموع الفرعي: {subtotal:.2f} {config['invoice']['currency']}
🎁 الخصم: {discount:.2f} {config['invoice']['currency']}
📊 الضريبة ({config['invoice']['tax_rate']*100}%): {tax:.2f} {config['invoice']['currency']}
💰 الإجمالي: {total:.2f} {config['invoice']['currency']}
"""
            
            if arguments.get('notes'):
                result += f"\n📝 ملاحظات: {arguments['notes']}"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "get_order":
            order = db.get_order(arguments['order_id'])
            
            if not order:
                return [TextContent(
                    type="text",
                    text=f"❌ الطلب #{arguments['order_id']} غير موجود"
                )]
            
            result = f"""📋 تفاصيل الطلب #{order['id']}

👤 العميل: {order['customer_name']}
📱 الهاتف: {order['customer_phone']}
📅 التاريخ: {order['created_at']}
🔖 الحالة: {order['status']}

📦 المنتجات:
"""
            for item in order['items']:
                result += f"  • {item['product_name']} × {item['quantity']} = {item['total_price']:.2f} {config['invoice']['currency']}\n"
            
            result += f"""
💵 المجموع الفرعي: {order['subtotal']:.2f} {config['invoice']['currency']}
🎁 الخصم: {order['discount']:.2f} {config['invoice']['currency']}
📊 الضريبة: {order['tax']:.2f} {config['invoice']['currency']}
💰 الإجمالي: {order['total']:.2f} {config['invoice']['currency']}
"""
            
            if order['notes']:
                result += f"\n📝 ملاحظات: {order['notes']}"
            
            return [TextContent(type="text", text=result)]
        
        # Customer Management
        elif name == "add_customer":
            customer_id = db.add_customer(arguments)
            
            return [TextContent(
                type="text",
                text=f"""✅ تم إضافة العميل بنجاح!

👤 الاسم: {arguments['name']}
📱 الهاتف: {arguments['phone']}
💬 واتساب: {arguments.get('whatsapp', 'غير محدد')}
📍 العنوان: {arguments.get('address', 'غير محدد')}

ID: {customer_id}"""
            )]
        
        elif name == "get_customer_history":
            orders = db.get_customer_orders(arguments['customer_id'])
            
            if not orders:
                return [TextContent(
                    type="text",
                    text="❌ لا يوجد طلبات لهذا العميل"
                )]
            
            total_purchases = sum(o['total'] for o in orders)
            
            result = f"""📊 سجل مشتريات العميل

📦 عدد الطلبات: {len(orders)}
💰 إجمالي المشتريات: {total_purchases:.2f} {config['invoice']['currency']}
📅 آخر طلب: {orders[0]['created_at']}

الطلبات الأخيرة:
"""
            for order in orders[:5]:
                result += f"  • طلب #{order['id']} - {order['total']:.2f} {config['invoice']['currency']} - {order['created_at']}\n"
            
            return [TextContent(type="text", text=result)]
        
        # Reports
        elif name == "daily_sales_report":
            from datetime import datetime
            date = arguments.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            report = db.get_sales_report(start_date=date, end_date=date)
            products = db.get_best_selling_products(limit=5, start_date=date)
            
            result = f"""📊 تقرير المبيعات - {date}

💰 إجمالي المبيعات: {report['total_sales'] or 0:.2f} {config['invoice']['currency']}
📦 عدد الطلبات: {report['total_orders'] or 0}
📈 متوسط الطلب: {report['average_order'] or 0:.2f} {config['invoice']['currency']}
🎁 إجمالي الخصومات: {report['total_discounts'] or 0:.2f} {config['invoice']['currency']}

🏆 الأكثر مبيعاً:
"""
            for i, p in enumerate(products, 1):
                result += f"  {i}. {p['name']} ({p['total_sold']} قطعة)\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "best_selling_products":
            limit = arguments.get('limit', 10)
            products = db.get_best_selling_products(limit=limit)
            
            result = f"🏆 أفضل {len(products)} منتج مبيعاً:\n\n"
            for i, p in enumerate(products, 1):
                result += f"{i}. {p['name']}\n"
                result += f"   المبيعات: {p['total_sold']} قطعة\n"
                result += f"   الإيرادات: {p['total_revenue']:.2f} {config['invoice']['currency']}\n\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "inventory_value_report":
            products = db.search_products()
            
            total_value = sum(p['quantity'] * p['cost'] for p in products)
            total_items = sum(p['quantity'] for p in products)
            
            result = f"""💼 تقرير قيمة المخزون

📦 إجمالي المنتجات: {len(products)} منتج
📊 إجمالي القطع: {total_items} قطعة
💰 قيمة المخزون: {total_value:.2f} {config['invoice']['currency']}
📈 متوسط قيمة المنتج: {total_value/len(products) if products else 0:.2f} {config['invoice']['currency']}
"""
            
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(
                type="text",
                text=f"❌ أداة غير معروفة: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"❌ حدث خطأ: {str(e)}"
        )]


def main():
    """Main entry point"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Auto Parts Inventory MCP Server...")
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()