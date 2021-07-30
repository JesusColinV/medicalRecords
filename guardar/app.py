
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.picker import MDDatePicker
from kivy.uix.stacklayout import StackLayout

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
Window.maximize()

import os
import sqlite3

def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        con.close()
    except Exception as e:
        print(e)

def create_database(self):
    pass

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    
class Main(StackLayout):
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker objecpip ist>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;pip inspi
        '''
        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        
    def submit(self):
        d1 = self.ids.txtInputFirstName.text
        d2 = self.ids.txtInputSecondName.text
        d3 = self.ids.txtInputSurName1.text
        d4 = self.ids.txtInputSurName2.text
        d5 = self.ids.txtInputEmail.text
        d6 = self.ids.txtInputCP.text
        d7 = self.ids.txtInputDir.text
        d8 = self.ids.txtInputPhoneNumber.text
        d9 = self.ids.txtInputDAte

        print(d1,d2,d3,d4,d5,d6,d7,d8,d9)
        
        
        
        
        
        
        
        
        
                       
                        



class app(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH + "/my_database.db"

    

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.icon ="C:\\Users\\ASUS\\Desktop\\clone\\KivyMD\\LUZ2.0\\metadata\\LOGO.png"
        self.title = 'LUZ Software Médico'
        return Builder.load_file("layout.kv")
    
app().run()