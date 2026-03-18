from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast

# --- ANDROID IMPORTS ---
if platform == "android":
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
        
        # Fundamental Android Classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        # AdMob Classes (19.8.0 structure)
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        InterstitialAd = autoclass('com.google.android.gms.ads.InterstitialAd')
        AdListener = autoclass('com.google.android.gms.ads.AdListener')
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    except Exception as e:
        Clipboard.copy(str(e))
else:
    def run_on_ui_thread(func): return func

# --- GLOBAL VARIABLES ---
_interstitial_ad = None
TEST_ID = "ca-app-pub-3940256099942544/1033173712"

# --- LISTENER ---
class MyAdListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/AdListener']
    __javacontext__ = 'app'

    @java_method('()V')
    def onAdLoaded(self):
        Clock.schedule_once(lambda x: toast("Ad Ready!"))

    @java_method('(I)V')
    def onAdFailedToLoad(self, errorCode):
        msg = f"Failed to load: Error Code {errorCode}"
        Clipboard.copy(msg)
        Clock.schedule_once(lambda x: toast(msg))

# --- AD FUNCTIONS ---
@run_on_ui_thread
def initialize_ads():
    try:
        # 19.8.0 mein initialize sirf context maangta hai
        MobileAds.initialize(PythonActivity.mActivity)
    except Exception as e:
        Clipboard.copy("Init Error: " + str(e))

@run_on_ui_thread
def load_interstitial():
    global _interstitial_ad
    try:
        # Create Interstitial instance
        _interstitial_ad = InterstitialAd(PythonActivity.mActivity)
        _interstitial_ad.setAdUnitId(TEST_ID)
        _interstitial_ad.setAdListener(MyAdListener())
        
        # Build and Load Request
        builder = AdRequest()
        _interstitial_ad.loadAd(builder.build())
    except Exception as e:
        Clipboard.copy("Load Error: " + str(e))

@run_on_ui_thread
def show_interstitial():
    global _interstitial_ad
    try:
        if _interstitial_ad and _interstitial_ad.isLoaded():
            _interstitial_ad.show()
        else:
            toast("Not ready, loading now...")
            load_interstitial()
    except Exception as e:
        Clipboard.copy("Show Error: " + str(e))

# --- APP CLASS ---
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
            # Initialize MobileAds first, then load after a small delay
            initialize_ads()
            Clock.schedule_once(lambda x: load_interstitial(), 2)

    def handle_click(self):
        self.count += 1
        self.root.ids.counter.text = f"Clicks: {self.count}"
        if self.count % 3 == 0:
            if platform == "android":
                show_interstitial()
            else:
                toast("Android only feature")

if __name__ == "__main__":
    MainApp().run()
    
