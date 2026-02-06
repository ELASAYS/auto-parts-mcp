# 🚗 Auto Parts Inventory MCP

**MCP Server لإدارة مخزون قطع غيار ومنتجات السيارات مع تكامل WhatsApp**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io)

---

## 📋 الوصف

نظام MCP متكامل لإدارة:
- 📦 المخزون والمنتجات
- 🛒 الطلبات والفواتير
- 👥 العملاء والموردين
- 📊 التقارير والإحصائيات
- 💬 التكامل مع WhatsApp

**مصمم خصيصاً لتجار قطع غيار السيارات وزيوت المحركات!**

---

## ✨ المميزات

### 🎯 إدارة المخزون
- ✅ إضافة/تعديل/حذف المنتجات
- ✅ تتبع الكميات المتاحة
- ✅ تنبيهات عند انخفاض المخزون
- ✅ بحث متقدم بالفلاتر
- ✅ تصنيفات المنتجات

### 🛍️ إدارة الطلبات
- ✅ إنشاء طلبات سريعة
- ✅ توليد فواتير PDF تلقائياً
- ✅ حساب الإجمالي والخصومات
- ✅ تتبع حالة الطلبات
- ✅ إرسال للواتساب مباشرة

### 👥 إدارة العملاء
- ✅ قاعدة بيانات العملاء
- ✅ سجل المشتريات
- ✅ رسائل ترويجية
- ✅ العملاء الأكثر شراءً

### 📊 التقارير
- ✅ تقرير المبيعات اليومي/الشهري
- ✅ المنتجات الأكثر مبيعاً
- ✅ قيمة المخزون الحالي
- ✅ تصدير Excel/CSV/PDF

---

## 🚀 التثبيت السريع

### المتطلبات
- Python 3.10 أو أحدث
- pip

### الخطوات

```bash
# 1. استنساخ المشروع
git clone https://github.com/your-username/auto-parts-mcp.git
cd auto-parts-mcp

# 2. إنشاء بيئة افتراضية
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. تثبيت المكتبات
pip install -r requirements.txt

# 4. تشغيل الـ MCP Server
python src/server.py
```

---

## 🔧 التكوين

### 1. تعديل الإعدادات

عدّل ملف `config.json`:

```json
{
  "whatsapp": {
    "phone_number": "201019388501",
    "api_key": "your_api_key_here"
  },
  "database": {
    "path": "data/inventory.db"
  },
  "alerts": {
    "low_stock_threshold": 5
  }
}
```

### 2. ربط مع Claude Desktop

أضف للملف `claude_desktop_config.json`:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "auto-parts": {
      "command": "python",
      "args": [
        "C:/path/to/auto-parts-mcp/src/server.py"
      ]
    }
  }
}
```

---

## 📖 الأدوات المتاحة

### 📦 إدارة المنتجات

#### `add_product`
```javascript
await add_product({
  name: "موبيل 1 تخليقي 5W-30",
  category: "زيوت محركات",
  price: 450.00,
  cost: 380.00,
  quantity: 50,
  supplier: "موزع موبيل",
  min_stock: 10
})
```

#### `update_stock`
```javascript
await update_stock({
  product_id: 1,
  quantity: 30,
  operation: "add" // or "subtract" or "set"
})
```

#### `search_products`
```javascript
await search_products({
  query: "موبيل",
  category: "زيوت محركات",
  in_stock_only: true
})
```

#### `get_low_stock`
```javascript
await get_low_stock({
  threshold: 5
})
```

---

### 🛒 إدارة الطلبات

#### `create_order`
```javascript
await create_order({
  customer_name: "أحمد محمد",
  customer_phone: "01012345678",
  products: [
    { product_id: 1, quantity: 2 },
    { product_id: 3, quantity: 1 }
  ],
  discount: 50,
  notes: "توصيل سريع"
})
```

#### `generate_invoice`
```javascript
await generate_invoice({
  order_id: 123,
  format: "pdf" // or "txt"
})
```

#### `send_to_whatsapp`
```javascript
await send_to_whatsapp({
  order_id: 123,
  phone_number: "201012345678"
})
```

---

### 👥 إدارة العملاء

#### `add_customer`
```javascript
await add_customer({
  name: "أحمد محمد",
  phone: "01012345678",
  whatsapp: "201012345678",
  address: "القاهرة، مصر",
  notes: "عميل VIP"
})
```

#### `get_customer_history`
```javascript
await get_customer_history({
  customer_id: 5
})
```

#### `get_top_customers`
```javascript
await get_top_customers({
  limit: 10,
  period: "month" // or "week", "year", "all"
})
```

---

### 📊 التقارير

#### `daily_sales_report`
```javascript
await daily_sales_report({
  date: "2024-02-05"
})
```

#### `best_selling_products`
```javascript
await best_selling_products({
  period: "month",
  limit: 10
})
```

#### `inventory_value_report`
```javascript
await inventory_value_report()
```

#### `export_report`
```javascript
await export_report({
  report_type: "sales",
  format: "excel",
  start_date: "2024-01-01",
  end_date: "2024-01-31"
})
```

---

## 💡 أمثلة الاستخدام

### مثال 1: إضافة منتج جديد
```
أنت: أضف منتج جديد: كاسترول إيدج 5W-40، السعر 480 جنيه، الكمية 30
Claude: [يستخدم add_product]
✅ تم إضافة المنتج بنجاح!
📦 المنتج: كاسترول إيدج 5W-40
💰 السعر: 480.00 ج.م
📊 الكمية: 30 قطعة
🏷️ التصنيف: زيوت محركات
```

### مثال 2: إنشاء طلب
```
أنت: عميل جديد اسمه محمد يريد 2 موبيل 1 و 1 كاسترول إيدج
Claude: [يستخدم create_order + generate_invoice]
✅ تم إنشاء الطلب #45
👤 العميل: محمد
📦 المنتجات:
  - موبيل 1 تخليقي × 2 = 900 ج.م
  - كاسترول إيدج × 1 = 480 ج.م
💰 الإجمالي: 1,380 ج.م
📄 تم توليد الفاتورة
```

### مثال 3: تقرير يومي
```
أنت: أعطني تقرير مبيعات اليوم
Claude: [يستخدم daily_sales_report]
📊 تقرير المبيعات - 2024-02-05

💰 إجمالي المبيعات: 15,450 ج.م
📦 عدد الطلبات: 23
👥 عدد العملاء: 18
📈 متوسط الطلب: 671.74 ج.م

🏆 الأكثر مبيعاً:
1. موبيل 1 (12 قطعة)
2. كاسترول إيدج (8 قطع)
3. شل هيليكس (6 قطع)
```

---

## 🗂️ هيكل المشروع

```
auto-parts-mcp/
├── src/
│   ├── server.py           # MCP Server الرئيسي
│   ├── database.py         # إدارة قاعدة البيانات
│   ├── models.py           # نماذج البيانات
│   ├── tools/              # أدوات MCP
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── customers.py
│   │   └── reports.py
│   └── utils/              # وظائف مساعدة
│       ├── invoice.py
│       ├── whatsapp.py
│       └── export.py
├── data/
│   └── inventory.db        # قاعدة البيانات SQLite
├── templates/
│   └── invoice.html        # قالب الفاتورة
├── tests/
│   └── test_tools.py
├── config.json
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🧪 الاختبار

```bash
# تشغيل الاختبارات
pytest tests/

# مع التغطية
pytest --cov=src tests/
```

---

## 📱 تكامل WhatsApp

يدعم النظام إرسال الفواتير عبر WhatsApp باستخدام:
- WhatsApp Business API
- أو خدمات مثل Twilio/MessageBird

قم بتعديل `src/utils/whatsapp.py` وأضف API key الخاص بك.

---

## 🔒 الأمان

- ✅ تشفير البيانات الحساسة
- ✅ التحقق من صحة المدخلات
- ✅ حماية من SQL Injection
- ✅ نسخ احتياطي تلقائي

---

## 🤝 المساهمة

نرحب بالمساهمات! الرجاء:

1. Fork المشروع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

---

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License - انظر ملف [LICENSE](LICENSE) للتفاصيل

---

## 📞 الدعم

- 📧 Email: support@example.com
- 💬 Discord: [Join Server](https://discord.gg/example)
- 📚 Docs: [Documentation](https://docs.example.com)

---

## 🎯 خارطة الطريق

- [x] إدارة المخزون الأساسية
- [x] نظام الطلبات
- [x] توليد الفواتير PDF
- [x] تكامل WhatsApp
- [ ] تطبيق موبايل
- [ ] Barcode Scanner
- [ ] تكامل مع أنظمة الدفع
- [ ] Dashboard تحليلي
- [ ] Multi-tenant support

---

## 🙏 شكر خاص

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Anthropic Claude](https://claude.ai)
- جميع المساهمين في المشروع

---

**صُنع بـ ❤️ لتجار قطع غيار السيارات**

⭐ إذا أعجبك المشروع، لا تنسى إعطائه نجمة على GitHub!