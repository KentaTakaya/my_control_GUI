from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

from kivy.core.text import LabelBase
# Font settings
LabelBase.register(name = "Roboto",
    fn_regular = "./Fonts/roboto/Roboto-Regular.ttf",
    fn_bold = "./Fonts/roboto/Roboto-Bold.ttf",
    fn_italic = "./Fonts/roboto/Roboto-Italic.ttf",
    fn_bolditalic = "./Fonts/roboto/Roboto-BoldItalic.ttf")

from kivy.core.window import Window
from kivy.utils import get_color_from_hex
Window.clearcolor = get_color_from_hex('#101216')

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.image import Image

class MainWindow(MDBoxLayout):
    def __init__(self, **key):
        super(MainWindow, self).__init__(**key)
        img = Image(source = "sin.png")
        test_label = MDLabel(font_name = "Roboto", text = "Hellow math", markup = True)
        self.add_widget(test_label)
        self.add_widget(img)

class ControllerTestApp(MDApp):
    def build(self):
        ma = MainWindow()
        return ma

if __name__ == '__main__':
    ControllerTestApp().run()
