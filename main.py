import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast
import requests
from threading import Thread
import json
from datetime import datetime

KV = '''
<FactCard>:
    orientation: 'vertical'
    padding: dp(8)
    size_hint: None, None
    size: dp(280), dp(140)
    pos_hint: {'center_x': .5}
    elevation: 3
    md_bg_color: app.theme_cls.bg_light

    MDLabel:
        text: root.fact_text
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1]
        padding: dp(8), dp(8)
        halign: 'center'

    MDLabel:
        text: root.timestamp
        theme_text_color: "Hint"
        size_hint_y: None
        height: dp(20)
        font_style: 'Caption'
        halign: 'right'
        padding_x: dp(8)

<MainScreen>:
    data_label: data_label
    category_label: category_label
    history_list: history_list
    
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(16)
        padding: dp(16)
        md_bg_color: app.theme_cls.bg_normal
        
        MDTopAppBar:
            title: "Awesome Facts"
            elevation: 2
            pos_hint: {"top": 1}
            right_action_items: [['history', lambda x: root.show_history()], ['theme-light-dark', lambda x: app.toggle_theme()]]
            
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(16)
            adaptive_height: True
            padding: [0, dp(20), 0, 0]
            
            MDCard:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(8)
                size_hint: None, None
                size: dp(300), dp(200)
                pos_hint: {'center_x': .5}
                elevation: 3
                md_bg_color: app.theme_cls.bg_light
                
                MDLabel:
                    id: data_label
                    text: 'Welcome! Click the button to fetch a fact!'
                    theme_text_color: "Primary"
                    halign: 'center'
                    valign: 'center'
                    
                MDLabel:
                    id: category_label
                    text: ''
                    theme_text_color: "Secondary"
                    font_style: 'Caption'
                    halign: 'center'
                    size_hint_y: None
                    height: self.texture_size[1]
                    
            MDBoxLayout:
                adaptive_height: True
                spacing: dp(8)
                padding: [dp(8), 0, dp(8), 0]
                pos_hint: {'center_x': .5}
                
                MDRaisedButton:
                    text: 'Fetch Random Fact'
                    on_release: root.fetch_data('random')
                    md_bg_color: app.theme_cls.primary_color
                    
                MDRaisedButton:
                    text: 'Tech Fact'
                    on_release: root.fetch_data('tech')
                    md_bg_color: app.theme_cls.accent_color
                    
        ScrollView:
            id: history_scroll
            size_hint_y: None
            height: dp(200)
            
            MDList:
                id: history_list
                spacing: dp(8)
                padding: dp(8)
'''

class FactCard(MDCard):
    fact_text = StringProperty('')
    timestamp = StringProperty('')

class MainScreen(MDScreen):
    data_label = ObjectProperty(None)
    category_label = ObjectProperty(None)
    history_list = ObjectProperty(None)
    loading = BooleanProperty(False)
    facts_history = []
    max_history = 10
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        Clock.schedule_once(self.load_history)
        
    def fetch_data(self, category='random'):
        if self.loading:
            toast("Please wait, already fetching data...")
            return
            
        self.loading = True
        self.show_loading()
        Thread(target=self.get_data_from_api, args=(category,)).start()
        
    def get_data_from_api(self, category):
        try:
            response = requests.get(f'https://facts7878.glitch.me/{category}', timeout=5)
            response.raise_for_status()
            data = response.json()
            
            Clock.schedule_once(lambda dt: self.update_content(data))
            
        except requests.Timeout:
            Clock.schedule_once(lambda dt: self.show_error(
                "Request timed out. Please check your internet connection."))
        except requests.ConnectionError:
            Clock.schedule_once(lambda dt: self.show_error(
                "Unable to connect to server. Please check if the server is running."))
        except requests.RequestException as e:
            Clock.schedule_once(lambda dt: self.show_error(
                f"An error occurred: {str(e)}"))
        finally:
            Clock.schedule_once(lambda dt: self.hide_loading())
            self.loading = False
            
    def update_content(self, data):
        fact = data.get('fact', 'No fact received')
        category = data.get('category', 'General')
        
        self.data_label.text = fact
        self.category_label.text = f"Category: {category}"
        
        self.add_to_history(fact)
        
    def add_to_history(self, fact):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.facts_history.insert(0, {
            'fact': fact,
            'timestamp': timestamp
        })
        
        if len(self.facts_history) > self.max_history:
            self.facts_history.pop()
            
        self.save_history()
        self.update_history_list()
        
    def update_history_list(self, *args):
        if self.history_list:
            self.history_list.clear_widgets()
            for item in self.facts_history:
                card = FactCard(
                    fact_text=item['fact'],
                    timestamp=item['timestamp']
                )
                self.history_list.add_widget(card)
            
    def save_history(self):
        try:
            # Construct the full path for the facts_history.json file
            file_path = os.path.join(self.user_data_dir, 'facts_history.json')
            
            with open(file_path, 'w') as f:
                json.dump(self.facts_history, f)
        except Exception as e:
            print(f"Error saving history: {e}")

    def load_history(self, *args):
        try:
            # Construct the full path for the facts_history.json file
            file_path = os.path.join(self.user_data_dir, 'facts_history.json')
            
            with open(file_path, 'r') as f:
                self.facts_history = json.load(f)
                self.update_history_list()
        except FileNotFoundError:
            # File does not exist, nothing to load
            pass
        except Exception as e:
            print(f"Error loading history: {e}")

            
    def show_loading(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Loading your fact...",
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()
        
    def hide_loading(self):
        if self.dialog:
            self.dialog.dismiss()
            
    def show_error(self, message):
        Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.8,
            pos_hint={'center_x': .5},
            duration=3,
        ).open()
        
    def show_history(self):
        if not self.facts_history:
            toast("No history available")
            return
            
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(400)
        )
        
        dialog = MDDialog(
            title="Facts History",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDFlatButton(
                    text="CLEAR",
                    on_release=lambda x: self.clear_history(dialog)
                )
            ]
        )
        dialog.open()
        
    def clear_history(self, dialog):
        self.facts_history.clear()
        self.save_history()
        self.update_history_list()
        dialog.dismiss()
        toast("History cleared")

class FactsApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        Builder.load_string(KV)
        return MainScreen()
        
    def toggle_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

if __name__ == '__main__':
    url = 'https://facts7878.glitch.me/' 
    requests.get(url)
    FactsApp().run()