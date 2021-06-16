from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast


KV = '''
BoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: "My Control GUI"
        left_action_items: [['menu', lambda x: None]]
        elevation: 10

    FloatLayout:
        id: main_float
        MDRoundFlatIconButton:
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .6}
            on_release: app.file_manager_open()

        MDTextField:
            hint_text: "Helper text on focus"
            helper_text: "This will disappear when you click off"
            shelper_text_mode: "on_focus"
            pos_hint: {'center_x': .2, 'center_y': .2}
            color_mode: 'accent'
            mode: "rectangle"

        MDLabel:
            id: filepath_label
            pos_hint: {'center_x': .7, 'center_y': .7}
            text: "A_PATH"


'''


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard = self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
            #preview = True,
            ext = [".py", ".kv", ".dat"],
        )

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.widget = Builder.load_string(KV)
        print(self.widget.children[0].children[0].text)
        return self.widget

    def file_manager_open(self):
        self.file_manager.show('./')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)
        self.widget.children[0].children[0].text = path

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


Example().run()
