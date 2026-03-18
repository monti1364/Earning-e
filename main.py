from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.animation import Animation
from kivymd.toast.kivytoast.kivytoast import toast

KV = '''
Screen:
    BoxLayout:
        orientation: "vertical"

        ScrollView:
            id: s1
            GridLayout:
                id: b1
                cols: 2
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                spacing: 10
                padding: 30

        MDTopAppBar:
            title: "Grid ScrollView Example"
            elevation: 4
            pos_hint: {'center_y': 1}
'''

class GridCardApp(MDApp):
    def build(self):
        self.title = "Scroll Grid App"
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def on_start(self):
        grid = self.root.ids.b1
        for i in range(1, 21):
            card = MDCard(
                size_hint=(1, None),
                height="120dp",
                padding="16dp",
                orientation="vertical",
                ripple_behavior=True,
                on_press=self.show_popup
            )
            label = MDLabel(
                text=f"Card {i}",
                halign="center",
                theme_text_color="Primary",
                font_style="H6"
            )
            card.add_widget(label)
            grid.add_widget(card)

    def show_popup(self, *args):
        # Check if popup already exists
        if hasattr(self, 'm') and self.m and self.m.parent:
            #self.m.add_widget(MDLabel(text=f'{self.m.parent} = {self.m}={hasattr(self,"m")} ')) # prevent multiple popups
            toast('already one')

        # Create popup MDCard
        else:
            self.m = MDCard(
                size_hint=(0.2,0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                on_press=self.dismiss_popup,
                md_bg_color=(1, 1, 1, 1),
                elevation=10000000,
                radius=[24],
                orientation="vertical",
                padding="12dp",
                opacity=0
            )
            self.anim()
            self.m.add_widget(MDLabel(text=f"{args}", halign="center", font_style="H6"))
            self.root.add_widget(self.m)

    def dismiss_popup(self, *args):
        if hasattr(self, 'm') and self.m and self.m.parent:
            self.root.remove_widget(self.m)
            self.m = None  # cleanup
            
    def anim(self):
            anim=Animation(size_hint=(0.6,0.4),opacity=1,duration=0.1)   
            anim.start(self.m)
            

GridCardApp().run()
