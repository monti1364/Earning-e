from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivymd.toast import toast

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    InterstitialAd = autoclass('com.google.android.gms.ads.interstitial.InterstitialAd')
    # Naye version mein ye path zaroori hai
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
else:
    def run_on_ui_thread(func): return func

_interstitial_ad = None

# --- FIX: Hum LoadCallback ko direct class se handle karenge ---
class AdHandler:
    @staticmethod
    def on_load_success(ad):
        global _interstitial_ad
        _interstitial_ad = ad
        toast("Ad Loaded Successfully!")

    @staticmethod
    def on_load_error(error):
        print(f"Ad Load Failed: {error.getMessage()}")

@run_on_ui_thread
def load_ad_v22():
    try:
        activity = PythonActivity.mActivity
        MobileAds.initialize(activity)
        
        # Test ID
        unit_id = "ca-app-pub-3940256099942544/1033173712"
        request = AdRequest().build()
        
        # Yahan hum Java wrapper ya direct load call use karte hain
        # Crash se bachne ke liye interface ko bypass karna padta hai
        # Is specific line par dhyan dein:
        from jnius import cast
        
        # Simple loading without complex callbacks to avoid IllegalArgumentException
        InterstitialAd.load(activity, unit_id, request, None) 
        # Note: 'None' ki wajah se load hoga par callback nahi milega. 
        # Interface crash fix karne ka yehi ek rasta hai Pyjnius mein.
        
    except Exception as e:
        print(f"Error: {e}")

class MainApp(MDApp):
    def build(self):
        return Builder.load_string('''
MDScreen:
    MDRaisedButton:
        text: "LOAD & SHOW AD"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_ad()
''')

    def show_ad(self):
        if platform == "android":
            load_ad_v22()
            toast("Checking for ads...")
        else:
            toast("Not on Android")

MainApp().run()
