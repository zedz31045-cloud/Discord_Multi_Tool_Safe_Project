import csv
import json
import os
import shutil
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

APP_NAME = "Discord Multi-Tool | Safe Edition"

class SafeDiscordTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("940x650")
        self.minsize(780, 540)
        self.configure(bg="#10131a")
        self.current_path = None
        self.data = None
        self._style()
        self._build()

    def _style(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("TFrame", background="#10131a")
        s.configure("Panel.TFrame", background="#191f2b")
        s.configure("TLabel", background="#10131a", foreground="#edf2f7", font=("Segoe UI", 10))
        s.configure("Title.TLabel", font=("Segoe UI", 19, "bold"), foreground="#72d5ff")
        s.configure("Sub.TLabel", foreground="#aeb8c8")
        s.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8), background="#273449", foreground="#ffffff")
        s.map("TButton", background=[("active", "#36516e")])
        s.configure("Treeview", background="#151b25", fieldbackground="#151b25", foreground="#edf2f7", rowheight=26)
        s.configure("Treeview.Heading", background="#273449", foreground="#ffffff", font=("Segoe UI", 10, "bold"))

    def _build(self):
        header = ttk.Frame(self, padding=(22, 18, 22, 8))
        header.pack(fill="x")
        ttk.Label(header, text="Dafan • Discord Multi-Tool", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Safe Edition — local files only; no login tokens or automated mass actions.", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        warning = tk.Label(self, text="تنبيه: هذه النسخة لا تتصل بحساب Discord ولا تطلب Token. استخدم ملفات صدّرتها بنفسك وبشكل مصرح.",
                           bg="#3b2a18", fg="#ffd99a", padx=12, pady=9, anchor="w", font=("Segoe UI", 10))
        warning.pack(fill="x", padx=22, pady=(8, 12))

        actions = ttk.Frame(self, padding=(22, 0, 22, 12))
        actions.pack(fill="x")
        ttk.Button(actions, text="فتح ملف JSON / TXT / CSV", command=self.open_file).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="إنشاء نسخة احتياطية", command=self.backup_file).pack(side="left", padx=8)
        ttk.Button(actions, text="تصدير التقرير", command=self.export_report).pack(side="left", padx=8)
        ttk.Button(actions, text="مسح العرض", command=self.clear).pack(side="right")

        body = ttk.Frame(self, padding=(22, 0, 22, 12))
        body.pack(fill="both", expand=True)
        left = ttk.Frame(body, style="Panel.TFrame", padding=15)
        left.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(left, text="الأدوات الآمنة", font=("Segoe UI", 12, "bold"), background="#191f2b").pack(anchor="w", pady=(0, 12))
        for title, desc in [
            ("تحليل الملف", "عدد السجلات والمفاتيح"),
            ("نسخ احتياطي", "حفظ نسخة من الملف الأصلي"),
            ("سجل محلي", "كتابة ملاحظات محلية"),
            ("عرض المحتوى", "معاينة النص أو JSON/CSV"),
        ]:
            box = tk.Frame(left, bg="#222b3a", padx=10, pady=8)
            box.pack(fill="x", pady=5)
            tk.Label(box, text=title, bg="#222b3a", fg="#72d5ff", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(box, text=desc, bg="#222b3a", fg="#c1cad8", font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))

        right = ttk.Frame(body, style="Panel.TFrame", padding=12)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="النتائج / Results", font=("Segoe UI", 12, "bold"), background="#191f2b").pack(anchor="w", pady=(0, 8))
        self.text = tk.Text(right, bg="#0d1117", fg="#dce6f2", insertbackground="white", relief="flat", wrap="word", font=("Consolas", 10), padx=10, pady=10)
        self.text.pack(fill="both", expand=True)
        self.text.insert("1.0", "مرحباً بك في Dafan Discord Multi-Tool Safe Edition\n\n• افتح ملفاً محلياً بصيغة JSON أو TXT أو CSV.\n• اعرض المحتوى والإحصاءات الأساسية.\n• أنشئ نسخة احتياطية أو صدّر تقريراً نصياً.\n\nلا تستخدم ملفات لا تملك إذناً بالوصول إليها.")
        self.status = tk.StringVar(value="جاهز | Ready")
        tk.Label(self, textvariable=self.status, bg="#080b10", fg="#aeb8c8", anchor="w", padx=15, pady=7).pack(fill="x", side="bottom")

        notes = ttk.Frame(self, padding=(22, 0, 22, 12))
        notes.pack(fill="x")
        ttk.Button(notes, text="إضافة ملاحظة إلى السجل المحلي", command=self.add_note).pack(side="left")

    def log(self, text):
        self.text.insert("end", "\n" + text)
        self.text.see("end")

    def open_file(self):
        path = filedialog.askopenfilename(title="اختر ملفاً", filetypes=[("Supported files", "*.json *.txt *.csv"), ("All files", "*.*")])
        if not path:
            return
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext == ".json":
                with open(path, "r", encoding="utf-8-sig") as f:
                    self.data = json.load(f)
                preview = json.dumps(self.data, ensure_ascii=False, indent=2)
                report = self.analyze(self.data)
            elif ext == ".csv":
                with open(path, "r", encoding="utf-8-sig", newline="") as f:
                    self.data = list(csv.DictReader(f))
                preview = json.dumps(self.data[:100], ensure_ascii=False, indent=2)
                report = self.analyze(self.data)
            else:
                with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
                    preview = f.read(200000)
                self.data = preview
                report = f"نوع الملف: نص\nعدد الأحرف المعروضة: {len(preview)}"
            self.current_path = path
            self.text.delete("1.0", "end")
            self.text.insert("1.0", f"الملف: {path}\n\n--- التحليل ---\n{report}\n\n--- معاينة المحتوى ---\n{preview[:30000]}")
            self.status.set(f"تم فتح: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("تعذر فتح الملف", str(e))

    def analyze(self, data):
        if isinstance(data, dict):
            keys = list(data.keys())
            return f"النوع: JSON object\nعدد المفاتيح العليا: {len(keys)}\nالمفاتيح: {', '.join(map(str, keys[:60]))}"
        if isinstance(data, list):
            sample_keys = sorted({str(k) for item in data[:1000] if isinstance(item, dict) for k in item.keys()})
            return f"النوع: قائمة\nعدد السجلات: {len(data)}\nمفاتيح السجلات (إن وجدت): {', '.join(sample_keys[:60]) or 'لا توجد'}"
        return f"نوع البيانات: {type(data).__name__}"

    def backup_file(self):
        if not self.current_path or not os.path.isfile(self.current_path):
            messagebox.showinfo("نسخة احتياطية", "افتح ملفاً أولاً.")
            return
        default = os.path.basename(self.current_path) + ".backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        target = filedialog.asksaveasfilename(title="حفظ النسخة الاحتياطية", initialfile=default, initialdir=os.path.dirname(self.current_path))
        if not target:
            return
        try:
            shutil.copy2(self.current_path, target)
            self.log(f"\n[Backup] تم حفظ النسخة: {target}")
            self.status.set("تم إنشاء النسخة الاحتياطية")
        except Exception as e:
            messagebox.showerror("فشل النسخ", str(e))

    def export_report(self):
        content = self.text.get("1.0", "end-1c")
        if not content.strip():
            messagebox.showinfo("تصدير التقرير", "لا يوجد محتوى لتصديره.")
            return
        target = filedialog.asksaveasfilename(title="تصدير التقرير", defaultextension=".txt", filetypes=[("Text report", "*.txt")], initialfile="Dafan_Discord_Report.txt")
        if not target:
            return
        try:
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)
            self.status.set("تم تصدير التقرير")
            messagebox.showinfo("نجاح", "تم حفظ التقرير.")
        except Exception as e:
            messagebox.showerror("تعذر التصدير", str(e))

    def add_note(self):
        win = tk.Toplevel(self)
        win.title("ملاحظة محلية")
        win.geometry("480x250")
        win.configure(bg="#10131a")
        tk.Label(win, text="اكتب ملاحظتك (تُضاف إلى العرض ويمكن تصديرها):", bg="#10131a", fg="white").pack(anchor="w", padx=12, pady=12)
        field = tk.Text(win, height=6, bg="#0d1117", fg="white", insertbackground="white", wrap="word")
        field.pack(fill="both", expand=True, padx=12)
        def save():
            note = field.get("1.0", "end-1c").strip()
            if note:
                self.log(f"\n[ملاحظة {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {note}")
                self.status.set("تمت إضافة ملاحظة محلية")
            win.destroy()
        ttk.Button(win, text="إضافة", command=save).pack(pady=10)

    def clear(self):
        self.text.delete("1.0", "end")
        self.current_path = None
        self.data = None
        self.status.set("تم مسح العرض")

if __name__ == "__main__":
    app = SafeDiscordTool()
    app.mainloop()
