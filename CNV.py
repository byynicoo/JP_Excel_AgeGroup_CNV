# IMPORT LIBRARIES
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import pandas as pd
from datetime import datetime

# IMPOSTA SFONDO NERO
Window.clearcolor = (0, 0, 0, 1)  # nero

class Convertitore(App):
    def build(self):
        self.icon = "favicon.png"

        # Layout principale verticale
        root = BoxLayout(orientation='vertical', padding=40, spacing=30)

        # Logo
        logo = Image(source="assets/logo.png", size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
        root.add_widget(logo)

        # Layout per pulsanti
        button_layout = GridLayout(cols=1, spacing=20, size_hint=(1, 0.5))

        # Pulsante NIKE
        self.button_nike = Button(
            text="NIKE - Aggiungi Age Group",
            font_size=20,
            bold=True,
            background_normal='',
            background_color=(1, 0.24, 0.2, 1),  # rosso elegante
            color=(1, 1, 1, 1),  # testo bianco
            size_hint=(1, None),
            height=60,
        )
        self.button_nike.bind(on_press=self.NIKE)
        button_layout.add_widget(self.button_nike)

        # Pulsante HADDAD
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
        self.button_haddad.bind(on_press=self.HADDAD)
        button_layout.add_widget(self.button_haddad)

        root.add_widget(button_layout)

        # Etichetta versione in basso
        version_label = Label(
            text="© Just Play TEAM - v.3.2.4 build 1",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.1),
            halign='center',
            valign='middle',
        )
        version_label.bind(size=version_label.setter('text_size'))
        root.add_widget(version_label)

        return root

    # Funzione NIKE
    def NIKE(self, instance):
        current_dateTime = datetime.now()

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

        def process_excel_file(input_file):
            input_df = pd.read_excel(input_file)
            if 'Codice sesso' not in input_df.columns:
                print("ERRORE - Conferma d'ordine errata, assicurati di aver inserito quella di NIKE.")
                return
            input_df['Age Group'] = input_df['Codice sesso'].apply(categorize_age_group)
            input_df.to_excel(input_file, index=False)
            print("[FUNZIONE] ESEGUITO - Conversione Nike Eseguita", current_dateTime)

        try:
            file_path = next(os.path.join("excel/", f) for f in os.listdir("excel/") if f.endswith(".xlsx"))
            process_excel_file(file_path)
        except StopIteration:
            print("Nessun file Excel trovato nella cartella 'excel/'")

    # Funzione HADDAD
    def HADDAD(self, instance):
        current_dateTime = datetime.now()

        def categorize_age_group(code):
            code = str(code)
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

        def categorize_brand(code):
            code = str(code)
            if code[0] == '6':
                return 'BOY'
            elif code[0] == '8':
                return 'GIRL'
            elif code[0] == '9':
                return 'BOY'
            elif code[0] == '1':
                return 'GIRL'
            elif code[0] == '3':
                return 'GIRL'
            elif code[0] == '4':
                return 'GIRL'
            else:
                return ''

        def process_excel_file(input_file):
            input_df = pd.read_excel(input_file)
            if 'Codice articolo fornitore' not in input_df.columns:
                print("ERRORE - Conferma d'ordine errata, assicurati di aver inserito quella di HADDAD.")
                return
            input_df['Age Group'] = input_df['Codice articolo fornitore'].apply(categorize_age_group)
            # input_df['Sesso'] = input_df['Codice articolo fornitore'].apply(categorize_brand)  # opzionale
            input_df.to_excel(input_file, index=False)
            print("[FUNZIONE] ESEGUITO - Conversione Haddad Eseguita", current_dateTime)

        try:
            file_path = next(os.path.join("excel/", f) for f in os.listdir("excel/") if f.endswith(".xlsx"))
            process_excel_file(file_path)
        except StopIteration:
            print("Nessun file Excel trovato nella cartella 'excel/'")


# AVVIO
if __name__ == "__main__":
    Convertitore().run()
