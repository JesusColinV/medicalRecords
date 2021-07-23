
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.picker import MDDatePicker
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from workers import CarrierKv, BuilderKv
Window.maximize()

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Main(Screen):
    myBuilder = BuilderKv()
    

    def on_save(self, instance, value, date_range):
        self.ids.txtInputDate.text = str(value)
        #print(instance, value)

    def on_cancel(self, instance, value):
        pass
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    

class App(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.icon ="C:\\Users\\ASUS\\Desktop\\clone\\KivyMD\\LUZ2.0\\metadata\\LOGO.png"
        self.title = 'LUZ Software Médico'
        return Main()

if __name__=='__main__':
    App().run()