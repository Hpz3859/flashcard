import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import json
import uuid
import re
import random

# --- 全局配置与色彩主题 ---
DB_FILE = 'flashcards.json'
GREEN_THRESHOLD = 9

class Theme:
    BG_PRIMARY = '#FCFAF2'
    BG_SECONDARY = '#DCE1B7'
    ACCENT_GREEN = '#502A24'
    ACCENT_GREEN_DARK = "#FBB7B7"
    TEXT_PRIMARY = '#502A24'
    TEXT_SECONDARY = '#FFFFFF'
    BORDER_COLOR = '#D1D1D1'
    HIGHLIGHT_COLOR = '#F0E68C' # 拖拽时高亮颜色

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("闪卡抽背软件")
        self.root.geometry("450x350")
        self.root.configure(bg=Theme.BG_PRIMARY)

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('.', background=Theme.BG_PRIMARY, foreground=Theme.TEXT_PRIMARY, font=('Helvetica', 11))
        self.style.configure('TFrame', background=Theme.BG_PRIMARY)
        self.style.configure('TLabel', background=Theme.BG_PRIMARY, foreground=Theme.TEXT_PRIMARY)
        # Note: TTK a/ `clam` a°a/e| a-ae-2a(c)a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a-2 a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?- a,?ae-|aa-a- a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?a$?- a| a| a| a| a| a|
        self.style.configure('TButton', background=Theme.BG_SECONDARY, foreground=Theme.ACCENT_GREEN, font=('KaiTi', 14, 'bold'), borderwidth=0, padding=(10, 8))
        self.style.map('TButton', background=[('active', Theme.ACCENT_GREEN_DARK), ('hover', Theme.ACCENT_GREEN_DARK)])
        
        self.recitation_settings = {'font_family': 'KaiTi', 'font_size': 22, 'paragraph_spacing': 10, 'line_spacing': 10}
        self.cards = self.load_cards()

        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(expand=True, fill="both")
        btn_create = ttk.Button(main_frame, text="制作新闪卡", command=lambda: self.open_create_window(self.root), width=20)
        btn_create.pack(pady=15, ipady=5)
        btn_list = ttk.Button(main_frame, text="闪卡列表与背诵", command=self.open_list_window, width=20)
        btn_list.pack(pady=15, ipady=5)

    def load_cards(self):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): return []

    def save_cards(self):
        try:
            with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(self.cards, f, ensure_ascii=False, indent=4)
        except Exception as e: messagebox.showerror("保存失败", f"无法保存文件: {e}")

    def find_card_by_id(self, card_id):
        for card in self.cards:
            if card.get('id') == card_id: return card
        return None

    def open_create_window(self, parent_win, card_id=None, prefilled_tags=None):
        create_win = CreateCardWindow(self, parent_win, card_id=card_id, prefilled_tags=prefilled_tags)
        parent_win.wait_window(create_win)

    def open_list_window(self): self.cards = self.load_cards(); CardListWindow(self)
    def open_recitation_window(self, card_ids):
        cards_to_recite = [self.find_card_by_id(cid) for cid in card_ids if self.find_card_by_id(cid)]
        if cards_to_recite: RecitationWindow(self, cards_to_recite)
        else: messagebox.showinfo("提示", "没有可供背诵的闪卡。")


class CreateCardWindow(tk.Toplevel):
    def __init__(self, app, parent, card_id=None, prefilled_tags=None):
        super().__init__(parent)
        self.app = app; self.card_id = card_id
        self.configure(bg=Theme.BG_PRIMARY)
        self.is_edit_mode = card_id is not None
        title = "修改闪卡" if self.is_edit_mode else "制作闪卡"
        self.title(title); self.geometry("800x600")
        self.transient(parent); self.grab_set()

        main_frame = ttk.Frame(self, padding=20); main_frame.pack(fill="both", expand=True)
        ttk.Label(main_frame, text="闪卡名字:", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.name_entry = ttk.Entry(main_frame, width=80, font=('Helvetica', 11)); self.name_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew", columnspan=2)
        ttk.Label(main_frame, text="闪卡归档:", font=('Helvetica', 11, 'bold')).grid(row=1, column=0, padx=10, pady=8, sticky="w")
        
        self.tags_entry = ttk.Combobox(main_frame, width=80, font=('Helvetica', 11))
        self.tags_entry.grid(row=1, column=1, padx=10, pady=8, sticky="ew", columnspan=2)

        self.tag_tree = self._build_tag_tree()
        self.current_tag_prefix = "" 
        self.tags_entry.bind('<KeyRelease>', self._update_tag_suggestions)
        self.tags_entry.bind('<<ComboboxSelected>>', self._on_tag_select)
        
        ttk.Label(main_frame, text="例如: #主tag;##次tag;###子tag", foreground="gray").grid(row=2, column=1, padx=10, sticky="w")
        ttk.Label(main_frame, text="闪卡内容:", font=('Helvetica', 11, 'bold')).grid(row=3, column=0, padx=10, pady=8, sticky="nw")
        self.content_text = tk.Text(main_frame, wrap="word", height=20, font=("Helvetica", 11), relief="solid", borderwidth=1); self.content_text.grid(row=3, column=1, rowspan=3, padx=10, pady=8, sticky="nsew", columnspan=2)
        
        button_frame = ttk.Frame(main_frame); button_frame.grid(row=6, column=1, columnspan=2, sticky="ew", pady=10, padx=10)
        
        btn_parse = ttk.Button(button_frame, text="填充当前表单", command=self.parse_from_content); btn_parse.pack(side="left")
        btn_bulk_parse = ttk.Button(button_frame, text="批量解析 & 保存", command=self.bulk_parse_and_save); btn_bulk_parse.pack(side="left", padx=10)
        btn_save = ttk.Button(button_frame, text="保存", command=self.save_card); btn_save.pack(side="right")
        
        main_frame.grid_columnconfigure(1, weight=1); main_frame.grid_rowconfigure(4, weight=1)
        if self.is_edit_mode:
            card = self.app.find_card_by_id(self.card_id)
            if card: self.name_entry.insert(0, card.get('name', '')); self.tags_entry.set(card.get('tags_string', '')); self.content_text.insert("1.0", card.get('content', ''))
        elif prefilled_tags:
            self.tags_entry.set(prefilled_tags)
        
        if not self.is_edit_mode:
            self._update_tag_suggestions()

    def _build_tag_tree(self):
        tree = {}
        for card in self.app.cards:
            tags_string = card.get('tags_string', '')
            if not tags_string: continue
            
            parts = [p.strip() for p in tags_string.split(';') if p.strip()]
            current_level = tree
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        return tree

    def _update_tag_suggestions(self, event=None):
        if event and event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'KP_Enter'):
            return

        current_text = self.tags_entry.get()
        path_parts = [p.strip() for p in current_text.split(';') if p.strip()]
        
        is_starting_new_tag = current_text.endswith(';') or not current_text

        if is_starting_new_tag:
            prefix_parts = path_parts
            typing_part = ""
        else:
            prefix_parts = path_parts[:-1]
            typing_part = path_parts[-1]

        self.current_tag_prefix = ';'.join(prefix_parts)

        current_level = self.tag_tree
        try:
            for part in prefix_parts:
                current_level = current_level[part]
        except KeyError:
            current_level = {}

        suggestions = [tag for tag in current_level.keys() if tag.startswith(typing_part)]
        
        if suggestions:
            self.tags_entry['values'] = suggestions
        else:
            self.tags_entry['values'] = []

    def _on_tag_select(self, event=None):
        selection = self.tags_entry.get()
        
        if self.current_tag_prefix:
            new_text = f"{self.current_tag_prefix};{selection};"
        else:
            new_text = f"{selection};"
        
        self.tags_entry.set(new_text)
        self.tags_entry.icursor(tk.END)
        self.tags_entry.focus()
        self._update_tag_suggestions()
        self.after(50, lambda: self.tags_entry.event_generate('<Down>'))

    def clear_fields(self):
        self.name_entry.delete(0, tk.END); self.tags_entry.set(''); self.content_text.delete("1.0", tk.END)
        self.name_entry.focus_set()

    def parse_from_content(self):
        content = self.content_text.get("1.0", tk.END); name_match = re.search(r'n\s*:(.*?)\n', content); tags_match = re.search(r't\s*:(.*?)(?:\n|$)', content, re.DOTALL); content_match = re.search(r'c\s*:\s*\{(.*?)\}', content, re.DOTALL)
        if name_match and tags_match and content_match: self.name_entry.delete(0, tk.END); self.name_entry.insert(0, name_match.group(1).strip()); self.tags_entry.set(tags_match.group(1).strip()); self.content_text.delete("1.0", tk.END); self.content_text.insert("1.0", content_match.group(1).strip()); messagebox.showinfo("成功", "已成功解析并填充字段！")
        else: messagebox.showwarning("解析失败", "未找到符合 'n:', 'c:{}', 't:' 格式的内容。")

    def save_card(self):
        name = self.name_entry.get().strip(); tags_string = self.tags_entry.get().strip(); content = self.content_text.get("1.0", tk.END).strip()
        if not name or not content: messagebox.showerror("错误", "闪卡名字和内容不能为空！"); return
        
        if self.is_edit_mode:
            card = self.app.find_card_by_id(self.card_id)
            if card: card['name'] = name; card['tags_string'] = tags_string; card['content'] = content
            messagebox.showinfo("成功", "修改已保存！")
        else:
            new_card = {"id": str(uuid.uuid4()), "name": name, "tags_string": tags_string, "content": content, "recitation_count": 0}; self.app.cards.append(new_card)
            messagebox.showinfo("成功", "新闪卡已保存！")
        
        self.app.save_cards(); self.app.root.event_generate("<<ListShouldRefresh>>")
        if self.is_edit_mode: self.destroy()
        else: self.clear_fields()

    def bulk_parse_and_save(self):
        full_text = self.content_text.get("1.0", tk.END).strip()
        if not full_text: messagebox.showwarning("提示", "内容区为空，无法解析。"); return
        
        blocks = re.findall(r'n:.*?(?=\n\s*n:|\Z)', full_text, re.DOTALL)
        if not blocks:
            messagebox.showwarning("解析失败", "未找到任何符合 'n:' 格式的卡片块。\n请确保每个卡片都以 'n:' 开头。"); return
            
        newly_created_cards = []
        for i, block in enumerate(blocks):
            name_match = re.search(r'n\s*:\s*(.*?)(?=\n|$)', block, re.DOTALL); content_match = re.search(r'c\s*:\s*\{(.*?)\}', block, re.DOTALL); tags_match = re.search(r't\s*:\s*(.*?)(?=\n|$)', block, re.DOTALL)
            if name_match and content_match and tags_match:
                name = name_match.group(1).strip(); content = content_match.group(1).strip(); tags = tags_match.group(1).strip()
                response = messagebox.askyesnocancel(title=f"确认保存卡片 ({i+1}/{len(blocks)})", message=f"即将保存以下闪卡：\n\n名称: {name}\n标签: {tags}\n内容: {content[:50]}...\n\n是否保存？\n(选择“否”跳过，选择“取消”中止)", icon='question')
                if response is True:
                    new_card = {"id": str(uuid.uuid4()), "name": name, "tags_string": tags, "content": content, "recitation_count": 0}
                    newly_created_cards.append(new_card)
                elif response is None:
                    messagebox.showinfo("操作中止", f"批量操作已中止。本次已成功解析 {len(newly_created_cards)} 张卡片。"); break
            else:
                response = messagebox.askyesnocancel(title="格式错误", message=f"第 {i + 1} 个卡片块格式不正确，无法解析。\n\n内容预览:\n{block[:100]}...\n\n是否继续解析下一个？", icon='warning')
                if response is None or response is False:
                    messagebox.showinfo("操作中止", f"批量操作已中止。本次已成功解析 {len(newly_created_cards)} 张卡片。"); break

        if newly_created_cards: self.app.cards.extend(newly_created_cards); self.app.save_cards(); self.app.root.event_generate("<<ListShouldRefresh>>")
        messagebox.showinfo("批量操作完成", f"全部完成！共成功保存了 {len(newly_created_cards)} 张新闪卡。")
        self.clear_fields()


class CardListWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root); self.app = app; self.title("闪卡列表"); self.geometry("900x700"); self.configure(bg=Theme.BG_SECONDARY)
        self.app.root.bind("<<ListShouldRefresh>>", lambda e: self.populate_tree()); self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        top_controls_frame = ttk.Frame(self, padding="10"); top_controls_frame.pack(fill="x")
        
        filter_frame = ttk.Frame(top_controls_frame); filter_frame.pack(side="left", fill="x", expand=True)
        ttk.Label(filter_frame, text="筛选:").pack(side="left", padx=(0, 5))
        self.filter_field = ttk.Combobox(filter_frame, values=["背诵次数"], state="readonly", width=10); self.filter_field.set("背诵次数"); self.filter_field.pack(side="left", padx=(0,2))
        self.filter_op = ttk.Combobox(filter_frame, values=["<", ">", "=", "!="], state="readonly", width=3); self.filter_op.set("<"); self.filter_op.pack(side="left", padx=(0,2))
        self.filter_value = ttk.Entry(filter_frame, width=6); self.filter_value.pack(side="left", padx=(0,5))
        btn_apply_filter = ttk.Button(filter_frame, text="应用", command=self.apply_filter, width=5); btn_apply_filter.pack(side="left")
        btn_clear_filter = ttk.Button(filter_frame, text="清除", command=self.clear_filter, width=5); btn_clear_filter.pack(side="left", padx=(2,10))

        ttk.Label(filter_frame, text="显示层级:").pack(side="left", padx=(10, 5))
        self.level_var = tk.StringVar(value="全部展开"); level_combo = ttk.Combobox(filter_frame, textvariable=self.level_var, values=["全部展开", "展开到一级", "展开到二级"], state="readonly", width=12); level_combo.pack(side="left")
        btn_apply_level = ttk.Button(filter_frame, text="应用层级", command=self.apply_expansion_level); btn_apply_level.pack(side="left", padx=5)

        style = ttk.Style()
        style.configure('Treeview', rowheight=28, font=('KaiTi', 14), background=Theme.BG_PRIMARY, fieldbackground=Theme.BG_PRIMARY, foreground=Theme.TEXT_PRIMARY)
        style.configure('Treeview.Heading', font=('KaiTi', 14, 'bold'), background=Theme.ACCENT_GREEN, foreground=Theme.TEXT_SECONDARY, relief="flat")
        style.map('Treeview.Heading', background=[('active', Theme.ACCENT_GREEN_DARK)])
        style.map('Treeview', background=[('selected', '#DCE1B7')])
        
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(main_frame, columns=("check", "count"), show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="名称"); self.tree.heading("check", text="☐", anchor="center"); self.tree.heading("count", text="背诵次数")
        self.tree.column("#0", width=500); self.tree.column("check", width=40, anchor="center"); self.tree.column("count", width=100, anchor="center"); self.tree.pack(side="left", fill="both", expand=True)
        
        self.all_selected = False
        self.checked_states = {}
        self.tree.bind("<ButtonPress-1>", self.start_drag)
        self.tree.bind("<Button-1>", self.on_tree_click, add="+")
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<B1-Motion>", self.on_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_drop)
        self.dragged_items = []
        self.last_highlighted_item = None
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview); scrollbar.pack(side="right", fill="y"); self.tree.configure(yscrollcommand=scrollbar.set)
        btn_frame = ttk.Frame(self, padding="10"); btn_frame.pack(fill="x")
        btn_recite = ttk.Button(btn_frame, text="背诵选中", command=self.recite_selected); btn_recite.pack(side="left", padx=5)
        self.populate_tree()

    def apply_filter(self):
        field = self.filter_field.get(); op = self.filter_op.get(); value_str = self.filter_value.get()
        if not value_str: messagebox.showwarning("提示", "筛选值不能为空。"); return
        try: value = int(value_str)
        except ValueError: messagebox.showerror("错误", "筛选值必须是数字。"); return
        def filter_logic(card):
            card_val = card.get('recitation_count', 0)
            if op == "<": return card_val < value
            if op == ">": return card_val > value
            if op == "=": return card_val == value
            if op == "!=": return card_val != value
            return False
        self.populate_tree(filter_func=filter_logic)

    def clear_filter(self):
        self.filter_value.delete(0, tk.END); self.populate_tree()

    def apply_expansion_level(self):
        level_str = self.level_var.get()
        all_items = self._get_all_item_ids()
        for item in all_items: self.tree.item(item, open=False)
        if level_str == "全部展开":
            for item in all_items: self.tree.item(item, open=True)
            return
        level_map = {"展开到一级": 1, "展开到二级": 2}
        target_level = level_map.get(level_str, 1)
        current_level_items = self.tree.get_children("")
        for _ in range(target_level):
            next_level_items = []
            for item in current_level_items:
                self.tree.item(item, open=True)
                next_level_items.extend(self.tree.get_children(item))
            current_level_items = next_level_items
            if not current_level_items: break

    def start_drag(self, event):
        self.dragged_items = []

    def on_drag(self, event):
        if not self.dragged_items and self.tree.identify_row(event.y):
            self.dragged_items = self.tree.selection()
        if not self.dragged_items: return
        
        self.tree.config(cursor="fleur")
        if self.last_highlighted_item and self.tree.exists(self.last_highlighted_item): self.tree.tag_remove('highlight', self.last_highlighted_item)
        drop_target = self.tree.identify_row(event.y)
        if drop_target and drop_target not in self.dragged_items:
            self.tree.tag_add('highlight', drop_target)
            self.last_highlighted_item = drop_target
        else: self.last_highlighted_item = None

    def on_drop(self, event):
        self.tree.config(cursor="")
        if self.last_highlighted_item and self.tree.exists(self.last_highlighted_item): self.tree.tag_remove('highlight', self.last_highlighted_item)
        if not self.dragged_items: return
        drop_target = self.tree.identify_row(event.y)
        if drop_target not in self.dragged_items: self.move_items(self.dragged_items, drop_target)
        self.dragged_items = []

    def _card_matches_prefix(self, card_tags, prefix):
        return card_tags == prefix or card_tags.startswith(prefix + ';')

    def move_items(self, items_to_move, drop_target_id):
        if self.app.find_card_by_id(drop_target_id): new_parent_id = self.tree.parent(drop_target_id)
        else: new_parent_id = drop_target_id
        
        for item_id in items_to_move:
            current = new_parent_id
            while current:
                if current == item_id: messagebox.showwarning("非法操作", "不能将一个标签移动到它自己的子标签下。"); return
                current = self.tree.parent(current)

        new_parent_path = new_parent_id.replace('/', ';') if new_parent_id else ""
        
        for item_id in items_to_move:
            moved_card = self.app.find_card_by_id(item_id)
            if moved_card: moved_card['tags_string'] = new_parent_path
            else:
                old_tag_path_prefix = item_id.replace('/', ';')
                dragged_tag_text = self.tree.item(item_id, 'text')
                new_tag_path_prefix = f"{new_parent_path};{dragged_tag_text}" if new_parent_path else dragged_tag_text
                
                for card in self.app.cards:
                    if self._card_matches_prefix(card.get('tags_string', ''), old_tag_path_prefix):
                        rest_of_tags = card.get('tags_string', '')[len(old_tag_path_prefix):]
                        card['tags_string'] = new_tag_path_prefix + rest_of_tags

        self.app.save_cards(); self.populate_tree()

    def show_context_menu(self, event):
        selection = self.tree.selection()
        item_id = self.tree.identify_row(event.y)

        if item_id not in selection:
            self.tree.selection_set(item_id if item_id else [])
        
        final_selection = self.tree.selection()
        
        menu = tk.Menu(self.tree, tearoff=0)
        
        if len(final_selection) == 1:
            single_item_id = final_selection[0]
            is_card = self.app.find_card_by_id(single_item_id)
            if is_card:
                menu.add_command(label="修改闪卡", command=lambda: self.app.open_create_window(self, single_item_id))
            else:
                menu.add_command(label="在此tag下创建闪卡", command=lambda: self.create_card_under_tag(single_item_id))
                menu.add_command(label="增加次级标签", command=lambda: self.add_sub_tag(single_item_id))
                menu.add_command(label="重命名标签", command=lambda: self.rename_tag(single_item_id))

        if final_selection:
            if menu.index('end') is not None:
                menu.add_separator()
            menu.add_command(label="删除选中", command=self.delete_selected_items)
        
        if not final_selection:
            menu.add_command(label="增加主标签", command=self.add_main_tag)

        menu.post(event.x_root, event.y_root)

    def create_card_under_tag(self, tag_id):
        tags_string = tag_id.replace('/', ';')
        self.app.open_create_window(self, prefilled_tags=tags_string)

    def delete_selected_items(self):
        selection = self.tree.selection()
        if not selection: return

        cards_to_delete_ids = set()
        tags_to_delete_prefixes = []

        for item_id in selection:
            if self.app.find_card_by_id(item_id):
                cards_to_delete_ids.add(item_id)
            else:
                tags_to_delete_prefixes.append(item_id.replace('/', ';'))

        num_cards = len(cards_to_delete_ids)
        num_tags = len(tags_to_delete_prefixes)
        msg_parts = []
        if num_cards > 0: msg_parts.append(f"{num_cards} 张闪卡")
        if num_tags > 0: msg_parts.append(f"{num_tags} 个标签 (及其内容)")
        
        if not msg_parts: return

        confirm_msg = f"确定要删除选中的 { ' 和 '.join(msg_parts) } 吗？\n此操作不可撤销。"

        if messagebox.askyesno("确认删除", confirm_msg, icon='warning'):
            cards_to_keep = []
            for card in self.app.cards:
                if card['id'] in cards_to_delete_ids:
                    continue

                is_under_deleted_tag = False
                card_tags = card.get('tags_string', '')
                for prefix in tags_to_delete_prefixes:
                    if self._card_matches_prefix(card_tags, prefix):
                        is_under_deleted_tag = True
                        break
                
                if is_under_deleted_tag:
                    continue
                
                cards_to_keep.append(card)
            
            self.app.cards = cards_to_keep
            self.app.save_cards()
            self.populate_tree()

    def _add_placeholder_card(self, tags_string):
        placeholder = {"id": str(uuid.uuid4()), "name": "__PLACEHOLDER__", "tags_string": tags_string, "content": "", "recitation_count": -1}
        self.app.cards.append(placeholder)
        self.app.save_cards(); self.populate_tree()

    def add_main_tag(self):
        name = simpledialog.askstring("新主标签", "请输入主标签名称:", parent=self)
        if name and name.strip(): self._add_placeholder_card(f"#{name.strip()}")

    def add_sub_tag(self, parent_item_id):
        name = simpledialog.askstring("新次级标签", f"在 '{self.tree.item(parent_item_id, 'text')}' 下创建新标签:", parent=self)
        if name and name.strip():
            parent_path = parent_item_id.replace('/', ';')
            parent_level = self.tree.item(parent_item_id, 'text').count('#')
            new_tag = '#' * (parent_level + 1) + name.strip()
            self._add_placeholder_card(f"{parent_path};{new_tag}")

    def rename_tag(self, item_id):
        old_tag_text = self.tree.item(item_id, "text")
        initial_name = old_tag_text.lstrip('#')
        
        new_name_raw = simpledialog.askstring("重命名标签", "请输入新的标签名称:", initialvalue=initial_name, parent=self)
        
        if not new_name_raw or not new_name_raw.strip():
            return
            
        new_name = new_name_raw.strip().lstrip('#')
        
        level = old_tag_text.count('#')
        new_tag_text = ('#' * level) + new_name

        if new_tag_text != old_tag_text:
            old_path_prefix = item_id.replace('/', ';')
            
            parent_iid = self.tree.parent(item_id)
            if parent_iid:
                parent_path = parent_iid.replace('/', ';')
                new_path_prefix = f"{parent_path};{new_tag_text}"
            else:
                new_path_prefix = new_tag_text
                
            for card in self.app.cards:
                tags = card.get('tags_string', '')
                if self._card_matches_prefix(tags, old_path_prefix):
                    rest_of_tags = tags[len(old_path_prefix):]
                    card['tags_string'] = new_path_prefix + rest_of_tags
                    
            self.app.save_cards()
            self.populate_tree()
            
    def on_tree_click(self, event):
        if self.dragged_items: return
        region = self.tree.identify("region", event.x, event.y)
        column = self.tree.identify_column(event.x)
        if region == "heading" and column == "#1":
            self.toggle_select_all(); return
        item_id = self.tree.identify_row(event.y)
        if not item_id: self.tree.selection_set([]); return
        if region == "cell" and column == "#1": self.toggle_check(item_id)

    def _get_all_item_ids(self):
        all_items = []
        def getter(parent):
            for child in self.tree.get_children(parent):
                all_items.append(child)
                getter(child)
        getter("")
        return all_items

    def _update_select_all_header(self):
        all_items = self._get_all_item_ids()
        if not all_items: self.all_selected = False
        else: self.all_selected = all(self.checked_states.get(item, False) for item in all_items)
        self.tree.heading("check", text='☑' if self.all_selected else '☐')

    def toggle_select_all(self):
        self.all_selected = not self.all_selected
        new_state_char = '☑' if self.all_selected else '☐'
        self.tree.heading("check", text=new_state_char)
        for item_id in self._get_all_item_ids():
            self.checked_states[item_id] = self.all_selected
            self.tree.set(item_id, "check", new_state_char)
            
    def toggle_check(self, item_id):
        if not item_id: return
        new_state = not self.checked_states.get(item_id, False)
        self.update_children_check_state(item_id, new_state)
        self.update_parent_check_state(item_id)
        self._update_select_all_header()

    def update_children_check_state(self, item_id, state):
        self.checked_states[item_id] = state; self.tree.set(item_id, "check", '☑' if state else '☐')
        for child_id in self.tree.get_children(item_id): self.update_children_check_state(child_id, state)

    def update_parent_check_state(self, item_id):
        parent_id = self.tree.parent(item_id)
        if not parent_id: return
        all_siblings_checked = all(self.checked_states.get(sid, False) for sid in self.tree.get_children(parent_id))
        self.checked_states[parent_id] = all_siblings_checked; self.tree.set(parent_id, "check", '☑' if all_siblings_checked else '☐')
        self.update_parent_check_state(parent_id)
        
    def on_close(self): self.app.root.unbind("<<ListShouldRefresh>>"); self.destroy()

    def populate_tree(self, filter_func=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        self.tree.tag_configure('green', foreground='#207178'); self.tree.tag_configure('highlight', background=Theme.HIGHLIGHT_COLOR)
        self.checked_states = {}
        tags_map = {}; unclassified_cards = []
        
        cards_to_display = self.app.cards
        if filter_func: cards_to_display = [card for card in self.app.cards if filter_func(card)]

        def parse_tags(tags_str):
            if not tags_str.strip(): return []
            tags = [t.strip() for t in tags_str.split(';') if t.strip()]; parsed = []
            for tag in tags:
                if '#' in tag: level = tag.count('#'); name = tag.lstrip('#'); parsed.append((level, name, tag))
            return sorted(parsed, key=lambda x: x[0])

        for card in cards_to_display:
            parsed_tags = parse_tags(card.get('tags_string', ''))
            if not parsed_tags:
                if card.get('name') != "__PLACEHOLDER__": unclassified_cards.append(card)
                continue
                
            parent_iid = ""; current_path = ""
            for level, name, original_tag in parsed_tags:
                path_part = original_tag; new_path = f"{current_path}/{path_part}" if current_path else path_part
                if new_path not in tags_map:
                    node_id = self.tree.insert(parent_iid, 'end', text=original_tag, open=True, iid=new_path); self.tree.set(node_id, "check", '☐'); tags_map[new_path] = node_id
                parent_iid = tags_map[new_path]; current_path = new_path
            
            if card.get('name') != "__PLACEHOLDER__":
                count = card.get('recitation_count', 0); tag_style = 'green' if count > GREEN_THRESHOLD else ''
                self.tree.insert(parent_iid, 'end', text=card['name'], values=('', count,), iid=card['id'], tags=(tag_style,)); self.tree.set(card['id'], "check", '☐')

        if unclassified_cards:
            unclassified_id = self.tree.insert("", 'end', text="[未分类]", open=True, iid="[unclassified]"); self.tree.set(unclassified_id, "check", '☐')
            for card in unclassified_cards:
                count = card.get('recitation_count', 0); tag_style = 'green' if count > GREEN_THRESHOLD else ''
                self.tree.insert(unclassified_id, 'end', text=card['name'], values=('', count,), iid=card['id'], tags=(tag_style,)); self.tree.set(card['id'], "check", '☐')
        self.apply_expansion_level()
        self._update_select_all_header()

    def get_checked_card_ids(self): return [item_id for item_id, is_checked in self.checked_states.items() if is_checked and self.app.find_card_by_id(item_id)]

    def recite_selected(self):
        card_ids_to_recite = list(dict.fromkeys(self.get_checked_card_ids()))
        if not card_ids_to_recite: messagebox.showwarning("提示", "请先勾选需要背诵的闪卡。"); return
        self.app.open_recitation_window(card_ids_to_recite); self.after(200, self.populate_tree)

class RecitationWindow(tk.Toplevel):
    def __init__(self, app, cards_to_recite):
        super().__init__(app.root)
        self.app = app; self.original_cards = cards_to_recite; self.cards = list(self.original_cards); self.current_index = 0
        self.title("背诵闪卡"); self.geometry("800x600"); self.configure(bg=Theme.BG_PRIMARY)
        bottom_frame = ttk.Frame(self, padding=10); bottom_frame.pack(side="bottom", fill="x", pady=5)
        card_frame = tk.Frame(self, bg=Theme.BG_PRIMARY, relief="raised", borderwidth=1, padx=20, pady=20); card_frame.pack(side="top", fill="both", expand=True, padx=30, pady=(20, 10))
        self.card_name_label = ttk.Label(card_frame, text="闪卡名字", style="Card.TLabel", font=("Helvetica", 16, "bold")); self.card_name_label.pack(side="top", anchor="w", pady=(0, 15))
        self.content_text = tk.Text(card_frame, wrap="word", relief="flat", borderwidth=0, bg=Theme.BG_PRIMARY); self.content_text.pack(fill="both", expand=True); self.content_text.config(state="disabled")
        order_label = ttk.Label(bottom_frame, text="顺序:"); order_label.pack(side="left", padx=(20, 5))
        self.order_var = tk.StringVar(value="顺序"); order_menu = ttk.Combobox(bottom_frame, textvariable=self.order_var, values=["顺序", "随机", "倒序", "按背诵次数倒序"], state="readonly", width=15); order_menu.pack(side="left"); order_menu.bind("<<ComboboxSelected>>", self.change_order)
        self.progress_label = ttk.Label(bottom_frame, text=""); self.progress_label.pack(side="left", padx=20)
        right_button_frame = ttk.Frame(bottom_frame); right_button_frame.pack(side="right", padx=20)
        modify_btn = ttk.Button(right_button_frame, text="修改 ✍️", command=self.modify_current_card, width=8); modify_btn.pack(side="left", padx=10)
        settings_btn = ttk.Button(right_button_frame, text="设置 ⚙️", command=self.open_settings_dialog, width=8); settings_btn.pack(side="left", padx=10)
        next_btn = ttk.Button(right_button_frame, text="下一个 →", command=self.next_card); next_btn.pack(side="left")
        self.update_text_styles(); self.display_card()

    def modify_current_card(self):
        if not self.cards: return
        current_card_id = self.cards[self.current_index]['id']
        self.app.open_create_window(self, card_id=current_card_id)
        updated_card_data = self.app.find_card_by_id(current_card_id)
        if updated_card_data:
            self.cards[self.current_index] = updated_card_data.copy()
            for i, card in enumerate(self.original_cards):
                if card['id'] == current_card_id: self.original_cards[i] = updated_card_data.copy(); break
        self.display_card()
        
    def update_text_styles(self):
        settings = self.app.recitation_settings; base_family = settings['font_family']; base_size = settings['font_size']
        try: self.fonts = {'card_body': font.Font(family=base_family, size=base_size),'card_h1': font.Font(family=base_family, size=int(base_size * 1.5), weight="bold"),'card_h2': font.Font(family=base_family, size=int(base_size * 1.2), weight="bold"),'card_bold': font.Font(family=base_family, size=base_size, weight="bold")}
        except tk.TclError: self.fonts = {'card_body': font.Font(size=base_size),'card_h1': font.Font(size=int(base_size * 1.5), weight="bold"),'card_h2': font.Font(size=int(base_size * 1.2), weight="bold"),'card_bold': font.Font(size=base_size, weight="bold")}
        self.content_text.config(font=self.fonts['card_body'], spacing2=settings['line_spacing'], spacing3=settings['paragraph_spacing'])
        self.app.style.configure("Card.TLabel", background=Theme.BG_SECONDARY)
        self.content_text.tag_configure("h1", font=self.fonts['card_h1'], spacing3=int(settings['paragraph_spacing'] * 1.5)); self.content_text.tag_configure("h2", font=self.fonts['card_h2'], spacing3=int(settings['paragraph_spacing'] * 1.2)); self.content_text.tag_configure("list", lmargin1=25, lmargin2=25); self.content_text.tag_configure("bold", font=self.fonts['card_bold']); self.content_text.tag_configure("cloze_hidden", underline=True, background="#f0f0f0", relief="raised"); self.content_text.tag_configure("cloze_revealed", background="#E0F2D6", relief="flat"); self.content_text.tag_bind("cloze", "<Button-1>", self.toggle_hidden_text)
        if hasattr(self, 'cards') and self.cards: self.render_content(self.cards[self.current_index].get('content', ''))
        
    def open_settings_dialog(self): SettingsDialog(self, self.app)
    
    def change_order(self, event=None):
        order = self.order_var.get(); self.current_index = 0
        if order == "顺序": self.cards = list(self.original_cards)
        elif order == "随机": self.cards = list(self.original_cards); random.shuffle(self.cards)
        elif order == "倒序": self.cards = list(reversed(self.original_cards))
        elif order == "按背诵次数倒序":
            self.cards = sorted(list(self.original_cards), key=lambda c: c.get('recitation_count', 0), reverse=True)
        self.display_card()

    def display_card(self):
        if not self.cards: self.card_name_label.config(text="没有卡片"); self.content_text.config(state="normal"); self.content_text.delete("1.0", tk.END); self.content_text.config(state="disabled"); return
        card = self.cards[self.current_index]
        db_card = self.app.find_card_by_id(card['id'])
        if db_card: db_card['recitation_count'] = db_card.get('recitation_count', 0) + 1
        self.app.save_cards()
        self.card_name_label.config(text=card['name']); self.progress_label.config(text=f"{self.current_index + 1} / {len(self.cards)}")
        self.render_content(card.get('content', ''))

    def render_content(self, raw_content):
        self.content_text.config(state="normal"); self.content_text.delete("1.0", tk.END); self.hidden_map = {}; cloze_id_counter = 0
        def replace_cloze(match):
            nonlocal cloze_id_counter; key = f"%%CLOZE_{cloze_id_counter}%%"; self.hidden_map[key] = match.group(1); cloze_id_counter += 1; return key
        content = re.sub(r'\[(.*?)\]', replace_cloze, raw_content)
        for line in content.split('\n'):
            line_tags = []
            if line.startswith("# "): line = line[2:]; line_tags.append("h1")
            elif line.startswith("## "): line = line[3:]; line_tags.append("h2")
            elif line.startswith("- "): line = "• " + line[2:]; line_tags.append("list")
            parts = re.split(r'(\*\*.*?\*\*|%%CLOZE_\d+%%)', line)
            for part in parts:
                if not part: continue
                current_tags = list(line_tags)
                if part.startswith('**') and part.endswith('**'): current_tags.append('bold'); self.content_text.insert(tk.END, part[2:-2], tuple(current_tags))
                elif part.startswith('%%CLOZE_'):
                    hidden_text = self.hidden_map[part]; placeholder = "  " + "\u00A0" * len(hidden_text) + "  "; cloze_id = part.split('_')[1].strip('%'); unique_tag = f"cloze_id_{cloze_id}"
                    self.content_text.insert(tk.END, placeholder, ("cloze", unique_tag, "cloze_hidden"))
                else: self.content_text.insert(tk.END, part, tuple(current_tags))
            self.content_text.insert(tk.END, '\n')
        self.content_text.config(state="disabled")

    def toggle_hidden_text(self, event):
        widget = event.widget; index = widget.index(f"@{event.x},{event.y}"); tags_at_index = widget.tag_names(index); unique_cloze_tag = None
        for tag in tags_at_index:
            if tag.startswith("cloze_id_"): unique_cloze_tag = tag; break
        if not unique_cloze_tag: return
        is_hidden = "cloze_hidden" in tags_at_index
        cloze_id = unique_cloze_tag.split('_')[-1]; placeholder_key = f"%%CLOZE_{cloze_id}%%"; original_text = self.hidden_map[placeholder_key]
        start, end = widget.tag_ranges(unique_cloze_tag); widget.config(state="normal"); widget.delete(start, end)
        if is_hidden: widget.insert(start, f" {original_text} ", ("cloze", unique_cloze_tag, "cloze_revealed"))
        else: placeholder = "  " + "\u00A0" * len(original_text) + "  "; widget.insert(start, placeholder, ("cloze", unique_cloze_tag, "cloze_hidden"))
        widget.config(state="disabled")

    def next_card(self):
        if self.current_index < len(self.cards) - 1: self.current_index += 1; self.display_card()
        else: messagebox.showinfo("完成", "恭喜！您已背诵完本轮所有闪卡。"); self.destroy()

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent; self.app = app
        self.title("显示设置"); self.geometry("420x350"); self.transient(parent); self.grab_set(); self.configure(bg=Theme.BG_PRIMARY)
        main_frame = ttk.Frame(self, padding=20); main_frame.pack(fill="both", expand=True)
        settings = self.app.recitation_settings
        
        self.font_family_var = tk.StringVar()
        self.font_size_var = tk.IntVar(value=settings['font_size']); self.paragraph_spacing_var = tk.IntVar(value=settings['paragraph_spacing']); self.line_spacing_var = tk.IntVar(value=settings['line_spacing'])
        self.font_map = {'宋体': 'SimSun','楷体': 'KaiTi','黑体': 'SimHei','微软雅黑': 'Microsoft YaHei','Times New Roman': 'Times New Roman','Arial': 'Arial'}
        self.reverse_font_map = {v: k for k, v in self.font_map.items()}
        
        ttk.Label(main_frame, text="字体选择:").grid(row=0, column=0, sticky="w", pady=5)
        font_combo = ttk.Combobox(main_frame, textvariable=self.font_family_var, values=list(self.font_map.keys()), state="readonly")
        
        current_font = settings['font_family']
        font_to_display = self.reverse_font_map.get(current_font, '楷体')
        
        self.font_family_var.set(font_to_display)
        font_combo.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)

        ttk.Label(main_frame, text="字体大小:").grid(row=1, column=0, sticky="w", pady=10)
        font_size_scale = ttk.Scale(main_frame, from_=10, to=30, orient="horizontal", variable=self.font_size_var, command=lambda s: size_val_label.config(text=f"{int(float(s))}px")); font_size_scale.grid(row=1, column=1, sticky="ew", pady=10)
        size_val_label = ttk.Label(main_frame, text=f"{self.font_size_var.get()}px", width=5); size_val_label.grid(row=1, column=2, sticky="w", padx=5)
        ttk.Label(main_frame, text="行间距:").grid(row=2, column=0, sticky="w", pady=10)
        line_spacing_scale = ttk.Scale(main_frame, from_=0, to=15, orient="horizontal", variable=self.line_spacing_var, command=lambda s: line_val_label.config(text=f"{int(float(s))}px")); line_spacing_scale.grid(row=2, column=1, sticky="ew", pady=10)
        line_val_label = ttk.Label(main_frame, text=f"{self.line_spacing_var.get()}px", width=5); line_val_label.grid(row=2, column=2, sticky="w", padx=5)
        ttk.Label(main_frame, text="段落间距:").grid(row=3, column=0, sticky="w", pady=10)
        paragraph_spacing_scale = ttk.Scale(main_frame, from_=0, to=25, orient="horizontal", variable=self.paragraph_spacing_var, command=lambda s: para_val_label.config(text=f"{int(float(s))}px")); paragraph_spacing_scale.grid(row=3, column=1, sticky="ew", pady=10)
        para_val_label = ttk.Label(main_frame, text=f"{self.paragraph_spacing_var.get()}px", width=5); para_val_label.grid(row=3, column=2, sticky="w", padx=5)
        main_frame.grid_columnconfigure(1, weight=1)
        button_frame = ttk.Frame(self); button_frame.pack(side="bottom", fill="x", padx=20, pady=10)
        apply_btn = ttk.Button(button_frame, text="应用", command=self.apply_settings); apply_btn.pack(side="right", padx=5)
        close_btn = ttk.Button(button_frame, text="关闭", command=self.destroy); close_btn.pack(side="right")

    def apply_settings(self):
        display_name = self.font_family_var.get()
        self.app.recitation_settings['font_family'] = self.font_map.get(display_name, display_name)
        self.app.recitation_settings['font_size'] = self.font_size_var.get()
        self.app.recitation_settings['paragraph_spacing'] = self.paragraph_spacing_var.get()
        self.app.recitation_settings['line_spacing'] = self.line_spacing_var.get()
        self.parent.update_text_styles()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

