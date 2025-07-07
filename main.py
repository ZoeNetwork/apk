from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.clock import Clock
import requests

HOTSPOT_IP = "192.168.178.34"
API_BASE = f"http://{HOTSPOT_IP}:5000"

TG_LIST = [
    "1", "2", "7", "9", "13", "20", "91", "93", "94", "99", "262",
    "270", "272", "4000", "91", "3100", "3101", "3102", "3103", "3104"
    # Add more talkgroups as needed
]

class ZoeMMDVM(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.status_label = Label(text="Loading status...", size_hint=(1, 0.1))
        self.add_widget(self.status_label)

        self.tg_spinner = Spinner(
            text="Select Talkgroup",
            values=TG_LIST,
            size_hint=(1, 0.1)
        )
        self.tg_spinner.bind(text=self.on_tg_select)
        self.add_widget(self.tg_spinner)

        self.unlink_btn = Button(text="Unlink Talkgroup", size_hint=(1, 0.1))
        self.unlink_btn.bind(on_press=self.unlink_tg)
        self.add_widget(self.unlink_btn)

        self.refresh_btn = Button(text="Refresh Status", size_hint=(1, 0.1))
        self.refresh_btn.bind(on_press=self.refresh_status)
        self.add_widget(self.refresh_btn)

        Clock.schedule_interval(lambda dt: self.refresh_status(None), 5)
        self.refresh_status(None)

    def refresh_status(self, instance):
        try:
            resp = requests.get(f"{API_BASE}/status", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                callsign = data.get("callsign", "N/A")
                tg = data.get("talkgroup", "None")
                mode = data.get("mode", "Idle")
                self.status_label.text = f"Callsign: {callsign} | Talkgroup: {tg} | Mode: {mode}"
        except Exception as e:
            self.status_label.text = f"Error fetching status: {e}"

    def on_tg_select(self, spinner, text):
        try:
            resp = requests.get(f"{API_BASE}/tg/{text}")
            if resp.status_code == 200:
                self.status_label.text = f"Linked to Talkgroup {text}"
        except Exception as e:
            self.status_label.text = f"Error linking TG: {e}"

    def unlink_tg(self, instance):
        try:
            resp = requests.get(f"{API_BASE}/unlink")
            if resp.status_code == 200:
                self.status_label.text = "Unlinked from Talkgroup"
        except Exception as e:
            self.status_label.text = f"Error unlinking TG: {e}"

class ZoeApp(App):
    def build(self):
        self.title = "Zoe MMDVM Hotspot"
        return ZoeMMDVM()

if __name__ == "__main__":
    ZoeApp().run()
