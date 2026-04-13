from PySide6.QtWidgets import QMessageBox, QFileDialog, QMenu
from PySide6.QtGui import QAction
from translations import TEXTS
import re

class MenuManager:
    def __init__(self, window):
        self.window = window
        self.current_lang = "ru"
        self.window.current_lang = "ru"
        
        self.setup_menu()
        self.setup_connections()
        
        # Defoult Language
        self.change_language("ru")

    def setup_menu(self):
        menubar = self.window.menuBar()
        lang_menu = menubar.addMenu("Language")
        
        action_ru = QAction("Русский", self.window)
        action_ru.triggered.connect(lambda: self.change_language("ru"))
        lang_menu.addAction(action_ru)

        action_en = QAction("English", self.window)
        action_en.triggered.connect(lambda: self.change_language("en"))
        lang_menu.addAction(action_en)

    def setup_connections(self):
        # Check btns before switch Language
        if hasattr(self.window, 'action_how_it_works'):
            self.window.action_how_it_works.triggered.connect(self.show_instruction)
        if hasattr(self.window, 'action_open'):
            self.window.action_open.triggered.connect(self.open_file)

    def change_language(self, lang_code):
        self.current_lang = lang_code
        self.window.current_lang = lang_code
        
        t = TEXTS[lang_code]

        # 1. Main UI
        self.window.setWindowTitle(t["window_title"])
        self.window.btn_save.setText(t["btn_save"])
        
        # Upd groups
        # Use findChild to find objects even if QUiLoader has not linked them
        box_1 = self.window.findChild(object, "box_1")
        if box_1: box_1.setTitle(t["box_1"])

        box_2 = self.window.findChild(object, "box_2")
        if box_2: box_2.setTitle(t["box_2"])

        box_3 = self.window.findChild(object, "box_3")
        if box_3: box_3.setTitle(t["box_3"])

        box_4 = self.window.findChild(object, "box_4")
        if box_4: box_4.setTitle(t["box_4"])
        
        # 2. Placeholders
        self.window.input_pp.setPlaceholderText(t["ph_1"])
        self.window.input_pm.setPlaceholderText(t["ph_2"])
        self.window.input_mp.setPlaceholderText(t["ph_3"])
        self.window.input_mm.setPlaceholderText(t["ph_4"])
        
        # 3. Menu
        # We are looking for an object of type QMenu with the name "menu_root".
        menu_root = self.window.findChild(QMenu, "menu_root")
        if menu_root:
            menu_root.setTitle(t["menu_main_title"])
        else:
            # If you cannot find it by the name menu_root, try searching for the first menu you come across.
            # This is insurance in case of problems with names.
            pass

        # Menu options
        if hasattr(self.window, 'action_open'):
            self.window.action_open.setText(t["menu_open"])
            
        if hasattr(self.window, 'action_how_it_works'):
            self.window.action_how_it_works.setText(t["menu_help"])

    def show_instruction(self):
        t = TEXTS[self.current_lang]
        QMessageBox.about(self.window, t["instruction_title"], t["instruction_text"])

    def open_file(self):
            file_name, _ = QFileDialog.getOpenFileName(
                self.window, "Open", "", "Text Files (*.txt *.md)"
            )
            if not file_name: return

            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    full_text = f.read()
                
                parts = re.split(r'^## \d\..+', full_text, flags=re.MULTILINE)
                
                if len(parts) >= 5:
                    def clean(txt):
                        # 1. Отрезаем подвал (всё, что идет начиная с ---)
                        txt = txt.split('---')[0]
                        # 2. Вырезаем строку с оценкой (то, что выделено жирным **)
                        txt = re.sub(r'\*\*.*?\*\*', '', txt)
                        # 3. Чистим от лишних пробелов и переносов строк по краям
                        txt = txt.strip()
                        # 4. Если при сохранении поле было пустым (сохранилось тире), возвращаем пустоту
                        if txt == '—':
                            return ''
                        return txt
                    
                    self.window.input_pp.setPlainText(clean(parts[1]))
                    self.window.input_pm.setPlainText(clean(parts[2]))
                    self.window.input_mp.setPlainText(clean(parts[3]))
                    self.window.input_mm.setPlainText(clean(parts[4]))
                    
                    msg_title = TEXTS[self.current_lang]["saved_title"]
                    QMessageBox.information(self.window, msg_title, "OK")
            except Exception as e:
                print(f"Ошибка парсинга: {e}")