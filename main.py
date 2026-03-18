from kivymd.app import MDApp
from kivy.lang import Builder
from kivmob import KivMob
from kivy.utils import platform
from kivymd.toast import toast

class MainApp(MDApp):
    def build(self):
        # Test App ID
        self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")
        
        # Test Interstitial ID
        self.ads.add_interstitial_ad("ca-app-pub-3940256099942544/1033173712")
        
        return Builder.load_string('''
MDScreen:
    MDRaisedButton:
        text: "SHOW INTERSTITIAL AD"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_ad()
''')

    def on_start(self):
        # App start hote hi background mein ad load karo
        if platform == "android":
            self.ads.request_interstitial_ad()

    def show_ad(self):
        if platform == "android":
            if self.ads.is_interstitial_ad_loaded():
                self.ads.show_interstitial_ad()
            else:
                toast("Ad loading... please wait")
                self.ads.request_interstitial_ad()
        else:
            toast("Ads only work on Android APK")

if __name__ == "__main__":
    MainApp().run()
    
