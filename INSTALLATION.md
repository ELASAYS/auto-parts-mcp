# 🚀 دليل التثبيت الشامل

## المتطلبات الأساسية

### 1. Python
- **الإصدار المطلوب:** Python 3.10 أو أحدث
- **التحقق من التثبيت:**
  ```bash
  python --version
  # يجب أن يظهر: Python 3.10.x أو أعلى
  ```

### 2. Git
- **للتحميل من GitHub**
- **التحقق:**
  ```bash
  git --version
  ```

### 3. Claude Desktop
- قم بتحميله من: https://claude.ai/download

---

## خطوات التثبيت

### الخطوة 1: تحميل المشروع

```bash
# استنساخ المشروع
git clone https://github.com/your-username/auto-parts-mcp.git

# الانتقال إلى المجلد
cd auto-parts-mcp
```

### الخطوة 2: إنشاء البيئة الافتراضية

#### على Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### على macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### الخطوة 3: تثبيت المكتبات

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### الخطوة 4: تكوين الإعدادات

1. **افتح ملف `config.json`**
2. **عدّل رقم الواتساب:**
   ```json
   {
     "whatsapp": {
       "phone_number": "201019388501"  // ضع رقمك هنا
     }
   }
   ```

### الخطوة 5: اختبار التشغيل

```bash
# تشغيل السيرفر
python src/server.py
```

يجب أن ترى:
```
INFO - Starting Auto Parts Inventory MCP Server...
```

اضغط `Ctrl+C` للإيقاف.

---

## ربط مع Claude Desktop

### Windows

1. **افتح الملف:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **أضف التكوين:**
   ```json
   {
     "mcpServers": {
       "auto-parts": {
         "command": "python",
         "args": [
           "C:\\Users\\YourName\\auto-parts-mcp\\src\\server.py"
         ]
       }
     }
   }
   ```

3. **استبدل المسار** بمسار المشروع الحقيقي

### macOS

1. **افتح الملف:**
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **أضف التكوين:**
   ```json
   {
     "mcpServers": {
       "auto-parts": {
         "command": "python3",
         "args": [
           "/Users/yourname/auto-parts-mcp/src/server.py"
         ]
       }
     }
   }
   ```

### Linux

1. **افتح الملف:**
   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```

2. **نفس التكوين مثل macOS**

---

## التحقق من التثبيت

### 1. أعد تشغيل Claude Desktop

### 2. افتح محادثة جديدة

### 3. اكتب:
```
هل MCP Auto Parts متصل؟
```

يجب أن يرد Claude:
```
نعم! MCP Auto Parts متصل وجاهز للاستخدام.
```

### 4. جرب إضافة منتج:
```
أضف منتج جديد: موبيل 1، السعر 450، الكمية 50
```

---

## حل المشاكل الشائعة

### مشكلة: "Python not found"

**الحل:**
```bash
# Windows: ثبت Python من python.org
# macOS: 
brew install python3

# Linux:
sudo apt install python3 python3-pip
```

### مشكلة: "Permission denied"

**الحل (macOS/Linux):**
```bash
chmod +x src/server.py
```

### مشكلة: "Module not found"

**الحل:**
```bash
# تأكد من تفعيل البيئة الافتراضية
pip install -r requirements.txt --force-reinstall
```

### مشكلة: "Database error"

**الحل:**
```bash
# أنشئ مجلد data
mkdir data

# احذف قاعدة البيانات القديمة
rm data/inventory.db

# شغّل السيرفر مرة أخرى
python src/server.py
```

### مشكلة: "MCP not connecting"

**الحل:**
1. تأكد من المسار صحيح في config
2. أعد تشغيل Claude Desktop
3. تحقق من logs:
   - Windows: `%APPDATA%\Claude\logs\`
   - macOS: `~/Library/Logs/Claude/`

---

## الخطوات التالية

بعد التثبيت الناجح:

1. ✅ جرب جميع الأدوات
2. ✅ أضف منتجاتك
3. ✅ أنشئ طلبات تجريبية
4. ✅ راجع التقارير
5. ✅ خصص الإعدادات

---

## دعم إضافي

- 📖 راجع README.md للتوثيق الكامل
- 🐛 أبلغ عن المشاكل على GitHub Issues
- 💬 انضم لمجتمع Discord

---

**مبروك! 🎉 MCP الخاص بك جاهز الآن!**