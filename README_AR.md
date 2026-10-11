# Dafan Discord Multi-Tool — Safe Edition

نسخة آمنة بواجهة رسومية لنظام Windows، مستوحاة من اسم الأداة الأصلية. لا تتضمن وظائف السبام أو Raid أو توليد/جمع Tokens أو Nitro أو تدمير الحسابات، ولا تتصل بحساب Discord.

## المميزات
- واجهة رسومية داكنة بالعربية والإنجليزية.
- فتح ملفات JSON وTXT وCSV المحلية ومعاينتها.
- إحصاءات أساسية للملف وعدد السجلات والمفاتيح.
- إنشاء نسخة احتياطية من الملف الأصلي.
- إضافة ملاحظات محلية وتصدير التقرير إلى TXT.
- لا تطلب Discord Token ولا ترسله إلى أي جهة.

## إنشاء ملف EXE على Windows
1. فك ضغط المشروع.
2. ثبّت Python 3.11 أو أحدث من https://www.python.org/downloads/windows/ مع تفعيل خيار **Add Python to PATH**.
3. انقر مرتين على `build_windows.bat` وانتظر انتهاء البناء.
4. ستجد الملف في `dist\Discord_Multi_Tool.exe`.

يحتاج بناء EXE إلى Windows؛ لا يمكن إنتاج ملف Windows EXE أصلي مباشرةً من Termux/Android باستخدام هذا الملف وحده.

## البناء عبر GitHub Actions
ارفع ملفات المشروع إلى مستودع GitHub، ثم افتح تبويب **Actions** وشغّل **Build Windows EXE**. بعد النجاح نزّل Artifact باسم `Discord_Multi_Tool_Windows`.

## ملاحظة
هذه النسخة تعمل على الملفات المحلية فقط؛ ليست أداة تسجيل دخول أو تحكم بحساب Discord، ولا تتجاوز صلاحيات Discord.
