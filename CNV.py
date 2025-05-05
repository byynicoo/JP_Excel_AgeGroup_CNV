import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
import pandas as pd
from datetime import datetime

# Sfondo nero
Window.clearcolor = (0, 0, 0, 1)

class Convertitore(App):
    def build(self):
        self.icon = "favicon.png"
        root = BoxLayout(orientation='vertical', padding=40, spacing=30)

        # Logo
        logo = Image(source="assets/logo.png", size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
        root.add_widget(logo)

        # Pulsanti
        button_layout = GridLayout(cols=1, spacing=20, size_hint=(1, 0.5))

        self.button_nike = Button(
            text="NIKE - Aggiungi Age Group",
            font_size=20,
            bold=True,
            background_normal='',
            background_color=(1, 0.24, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=60,
        )
        self.button_nike.bind(on_press=lambda x: self.open_filechooser(self.NIKE))
        button_layout.add_widget(self.button_nike)

        self.button_haddad = Button(
            text="HADDAD - Aggiungi Age Group & Brand",
            font_size=20,
            bold=True,
            background_normal='',
            background_color=(1, 0.24, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=60,
        )
        self.button_haddad.bind(on_press=lambda x: self.open_filechooser(self.HADDAD))
        button_layout.add_widget(self.button_haddad)

        root.add_widget(button_layout)

        # Etichetta versione
        version_label = Label(
            text="3Abrands - v.3.2.4 build 1.2",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.1),
            halign='center',
            valign='middle',
        )
        version_label.bind(size=version_label.setter('text_size'))
        root.add_widget(version_label)

        return root

    def open_filechooser(self, callback_function):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(filters=['*.xlsx'], path='excel/')
        button_box = BoxLayout(size_hint_y=0.2, spacing=10, padding=10)

        btn_select = Button(text="Seleziona", background_color=(0, 0.6, 0, 1), color=(1, 1, 1, 1))
        btn_cancel = Button(text="Annulla", background_color=(0.5, 0, 0, 1), color=(1, 1, 1, 1))

        popup = Popup(title="Seleziona un file Excel", content=content, size_hint=(0.9, 0.9))
        content.add_widget(filechooser)
        content.add_widget(button_box)
        button_box.add_widget(btn_cancel)
        button_box.add_widget(btn_select)

        def select_file(instance):
            if filechooser.selection:
                selected_file = filechooser.selection[0]
                popup.dismiss()
                callback_function(selected_file)

        btn_select.bind(on_press=select_file)
        btn_cancel.bind(on_press=popup.dismiss)
        popup.open()

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        label = Label(text=message, halign='center', valign='middle', color=(1, 1, 1, 1))
        label.bind(size=label.setter('text_size'))
        btn_close = Button(text="OK", size_hint_y=None, height=40, background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1))

        popup = Popup(title=title, content=layout, size_hint=(0.7, 0.4))
        btn_close.bind(on_press=popup.dismiss)

        layout.add_widget(label)
        layout.add_widget(btn_close)
        popup.open()

    # NIKE
    def NIKE(self, file_path):
        def categorize_age_group(gender_age_code):
            if gender_age_code == '':
                return "BIG SIZE"
            elif gender_age_code == 'U':
                return "UNISEX"
            elif gender_age_code == 'D':
                return "BIG SIZE"
            elif gender_age_code == 'J':
                return "TEEN"
            else:
                return "MANCANTE"

        try:
            input_df = pd.read_excel(file_path)
            if 'Codice sesso' not in input_df.columns:
                raise ValueError("Colonna 'Codice sesso' mancante.")
            input_df['Age Group'] = input_df['Codice sesso'].apply(categorize_age_group)
            input_df.to_excel(file_path, index=False)
            self.show_popup("Operazione completata", "Conversione NIKE eseguita con successo.")
        except Exception as e:
            self.show_popup("Errore", f"Errore nella conversione NIKE:\n{str(e)}")

    # HADDAD
    def HADDAD(self, file_path):
        def categorize_age_group(code):
            code = str(code)
            if len(code) > 10:
                return ''
            if '-' not in code:
                return ''
            if len(code) > 1 and code[1] == 'A':
                return ''
            if code[0] in ['1', '6']:
                return 'INFANT'
            elif code[0] in ['3', '8']:
                return 'KIDS'
            elif code[0] in ['4', '9']:
                return 'TEEN'
            else:
                return ''

        try:
            input_df = pd.read_excel(file_path)
            if 'Codice articolo fornitore' not in input_df.columns:
                raise ValueError("Colonna 'Codice articolo fornitore' mancante.")
            input_df['Age Group'] = input_df['Codice articolo fornitore'].apply(categorize_age_group)
            input_df.to_excel(file_path, index=False)
            self.show_popup("Operazione completata", "Conversione HADDAD eseguita con successo.")
        except Exception as e:
            self.show_popup("Errore", f"Errore nella conversione HADDAD:\n{str(e)}")


if __name__ == "__main__":
    Convertitore().run()
