from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast

# Android specific imports for 19.8.0
if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    
    # 19.8.0 mein paths alag hote hain (interstitial word beech mein nahi hota)
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    InterstitialAd = autoclass('com.google.android.gms.ads.InterstitialAd')
    AdListener = autoclass('com.google.android.gms.ads.AdListener')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
else:
    def run_on_ui_thread(func): return func

_interstitial_ad = None
TEST_ID = "ca-app-pub-3940256099942544/1033173712"

# 19.8.0 mein AdListener ek Interface hai (Isse crash nahi hoga)
class MyAdListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/AdListener']
    __javacontext__ = 'app'

    @java_method('()V')
    def onAdLoaded(self):
        Clock.schedule_once(lambda x: toast("Ad Ready to Show!"))

    @java_method('(I)V')
    def onAdFailedToLoad(self, errorCode):
        # Error codes: 0=Internal, 1=Invalid, 2=Network, 3=No Fill
        err = f"Load Failed! Code: {errorCode}"
        Clipboard.copy(err)
        Clock.schedule_once(lambda x: toast(err))

@run_on_ui_thread
def load_interstitial():
    global _interstitial_ad
    try:
        activity = PythonActivity.mActivity
        MobileAds.initialize(activity)
        
        # 19.8.0 loading style
        _interstitial_ad = InterstitialAd(activity)
        _interstitial_ad.setAdUnitId(TEST_ID)
        _interstitial_ad.setAdListener(MyAdListener())
        
        builder = AdRequest()
        _interstitial_ad.loadAd(builder.build())
    except Exception as e:
        Clipboard.copy("Load Exception: " + str(e))

@run_on_ui_thread
def show_interstitial():
    global _interstitial_ad
    try:
        if _interstitial_ad and _interstitial_ad.isLoaded():
            _interstitial_ad.show()
        else:
            toast("Ad not loaded yet. Loading now...")
            load_interstitial()
    except Exception as e:
        Clipboard.copy("Show Exception: " + str(e))

# --- UI ---
kv = '''
MDScreen:
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDRaisedButton:
            text: "SHOW AD (3rd Click)"
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: app.handle_click()
        MDLabel:
            id: lbl
            text: "Clicks: 0"
            halign: "center"
            pos_hint: {"center_y": .4}
'''

class TestApp(MDApp):
    def build(self):
        self.count = 0
        return Builder.load_string(kv)

    def on_start(self):
        if platform == "android":
            load_interstitial()

    def handle_click(self):
        self.count += 1
        self.root.ids.lbl.text = f"Clicks: {self.count}"
        if self.count % 3 == 0:
            if platform == "android":
                show_interstitial()
            else:
                toast("Works only on Android")

if __name__ == '__main__':
    TestApp().run()
    
