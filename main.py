from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast

# Global variables
InterstitialAd = None
AdRequest = None
MobileAds = None
_interstitial_ad = None
TEST_ID = "ca-app-pub-3940256099942544/1033173712"

class MainApp(MDApp):
    def build(self):
        self.count = 0
        return Builder.load_string('''
MDScreen:
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDRaisedButton:
            text: "SHOW INTERSTITIAL"
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: app.handle_click()
        MDLabel:
            id: counter
            text: "Clicks: 0"
            halign: "center"
            pos_hint: {"center_y": .4}
''')

    def on_start(self):
        if platform == "android":
            # 2 second baad load karein taaki app stable ho jaye
            Clock.schedule_once(self.setup_ads, 2)

    def setup_ads(self, dt):
        global InterstitialAd, AdRequest, MobileAds, MyAdListener
        try:
            from jnius import autoclass, PythonJavaClass, java_method
            from android.runnable import run_on_ui_thread

            # Classes ko function ke andar load kar rahe hain taaki startup crash na ho
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            InterstitialAd = autoclass('com.google.android.gms.ads.InterstitialAd')
            AdListener = autoclass('com.google.android.gms.ads.AdListener')
            MobileAds = autoclass('com.google.android.gms.ads.MobileAds')

            class MyAdListener(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/ads/AdListener']
                __javacontext__ = 'app'
                @java_method('()V')
                def onAdLoaded(self): toast("Ad Ready!")
                @java_method('(I)V')
                def onAdFailedToLoad(self, code): print(f"Error {code}")

            # Initialize
            MobileAds.initialize(PythonActivity.mActivity)
            self.load_ad_logic()
            
        except Exception as e:
            error_msg = f"Setup Error: {str(e)}"
            Clipboard.copy(error_msg)
            toast("Ads setup failed. Error copied.")

    def load_ad_logic(self):
        global _interstitial_ad
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        _interstitial_ad = InterstitialAd(PythonActivity.mActivity)
        _interstitial_ad.setAdUnitId(TEST_ID)
        _interstitial_ad.setAdListener(MyAdListener())
        _interstitial_ad.loadAd(AdRequest().build())

    def handle_click(self):
        self.count += 1
        self.root.ids.counter.text = f"Clicks: {self.count}"
        if self.count % 3 == 0:
            self.show_ad()

    def show_ad(self):
        if _interstitial_ad and _interstitial_ad.isLoaded():
            _interstitial_ad.show()
            self.load_ad_logic() # Reload
        else:
            toast("Ad not ready or not supported on this build")

if __name__ == "__main__":
    MainApp().run()
    
