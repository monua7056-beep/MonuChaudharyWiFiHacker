from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import random
import os
import shutil

Window.clearcolor = (0.02, 0.08, 0.02, 1)

# App storage folder
if platform == 'android':
    try:
        from android.storage import app_storage_path
        APP_DIR = app_storage_path()
    except:
        APP_DIR = '/data/data/com.monuchaudhary.monuwifi/files'
else:
    APP_DIR = os.path.expanduser('~/.monu_wifi')

SAVED_FILE = os.path.join(APP_DIR, 'passwords.txt')


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 8

        self.networks = []
        self.selected_network = None
        self.passwords = []

        # Folder बनाओ
        if not os.path.exists(APP_DIR):
            try:
                os.makedirs(APP_DIR)
            except:
                pass

        # पुरानी file load करो
        self.auto_load_saved()

        # Title
        title = Label(
            text='[b]Monu Chaudhary[/b]\n[b]WiFi Hacker Pro[/b]',
            markup=True,
            font_size='22sp',
            color=(0, 1, 0.25, 1),
            size_hint=(1, 0.13)
        )
        self.add_widget(title)

        # Status
        self.status_label = Label(
            text=self.get_status_text(),
            font_size='12sp',
            color=(0, 1, 0.25, 1),
            size_hint=(1, 0.07)
        )
        self.add_widget(self.status_label)

        # Terminal
        self.scroll = ScrollView(size_hint=(1, 0.42))
        self.terminal = Label(
            text='> System ready...\n> Add password file first',
            font_size='12sp',
            color=(0, 1, 0.25, 1),
            halign='left',
            valign='top',
            size_hint_y=None,
            size_hint_x=1,
        )
        self.terminal.bind(
            width=lambda *x: setattr(self.terminal, 'text_size', (self.terminal.width, None)),
            texture_size=lambda *x: setattr(self.terminal, 'height', self.terminal.texture_size[1])
        )
        self.scroll.add_widget(self.terminal)
        self.add_widget(self.scroll)

        # Button 1: ADD PASSWORD FILE
        self.add_btn = Button(
            text='📁 ADD PASSWORD FILE',
            font_size='17sp',
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        self.add_btn.bind(on_press=self.open_file_chooser)
        self.add_widget(self.add_btn)

        # Button 2: FIND NETWORK
        self.btn = Button(
            text='🔍 FIND NETWORK',
            font_size='19sp',
            background_color=(0, 1, 0.25, 1),
            color=(0, 0, 0, 1),
            size_hint=(1, 0.11)
        )
        self.btn.bind(on_press=self.start_scan)
        self.add_widget(self.btn)

        # Footer
        footer = Label(
            text='Owner: Monu Chaudhary | v1.0',
            font_size='11sp',
            color=(0, 1, 0.25, 1),
            size_hint=(1, 0.05)
        )
        self.add_widget(footer)

    def get_status_text(self):
        if self.passwords:
            return f'✅ File loaded: {len(self.passwords)} passwords'
        return '⚠️ No password file added yet'

    def update_status(self):
        self.status_label.text = self.get_status_text()

    def log(self, msg):
        self.terminal.text += f'\n> {msg}'

    def auto_load_saved(self):
        try:
            if os.path.exists(SAVED_FILE):
                with open(SAVED_FILE, 'r', encoding='utf-8') as f:
                    self.passwords = [
                        line.strip() for line in f
                        if line.strip() and not line.startswith('#')
                    ]
        except Exception as e:
            print(f"Auto load error: {e}")
            self.passwords = []

    # ============ ADD PASSWORD FILE ============
    def open_file_chooser(self, instance):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                ])
            except Exception as e:
                print(f"Permission error: {e}")

        self.log('')
        self.log('📁 Opening file manager...')
        self.log('   Select your passwords.txt')

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        filechooser = FileChooserListView(
            path='/sdcard' if platform == 'android' else os.path.expanduser('~'),
            filters=['*.txt']
        )
        content.add_widget(filechooser)

        btn_box = BoxLayout(size_hint_y=0.15, spacing=10)
        select_btn = Button(text='✅ ADD', background_color=(0, 1, 0.25, 1))
        cancel_btn = Button(text='❌ CANCEL', background_color=(1, 0.2, 0.2, 1))
        btn_box.add_widget(select_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        popup = Popup(
            title='Select passwords.txt',
            content=content,
            size_hint=(0.95, 0.9)
        )

        def on_select(inst):
            if filechooser.selection:
                path = filechooser.selection[0]
                popup.dismiss()
                self.import_file(path)
            else:
                self.log('❌ No file selected')

        def on_cancel(inst):
            popup.dismiss()
            self.log('❌ Cancelled')

        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=on_cancel)
        popup.open()

    def import_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith('#')
                ]

            if not lines:
                self.log('❌ File is empty!')
                return

            shutil.copy(path, SAVED_FILE)
            self.passwords = lines

            self.log(f'✅ File added: {os.path.basename(path)}')
            self.log(f'   Total passwords: {len(self.passwords)}')
            self.update_status()

        except Exception as e:
            self.log(f'❌ Error: {e}')

    # ============ FIND NETWORK ============
    def start_scan(self, instance):
        if not self.passwords:
            self.log('')
            self.log('⚠️ No password file!')
            self.log('   Add file first.')
            return

        self.btn.disabled = True
        self.add_btn.disabled = True
        self.terminal.text = '> [FIND NETWORK initiated...]'
        Clock.schedule_once(lambda dt: self.scan_networks(), 1)

    def scan_networks(self):
        self.log('Scanning nearby networks...')
        self.networks = [
            'JioFiber_Monu',
            'Airtel_Home_5G',
            'TP-Link_2.4G',
            'Monu_Chaudhary_WiFi',
            'Neighbor_WiFi',
        ]
        Clock.schedule_once(lambda dt: self.show_networks(), 1.5)

    def show_networks(self):
        self.log(f'Found {len(self.networks)} networks:')
        for i, name in enumerate(self.networks, 1):
            self.log(f'  {i}. {name} 🔒')
        Clock.schedule_once(lambda dt: self.show_select_buttons(), 0.5)

    def show_select_buttons(self):
        self.log('')
        self.log('👇 Select target:')
        for name in self.networks:
            b = Button(
                text=f'📶 {name}',
                font_size='14sp',
                background_color=(0, 0.6, 0.15, 1),
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=42
            )
            b.bind(on_press=lambda inst, n=name: self.select_network(n))
            self.add_widget(b, index=len(self.children) - 3)

    def select_network(self, name):
        self.selected_network = name
        self.terminal.text = '> [FIND NETWORK initiated...]\n> Scanning nearby networks...'
        for n in self.networks:
            self.log(f'  • {n} 🔒')
        self.log('')
        self.log(f'🎯 Target: {name}')
        Clock.schedule_once(lambda dt: self.check_passwords(), 1)

    # ============ CHECK PASSWORDS ============
    def check_passwords(self):
        self.log('')
        total = len(self.passwords)
        self.log(f'🔐 Password check ({total} total)...')

        if total <= 5:
            delay = 1.2
        elif total <= 15:
            delay = 0.6
        elif total <= 50:
            delay = 0.3
        else:
            delay = 0.15

        for i, pwd in enumerate(self.passwords, 1):
            Clock.schedule_once(
                lambda dt, p=pwd, n=i, t=total: self.try_one(p, n, t),
                i * delay
            )

        Clock.schedule_once(
            lambda dt: self.show_final_result(),
            total * delay + 1
        )

    def try_one(self, pwd, num, total):
        masked = pwd[:3] + '*' * (len(pwd) - 3) if len(pwd) > 3 else '***'
        self.log(f'[{num}/{total}] Trying: {masked}...')
        if num == total:
            self.log('Matching database...')

    def show_final_result(self):
        real_pwd = random.choice(self.passwords)

        self.log('')
        self.log('██████████████████████████')
        self.log('  ⚡ CONNECTED SUCCESSFULLY ⚡')
        self.log('██████████████████████████')
        self.log(f'  📶 WiFi Name: {self.selected_network}')
        self.log(f'  🔑 Password : {real_pwd}')
        self.log(f'  🔒 Security : WPA2-PSK')
        self.log(f'  ✅ Status   : CONNECTED')
        self.log('')
        self.log('  👨‍💻 Hacked by Monu Chaudhary')
        self.log('██████████████████████████')

        self.btn.disabled = False
        self.add_btn.disabled = False
        self.btn.text = '🔄 HACK AGAIN'


class MonuWiFiApp(App):
    def build(self):
        self.title = 'Monu Chaudhary WiFi Hacker'
        return MainScreen()


if __name__ == '__main__':
    MonuWiFiApp().run()
