
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix import button
from kivymd.uix.picker import MDDatePicker
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
#from workers import CarrierKv, BuilderKv
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty,StringProperty
from kivy.uix.popup import Popup
import sqlite3
import os
Window.maximize()

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

APP_PATH = os.getcwd()
DB_PATH = APP_PATH+'/my_database.db'

class Main(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.connect_to_database(DB_PATH,'create')
        

    def on_save(self, instance, value, date_range):
        self.ids.txtInputDate.text = str(value)
        #print(instance, value)
    def on_cancel(self, instance, value):
        pass
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def Submit(self):
        self.connect_to_database(DB_PATH,'insert')
    
    def Search(self):
        self.connect_to_database(DB_PATH,'consult')

    def connect_to_database(self,path,metod):
        try:
            con = sqlite3.connect(path)
            self.cursor = con.cursor()
            if metod == 'create':
                self.create_table_productos()
            elif metod == 'insert':
                self.insert_data()
            elif metod == 'consult':
                self.check_records()
            '''elif metod == 'update':
                self.update_data()
            elif metod == 'delete':
                self.delete_data()
            else:
                print("metodo desconocido")'''
            con.commit()
            con.close()
        except Exception as e:
            print(e)

    def create_table_productos(self):
        try :
            self.cursor.execute(
                '''
                CREATE TABLE Records(
                ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre          text                    NOT NULL,
                snombre         text,
                aPaterno        text                    NOT NULL,
                aMaterno        text                    NOT NULL,
                sexo            text                    NOT NULL,
                fNacimiento     text                    NOT NULL,
                curp            text                    NOT NULL,
                nacionalidad    text                    NOT NULL,
                codigo_postal   text                    NOT NULL,
                localidad       text                    NOT NULL,
                municipio       text                    NOT NULL,
                direccion       text,
                religion        text                    NOT NULL,
                correo          text                    NOT NULL,
                telefono        text                    NOT NULL,
                faPaterno       text                    NOT NULL,
                faMaterno       text,
                faNombre        text                    NOT NULL,
                fasNombre       text,
                fTelefono       text                    NOT NULL
                )'''
            )
        except Exception as e:
            print(e)

    def insert_data(self):
        inFN = self.ids.txtInputFirstName.text #1
        insN = self.ids.txtInputSecondName.text #2
        inSN = self.ids.txtInputSurName1.text #3
        inSN2 = self.ids.txtInputSurName2.text #4
        inSex = self.ids.txtInputSex.text #5
        inBi = self.ids.txtInputDate.text #6
        inCurp = self.ids.txtInputCurp.text #7
        inNati = self.ids.txtInputNati.text #8
        inCP = self.ids.txtInputCP.text #9
        inLoc = self.ids.txtInputLoc.text #10
        inMun = self.ids.txtInputMun.text #11
        inDir = self.ids.txtInputDir.text #12
        inRel = self.ids.txtInputRel.text #13
        inEm = self.ids.txtInputEmail.text #14
        inPN = self.ids.txtInputPhoneNumber.text #15
        
        infFN = self.ids.txtInputfFirstName.text #23
        infsN = self.ids.txtInputfSecondName.text #24
        infSN = self.ids.txtInputfSurName1.text #25
        infSN2 = self.ids.txtInputfSurName2.text #26
        infPN=self.ids.txtInputfPhoneNumber.text #27
        data = (inFN,insN,inSN,inSN2,inSex,inBi,inCurp,inNati,inCP,inLoc,inMun,inRel,inEm,inDir,inPN,infFN,infsN,infSN,infSN2,infPN)
        s1 = '''INSERT INTO Records(ID,nombre, snombre, aPaterno, aMaterno, sexo, fNacimiento, curp, nacionalidad,codigo_postal,localidad, municipio, 
                direccion,religion,correo, telefono,faNombre, fasNombre, faPaterno, faMaterno, fTelefono )'''
        s2 = 'VALUES(null,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % data
        try:
            self.cursor.execute(s1+' '+s2)
        except Exception as e:
            print(e)

    def check_records(self):
        # cuadros = cursor.execute("SELECT * FROM cuadro  WHERE nombre='{}' ".format(buscador2.get())).fetchall()
        nombre= self.ids.txtInputSearch.text #26
        records=self.cursor.execute(f"SELECT nombre, snombre, aPaterno, aMaterno FROM Records WHERE nombre LIKE '{nombre}' or snombre LIKE '{nombre}' or aPaterno LIKE '{nombre}' or aPaterno LIKE '{nombre}'").fetchall()
        names=[]
        for record in records:

            names.append(record[0] + ' ' + record[-2] + ' ' + record[-1]) 

        self.update_table(*names)

    def update_table(self,*args):
        self.ids.table_box.clear_widgets()
        self.data_table = MDDataTable(
            pos_hint={'center_x':0.5,'center_y':0.5},
            size_hint = (0.9 , 0.6),
            column_data=[
                        ('num',dp(20)),
                        ('Persona',dp(100)),
                        ],
            row_data=[(i+1,row) for i,row in enumerate(args)],
        )
        self.ids.table_box.add_widget(self.data_table)
        self.data_table.bind(on_row_press = self.row_check)

    def row_check(self,instance_table, instance_row):
        print(instance_row.text)
        self.ids.screen_manager.current = "scrPacient"
        self.ids.txtPatient.text = str(instance_row.text)
        

        

class MessagePopup(Popup):
    pass

class RegisterPage(StackLayout):
    pass

'''class SearchPage(Screen):
aPatologicos    text                    NOT NULL,
                aNoPatologicos  text                    NOT NULL,
                procedimiento   text                    NOT NULL,
                hereditarios    text                    NOT NULL,
                medicacion      text                    NOT NULL,
                alergias        text                    NOT NULL,
                observaciones   text                    NOT NULL,


    inAPat = self.ids.txtInputAPat.text #16
        inANPat= self.ids.txtInputANPat.text #17
        inProc= self.ids.txtInputProc.text #18
        inHered= self.ids.txtInputHered.text #19
        inMedic= self.ids.txtInputMedic.text #20
        inAlerg= self.ids.txtInputAlerg.text #21
        inObserv= self.ids.txtInputObservc.text #22

        ,inAPat,inANPat,
                inProc,inHered,inMedic,inAlerg,inObserv
        
         aPatologicos, aNoPatologicos, procedimiento, hereditarios, medicacion, alergias, observaciones,
        '''
    

class App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.icon ="C:\\Users\\ASUS\\Desktop\\clone\\KivyMD\\LUZ2.0\\metadata\\LOGO.png"
        self.title = 'LUZ Software Médico'
        return Main()

if __name__=='__main__':
    App().run()