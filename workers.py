from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os
import sqlite3

class CarrierKv:
    def __init__(self):
        pass
    def connect_to_database(self,path,metod):
        try:
            con = sqlite3.connect(path)
            self.cursor = con.cursor()
            if metod == 'create':
                self.create_table_productos()
            elif metod == 'insert':
                self.insert_data()
            elif metod == 'update':
                self.update_data()
            elif metod == 'consult':
                self.check_memory()
            elif metod == 'delete':
                self.delete_data()
            else:
                print("metodo desconocido")

            con.commit()
            con.close()
        except Exception as e:
            print(e)

    def create_table_productos(self):
        try :
            self.cursor.execute(
                '''
                CREATE TABLE Records(
                ID              INT   PRIMARY KEY  AUTOINCREMENT,
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
                religion        text                    NOT NULL,
                correo          text                    NOT NULL,
                telefono        text                    NOT NULL,
                aPatologicos    text                    NOT NULL,
                aNoPatologicos  text                    NOT NULL,
                procedimiento   text                    NOT NULL,
                hereditarios    text                    NOT NULL,
                medicacion      text                    NOT NULL,
                alergias        text                    NOT NULL,
                observaciones   text                    NOT NULL,
                faPaterno       text                    NOT NULL,
                faMaterno       text                    NOT NULL,
                faNombre       text                    NOT NULL,
                fasNombre
                fTelefono       text                    NOT NULL
                )'''
            )
        except sqlite3.OperationalError:
            print("La tabla de Pacientes ya existe.")
        else:
            print("La tabla de Pacientes se ha creado correctamente.")

    def insert_data(self):
        inFN = self.ids.txtInputFirstName.text
        insN = self.ids.txtInputSecondName.text
        inSN = self.ids.txtInputSurName1.text
        inSN2 = self.ids.txtInputSurName2.text
        inSex = self.ids.txtInputSex.text
        inBi = self.ids.txtInputDate.text
        inCurp = self.ids.txtInputCurp.text
        inNati = self.ids.txtInputNati.text
        inCP = self.ids.txtInputCP.text
        inLoc = self.ids.txtInputLoc.text
        inMun = self.ids.txtInputMun.text
        inDir = self.ids.txtInputDir.text
        inRel = self.ids.txtInputRel.text
        inEm = self.ids.txtInputEmail.text
        inPN = self.ids.txtInputPhoneNumber.text
        inAPat = self.ids.txtInputAPat.text
        inANPat= self.ids.txtInputANPat.text
        inProc= self.ids.txtInputProc.text
        inHered= self.ids.txtInputHered.text
        inMedic= self.ids.txtInputMedic.text
        inAlerg= self.ids.txtInputAlerg.text
        inObserv= self.ids.txtInputObservc.text
        infFN = self.ids.txtInputfFirstName.text
        infsN = self.ids.txtInputfSecondName.text
        infSN = self.ids.txtInputfSurName1.text
        infSN2 = self.ids.txtInputfSurName2.text
        infPN=self.ids.txtInputfPhoneNumber.text

        data = (inFN,insN,inSN,inSN2,inSex,inBi,inCurp,inNati,inCP,inLoc,inMun,inRel,inEm,inDir,inPN,inAPat,inANPat,
                inProc,inHered,inMedic,inAlerg,inObserv,infFN,infsN,infSN,infSN2,infPN)
        s1 = '''INSERT INTO Records(nombre, snombre, aPaterno, aMaterno, sexo, fNacimiento, curp, nacionalidad,codigo_postal,localidad, municipio,direccion,
                religion,correo, telefono, aPatologicos, aNoPatologicos, procedimiento, hereditarios, medicacion, alergias, observaciones,
                faNombre, fasNombre, faPaterno, faMaterno, fTelefono )'''
        s2 = 'VALUES(null,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % data
        try:
            self.cursor.execute(s1+' '+s2)
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in data:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
                
    def check_memory(self,DB_PATH):
        self.ids.container.clear_widgets()
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID, Nombre, Enfermedad, Altura, Edad from Records')
        for i in cursor:
            wid = DataWid(self.mainwid)
            r1 = 'ID: '+str(100000000+i[0])[1:9]+'\n'
            r2 = i[1]+', '+i[2]+'\n'
            r3 = 'Precio por unidad: '+'$'+str(i[3])+'\n'
            r4 = 'En almacen: '+str(i[4])
            wid.data_id = str(i[0])
            wid.data = r1+r2+r3+r4
            self.ids.container.add_widget(wid)
        wid = NewDataButton(self.mainwid)
        self.ids.container.add_widget(wid)
        con.close()

    '''def check_memoryAlmacen(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'select Nombre, Marca, Costo, Almacen from Productos where ID='
        cursor.execute(s+self.data_id)
        for i in cursor:
            self.ids.ti_nombre.text = i[0]
            self.ids.ti_marca.text = i[1]
            self.ids.ti_costo.text = str(i[2])
            self.ids.ti_almacen.text = str(i[3])
        con.close()'''

    

    def update_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_nombre.text
        d2 = self.ids.ti_marca.text
        d3 = self.ids.ti_costo.text
        d4 = self.ids.ti_almacen.text
        a1 = (d1,d2,d3,d4)
        s1 = 'UPDATE Productos SET'
        s2 = 'Nombre="%s",Marca="%s",Costo=%s,Almacen=%s' % a1
        s3 = 'WHERE ID=%s' % self.data_id
        try:
            cursor.execute(s1+' '+s2+' '+s3)
            con.commit()
            con.close()
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
            con.close()

    def delete_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from productos where ID='+self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_database()

    '''def back_to_dbw(self):
        self.mainwid.goto_database()'''

class BuilderKv(ScreenManager):
    def __init__(self,**kwargs):
        super(BuilderKv,self).__init__()
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH+'/my_database.db'
        #self.DataBaseWid = DataBaseWid(self)
        #self.InsertDataWid = BoxLayout()
        #self.UpdateDataWid = BoxLayout()
        #self.Popup = MessagePopup()
        print("hola mundo")
        self.openApp()

    ''' wid = Screen(name='database')
        #wid.add_widget(self.DataBaseWid)
        #self.add_widget(wid)
        wid = Screen(name='insertdata')
        wid.add_widget(self.InsertDataWid)
        self.add_widget(wid)
        wid = Screen(name='updatedata')
        wid.add_widget(self.UpdateDataWid)
        self.add_widget(wid)
        self.goto_start()'''
        
    def openApp(self):
        myCarrier = CarrierKv()
        myCarrier.connect_to_database(self.DB_PATH,'create')
    
    
        #self.goto_database()
'''
    def goto_start(self):
        self.current = 'start'
        
    def goto_database(self):
        #self.DataBaseWid.check_memory()
        self.current = 'database'
        
    def goto_insertdata(self):
        #self.InsertDataWid.clear_widgets()
        #wid = InsertDataWid(self)
        #self.InsertDataWid.add_widget(wid)
        self.current = 'insertdata'

    def goto_updatedata(self,data_id):
        #self.UpdateDataWid.clear_widgets()
        #wid = UpdateDataWid(self,data_id)
        #self.UpdateDataWid.add_widget(wid)
        #self.current = 'updatedata'
    
    '''

class MessagePopup(Popup):
    pass