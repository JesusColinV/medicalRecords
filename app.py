
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix import button
from kivymd.uix.picker import MDDatePicker
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
#from kivy.uix.scrollview import ScrollView
#from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
#from workers import CarrierKv, BuilderKv
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty,StringProperty
from kivy.uix.popup import Popup
import datetime
import sqlite3
import os
import uuid
from datetime import datetime as dt
try:
    from PaPDF import PaPDF
except:
    pass




Window.maximize()



class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

APP_PATH = os.getcwd()
DB_PATH = APP_PATH+'/my_database.db'

class Main(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.doctor= "MIGUEL DEMO"
        self.cedula = 'XXXXXX'
        self.especialidad = "Medicina General"
        self.ubicacion = "Toluca, Estado de México cp 50180"
        self.telefono = "7221184564"
        self.correo = "luzsoftwaremedico@gmail.com"
        self.connect_to_database(DB_PATH,'create')
        self.dicbackground={
            0:'Patologicos',
            1:'NoPatologicos',
            2:'hereditarios',
            3:'medicación',
            4:'alergias',
            5:'religion',
            6:'observaciones',
            }
        self.i_background = 0
        self.endRecordD = True
        self.endRecordP = True

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

    def Consultation(self):
        self.connect_to_database(DB_PATH,'newVisit')
    
    def Search(self):
        self.connect_to_database(DB_PATH,'consult')
    
    def Submit_backgound(self):
        self.connect_to_database(DB_PATH,'insertBackground')
    
    def load_backgound(self):
        self.connect_to_database(DB_PATH,'loadBackground')

    def load_record(self):
        self.connect_to_database(DB_PATH,'loadRecord')
    
    def load_patient(self):
        return self.connect_to_database(DB_PATH,'loadPatient')
        
        
    
    def titleBgNext(self):
        #dicbackground
        if self.i_background==6:
            self.i_background=0
        else:
            self.i_background = self.i_background+1
        self.ids.LabInputtypebg.text = self.dicbackground[self.i_background]

    def titleBgPrev(self):
        if self.i_background==0:
            self.i_background=6
        else:
            self.i_background = self.i_background-1
        self.ids.LabInputtypebg.text = self.dicbackground[self.i_background]


    def save_path(self):
        #self.connect_to_database(DB_PATH,'insertPat')
        IDCIE='001'
        InPAT=self.ids.txtInputPato.text
        #if self.data_table.column_data == None:

        if self.endRecordP == True:
            args=[[InPAT,IDCIE]]
            
            self.endRecordP = False
        else:
            args=[[pat,cie]for pat, cie in self.data_table_pato.row_data]
            args.append([InPAT,IDCIE])
        
        self.ids.table_box_pato.clear_widgets()
        self.data_table_pato = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.3,'center_y':0.4},
            size_hint = (1, 1),
            column_data=[(row,dp(30)) for row in ['Patologias','CIE']],
            row_data=[(row[0],row[1]) for row in args],
        )
        self.ids.table_box_pato.add_widget(self.data_table_pato)
        self.data_table_pato.bind(on_row_press = self.row_delete_pato)
        self.ids.txtInputPato.text=''

#error al eluiminar un valor
    def row_delete_pato(self,instance_table, instance_row):
        #print(instance_row.text)
        self.ids.table_box_pato.clear_widgets()
        args=[[pat,cie]for pat, cie in self.data_table_pato.row_data if pat is not instance_row.text]
        self.data_table_pato = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.3,'center_y':0.4},
            size_hint = (1, 1),
            column_data=[(row,dp(30)) for row in ['Patologias','CIE']],
            row_data=[(row[0],row[1]) for row in args],
        )
        self.ids.table_box_pato.add_widget(self.data_table_pato)

    def save_drug(self):
        InMED=self.ids.txtInputMed.text
        InUNIT=self.ids.txtInputUnit.text
        InFreq=self.ids.txtInputFreq.text
        if self.endRecordD == True:
            args=[[InMED,InUNIT,InFreq]]
            self.endRecordD = False
        else:
            args=[[med,unity,freq]for med,unity,freq in self.data_table_drugs.row_data]
            args.append([InMED,InUNIT,InFreq])
        

        self.ids.table_box_drugs.clear_widgets()
        self.data_table_drugs = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.3,'center_y':0.7},
            size_hint = (1 , 1),
            column_data=[(row,dp(40)) for row in ['Medicamento','Unidad','Frecuencia']],
            row_data=[(row[0],row[1],row[2]) for row in args],
        )
        self.data_table_drugs.height=500
        self.ids.table_box_drugs.add_widget(self.data_table_drugs)
        self.data_table_drugs.bind(on_row_press = self.row_delete_drugs)

        #self.connect_to_database(DB_PATH,'insertDrug')
        self.ids.txtInputMed.text=''
        self.ids.txtInputUnit.text=''
        self.ids.txtInputFreq.text=''

    def row_delete_drugs(self,instance_table, instance_row):
        #print(instance_row.text)
        self.ids.table_box_drugs.clear_widgets()
        args=[[med,unity,freq]for med,unity,freq in self.data_table_drugs.row_data if med is not instance_row.text and unity is not instance_row.text and freq is not instance_row.text]
        self.data_table_drugs = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.3,'center_y':0.7},
            size_hint = (1 , 1),
            column_data=[(row,dp(40)) for row in ['Medicamento','Unidad','Frecuencia']],
            row_data=[(row[0],row[1],row[2]) for row in args],
        )
        self.ids.table_box_drugs.add_widget(self.data_table_drugs)

    

    def mk_consultation(self):
        self.ids.idConsultation.text = str(uuid.uuid4())

    def connect_to_database(self,path,metod):
        try:
            con = sqlite3.connect(path)
            self.cursor = con.cursor()
            if metod == 'create':
                self.create_table_records()
                self.create_table_antecedent()
                self.create_table_agenda()
                self.create_table_consultation()
                self.create_table_patology()
                self.create_table_medication()
            elif metod == 'insert':
                self.insert_data_new()
            elif metod == 'consult':
                self.check_records()
            elif metod == 'view':
                self.get_data()
            elif metod == 'newVisit':
                self.insert_consultation()
            elif metod == 'insertPat':
                self.insert_patology()
            elif metod == 'insertDrug':
                self.insert_drugs()
            elif metod == 'insertBackground':
                self.insertBackground()
            elif metod == 'loadBackground':
                self.getBackground()
            elif metod == 'loadRecord':
                self.getRecord()
            elif metod == 'loadPatient':
                data = self.getDataPatient()
                con.commit()
                con.close()
                return data

                
                


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

    def create_table_records(self):
        try :
            
            self.cursor.execute('''create table if not exists Records(
                        ID_pat text,
                        fecha text,
                        nombre text,
                        snombre text,
                        aPaterno text,
                        aMaterno text,
                        sexo text,
                        fNacimiento text,
                        curp text)
                        ''')
        except Exception as e:
            print(e)

    def create_table_antecedent(self):
        try :
            self.cursor.execute(
                '''
                create table if not exists Antecedent(
                ID_patient      text,
                Antecedente     text,
                Descripción     text,
                Tipo            text,
                fecha           text,
                FOREIGN KEY (ID_patient) REFERENCES Records(ID_pat)
                )'''
            )
        except Exception as e:
            print(e)


    def create_table_agenda(self):
        try :
            self.cursor.execute(
                '''
                create table if not exists Agenda(
                ID_patient      text,
                ID_agenda       text,
                fecha           text,
                nacionalidad    text,
                postalCode      text,
                localidad       text,
                municipio       text,
                direccion       text,
                telefono        text,
                correo          text,
                faPaterno       text,
                faMaterno       text,
                faNombre        text,
                fasNombre       text,
                fTelefono       text,
                observaciones   text,
                FOREIGN KEY (ID_patient) REFERENCES Records(ID_pat)
                )'''
            )
        except Exception as e:
            print(e)
 

    def create_table_consultation(self):
        try :
            self.cursor.execute(
                '''
                create table if not exists Consultation(
                ID_patient          text,
                ID_consultation     text,
                fecha               text,
                altura              text,
                peso                text,
                tsistolica          text,
                tdiastolica         text,
                frecRespiratoria    text,
                estuLaboratorio     text,
                estuGabinete        text,
                observaciones       text,
                FOREIGN KEY (ID_patient) REFERENCES Records(ID_pat)
                )'''
            )
        except Exception as e:
            print(e)
  

    def create_table_patology(self):
        try :
            self.cursor.execute(
                '''
                create table if not exists Patology(
                ID_patient          text,
                ID_consultation     text,
                fecha               text,
                patologia           text,
                cie                 text,
                FOREIGN KEY (ID_patient) REFERENCES Records(ID_pat)
                )'''
            )
        except Exception as e:
            print(e)

    def create_table_medication(self):
        try :
            self.cursor.execute(
                '''
                create table if not exists Medication(
                ID_patient          text,
                ID_consultation     text,
                fecha               text,
                medicamento         text,
                unidad              text,
                frecuencia          text,
                FOREIGN KEY (ID_patient) REFERENCES Records(ID_pat)
                )'''
            )
        except Exception as e:
            print(e)
 
    def insert_data_new(self):
        # Records
        id_pat= (uuid.uuid4())
        inFN = self.ids.txtInputFirstName.text #1
        insN = self.ids.txtInputSecondName.text #2
        inSN = self.ids.txtInputSurName1.text #3
        inSN2 = self.ids.txtInputSurName2.text #4
        inSex = self.ids.txtInputSex.text #5
        inBi = self.ids.txtInputDate.text #6
        inCurp = self.ids.txtInputCurp.text #7

        # Agenda
        id_agenda= str(uuid.uuid4())
        inNati = self.ids.txtInputNati.text #1
        inCP = self.ids.txtInputCP.text #2
        inLoc = self.ids.txtInputLoc.text #3
        inMun = self.ids.txtInputMun.text #4
        inDir = self.ids.txtInputDir.text #5
        inPN = self.ids.txtInputPhoneNumber.text #6
        inEm = self.ids.txtInputEmail.text #7
        infFN = self.ids.txtInputfFirstName.text #8
        infsN = self.ids.txtInputfSecondName.text #9
        infSN = self.ids.txtInputfSurName1.text #10
        infSN2 = self.ids.txtInputfSurName2.text #11
        infPN=self.ids.txtInputfPhoneNumber.text #12
        InObs=self.ids.txtInputAgObsReg.text# 13
        inDate= str(datetime.datetime.today())
      

        dataRec = (id_pat,inDate,inFN,insN,inSN,inSN2,inSex,inBi,inCurp)
        dataAgenda = (id_agenda,id_pat,inDate,inNati,inCP,inLoc,inMun,inDir,inPN,inEm,infFN,infsN,infSN,infSN2,infPN,InObs)
        
        sRec1 = '''INSERT INTO Records(ID_pat,fecha,nombre,snombre,aPaterno,aMaterno,sexo,fNacimiento,curp)'''
        sRec2 = 'VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % dataRec
        
        sAgenda1 = '''INSERT INTO Agenda(ID_agenda,ID_patient,fecha,nacionalidad,postalCode,localidad, municipio,direccion,telefono,correo,faNombre, fasNombre, faPaterno, faMaterno, fTelefono,observaciones )'''
        sAgenda2 = 'VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % dataAgenda
        #self.ids.registerPage.clear_widgets()
        self.ids.txtInputFirstName.text = ''
        self.ids.txtInputSecondName.text = ''
        self.ids.txtInputSurName1.text = ''
        self.ids.txtInputSurName2.text = ''
        self.ids.txtInputSex.text = ''
        self.ids.txtInputDate.text = ''
        self.ids.txtInputCurp.text = ''
        self.ids.txtInputNati.text = ''
        self.ids.txtInputCP.text = ''
        self.ids.txtInputLoc.text = ''
        self.ids.txtInputMun.text = ''
        self.ids.txtInputDir.text = ''
        self.ids.txtInputEmail.text = ''
        self.ids.txtInputPhoneNumber.text = ''
        self.ids.txtInputfFirstName.text = ''
        self.ids.txtInputfSecondName.text = ''
        self.ids.txtInputfSurName1.text = ''
        self.ids.txtInputfSurName2.text = ''
        self.ids.txtInputfPhoneNumber.text = ''
        self.ids.txtInputAgObsReg.text = ''
        
        try:
            self.cursor.execute(sRec1+' '+sRec2)
            #self.cursor.execute("INSERT INTO Agenda VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", dataAgenda)
            self.cursor.execute(sAgenda1+' '+sAgenda2) #un valor de más revisar el codigo previo de menus
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
            use_pagination=True,
            pos_hint={'center_x':0.5,'center_y':0.5},
            size_hint = (0.9 , 0.6),
            column_data=[(row,dp(120)) for row in ['Lista de pacientes']],
            row_data=[tuple([row]) for row in args],
        )
        self.ids.table_box.add_widget(self.data_table)
        self.data_table.bind(on_row_press = self.row_check)

    def row_check(self,instance_table, instance_row):
        #print(instance_row.text)
        self.ids.screen_manager.current = "scrPacient"
        self.ids.LabPatientNom.text = str(instance_row.text)
        self.connect_to_database(DB_PATH,'view')

    def get_data(self):
        name = self.ids.LabPatientNom.text
        data=self.cursor.execute(f"SELECT ID_pat,sexo,fNacimiento FROM Records WHERE nombre LIKE '{name.split()[0]}' and aPaterno LIKE '{name.split()[-2]}' and aMaterno LIKE '{name.split()[-1]}'").fetchall()
        data=data[0]
        self.ids.LabPatientID.text=data[0]
        self.ids.LabPatientSex.text=data[1]
        self.ids.LabPatientBird.text=data[2]

        agenda_data=self.cursor.execute(f"SELECT * FROM Agenda WHERE ID_patient = '{data[0]}'").fetchall()
        agenda_data=agenda_data[-1]
        self.ids.txtInputNatAg.text=agenda_data[3]
        self.ids.txtInputCPAg.text=agenda_data[4]
        self.ids.txtInputLocAg.text=agenda_data[5]
        self.ids.txtInputmunAg.text=agenda_data[6]
        self.ids.txtInputDireAg.text=agenda_data[7]
        self.ids.txtInputTel.text=agenda_data[8]
        self.ids.txtInputEmailAg.text=agenda_data[9]
        self.ids.txtInputSurNameFam.text=agenda_data[10]
        self.ids.txtInputSecSurNameFam.text=agenda_data[11]
        self.ids.txtInputNameFam.text=agenda_data[12]
        self.ids.txtInputsNameFam.text=agenda_data[13]
        self.ids.txtInputPNfam.text=agenda_data[14]
        self.ids.txtInputObsAg.text=agenda_data[15]
    
    
    def insertBackground(self):
        IDPatient = self.ids.LabPatientID.text
        AntecBg = self.ids.LabInputBackground.text
        DescrBg = self.ids.LabInputDescriptionBg.text
        TypeBg = self.ids.LabInputtypebg.text
        inDate= str(datetime.datetime.today())

        #dataRec=[IDPatient,AntecBg,DescrBg,TypeBg,inDate]
        sBG1 = '''INSERT INTO Antecedent(ID_patient,Antecedente,Descripción,Tipo,fecha)'''
        sBG2 = 'VALUES("%s","%s","%s","%s","%s")' % (IDPatient,AntecBg,DescrBg,TypeBg,inDate)

        self.ids.LabInputBackground.text = ''
        self.ids.LabInputDescriptionBg.text = ''

        try:
            self.cursor.execute(sBG1+' '+sBG2)
        except Exception as e:
            print(e)


    def getBackground(self):
        IDPatient = self.ids.LabPatientID.text
        TypeBg = self.ids.LabInputtypebg.text
        data=self.cursor.execute(f"SELECT Antecedente,Descripción FROM Antecedent WHERE ID_patient = '{IDPatient}' and Tipo = '{TypeBg}'").fetchall()
        
        
        self.ids.table_box_background.clear_widgets()
        self.data_table_background = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.3,'center_y':0.4},
            size_hint = (1, 1),
            column_data=[(row,dp(30)) for row in [f'{TypeBg}','Descripción']],
            row_data=data,
        )
        self.ids.table_box_background.add_widget(self.data_table_background)
        self.data_table_background.bind(on_row_press = self.row_delete_background)
    
    def getRecord(self):
        IDPatient = self.ids.LabPatientID.text
        data=self.cursor.execute(f"SELECT * FROM Consultation WHERE ID_patient = '{IDPatient}' ").fetchall()
        #drow=[]
        col=[]
        for i in range(len(data)):
            
            id=data[i][1]
            #col.append(data[i][2])
            
            dataid=self.cursor.execute(f"SELECT medicamento, unidad, frecuencia FROM Medication WHERE ID_patient = '{IDPatient}' and ID_consultation = '{id}'").fetchall()
            for d in dataid:
                col.append((data[i][2],d[0]))
            #dataid=self.cursor.execute(f"SELECT patologia FROM Patology WHERE ID_patient = '{IDPatient}' and ID_consultation = '{id}' ").fetchall()
            #for d in dataid:
            #    col.append(d[0])
            #drow.append(col)
                           
        self.ids.table_box_record.clear_widgets()
        self.data_table_record = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.5,'center_y':0.8},
            size_hint = (1, 1),
            column_data=[(row,dp(70)) for row in [f'Fecha','Patologia']],
            row_data=col,
        )
        self.ids.table_box_record.add_widget(self.data_table_record)
        # self.data_table_record.bind(on_row_press = self.row_delete_record)


    def row_delete_background(self,instance_table, instance_row):
        pass
        '''typeBG='Hereditario'
        print(instance_row.text)
        self.ids.table_box_background.clear_widgets()
        args=[[inbg,cie]for inbg, cie in self.data_table_background.row_data if pat is not instance_row.text]
        self.data_table_background = MDDataTable(
            use_pagination=True,
            pos_hint={'center_x':0.3,'center_y':0.4},
            size_hint = (1, 1),
            column_data=[(row,dp(30)) for row in [f'{typeBG}','CIE']],
            row_data=[(row[0],row[1]) for row in args],
        )
        self.ids.table_box_pato.add_widget(self.data_table_background)'''

    def receta(self):
        print(self.doctor)
        path = 'metadata/recetaD.jpg'

        
        record_data = self.load_patient()
        genero = record_data[0][6]
        nombre = record_data[0][2] + record_data[0][3] + record_data[0][4] + record_data[0][5]
        peso = self.ids.txtInputWeight.text
        edad = datetime.datetime.today().year -  dt.strptime(record_data[0][7], "%Y-%m-%d").year
        talla = self.ids.txtInputHeight.text
        diagnostico = self.data_table_pato.row_data
        prescripcion = self.data_table_drugs.row_data
        recomendaciones = self.ids.txtInputObsCon.text
        doctor = self.doctor
        cedula = self.cedula
        especialidad = self.especialidad
        ubicacion = self.ubicacion
        telefono = self.telefono
        correo = self.correo

        # agregar registro de patologias y medicamentos

        #InTAS=self.ids.txtInputTAS.text
        #InTAD=self.ids.txtInputTAD.text
        #InFR=self.ids.txtInputFR.text

 

        
        with PaPDF(f"{datetime.datetime.today()}.pdf") as pdf:
            pdf.addImage(path, 0, 0, 210, 300)
            # pdf.addTrueTypeFont('SourceSansPro-Regular','SourceSansPro-Regular.ttf')
            # pdf.setFont('SourceSansPro-Regular')
            pdf.setFontSize(8)
            pdf.addText(12, 232, '{}'.format(str(datetime.datetime.today())))
            pdf.addText(105, 232, '{}'.format(genero))
            pdf.addText(12, 218, '{}'.format(nombre))
            pdf.addText(105, 218, '{}'.format(peso))
            pdf.addText(12, 200, '{}'.format(edad))
            pdf.addText(105, 200, '{}'.format(talla))
            m=179
            for i in range(len(diagnostico)):
                pdf.addText(14, m, '{}'.format(diagnostico[i][0]))
                m=m-10

            n=135
            for i in range(len(prescripcion)):
                pdf.addText(14, n, '{}'.format(f"{prescripcion[i][0]} tomar {prescripcion[i][1]} unidades cada {prescripcion[i][2]} hrs "))
                n=n-10

            pdf.addText(14, 90, '{}'.format(recomendaciones)) # tenia 99
            pdf.setFontSize(14)
            pdf.addText(120, 275, 'Dr. {}'.format(doctor))

            pdf.addText(120, 270, f'Cedula: {cedula}')
            pdf.addText(120, 265, f'Especialidad: {especialidad}')
            pdf.addText(12, 35, f'dirección: {ubicacion}')
            pdf.addText(12, 30, f'cel: {telefono}')
            pdf.addText(12, 25, f'email: {correo}')
        
    
    def getDataPatient(self):
        agenda_data=self.cursor.execute(f"SELECT * FROM Records WHERE ID_pat = '{self.ids.LabPatientID.text}'").fetchall()
        return agenda_data

    def insert_consultation(self):
        ID_patient = self.ids.LabPatientID.text
        fecha= str(datetime.datetime.today())
        InHeight=self.ids.txtInputHeight.text
        InWeight=self.ids.txtInputWeight.text
        InTAS=self.ids.txtInputTAS.text
        InTAD=self.ids.txtInputTAD.text
        InFR=self.ids.txtInputFR.text
        InEL=self.ids.txtInputEL.text
        InEG=self.ids.txtInputEG.text
        InObs=self.ids.txtInputObsCon.text

        ID_consultation = self.ids.idConsultation.text
        dataConsult = (ID_patient,ID_consultation,fecha,InHeight,InWeight,InTAS,InTAD,InFR,InEL,InEG,InObs)
        sCon1 = '''INSERT INTO Consultation(ID_patient,ID_consultation,fecha,altura,peso,tsistolica,tdiastolica,frecRespiratoria,estuLaboratorio,estuGabinete,observaciones)'''
        sCon2 = 'VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % dataConsult
        self.receta()
        self.ids.txtInputHeight.text= ''
        self.ids.txtInputWeight.text= ''
        self.ids.txtInputTAS.text= ''
        self.ids.txtInputTAD.text= ''
        self.ids.txtInputFR.text= ''
        self.ids.txtInputEL.text= ''
        self.ids.txtInputEG.text= ''
        self.ids.txtInputObsCon.text = ''
        self.endRecordD = True
        self.endRecordP = True
        self.insert_patology()
        self.insert_drugs()
        
        try:
            self.cursor.execute(sCon1+' '+sCon2)
        except Exception as e:
            print(e)
        

    def insert_patology(self):
        ID_patient = self.ids.LabPatientID.text
        ID_consultation = self.ids.idConsultation.text
        fecha= str(datetime.datetime.today())
        IDCIE='001'
        try:
            args=[[pato,cie]for pato,cie in self.data_table_pato.row_data]
            #InPAT=self.ids.txtInputPato.text
            for  i in range(len(args)):
                dataPatology = (ID_patient,ID_consultation,fecha,args[i][0],args[i][1])
                sPatology1 = '''INSERT INTO Patology(ID_patient,ID_consultation,fecha,cie,patologia)'''
                sPatology2 = 'VALUES("%s","%s","%s","%s","%s")' % dataPatology
                try:
                    self.cursor.execute(sPatology1 +' '+sPatology2)
                    #self.update_table_pato(*dataPatology[3:])
                except Exception as e:
                    print(e)
        except:
            print('no hay patologia')
            dataPatology = (ID_patient,ID_consultation,fecha,'None','None')
            sPatology1 = '''INSERT INTO Patology(ID_patient,ID_consultation,fecha,cie,patologia)'''
            sPatology2 = 'VALUES("%s","%s","%s","%s","%s")' % dataPatology
            try:
                self.cursor.execute(sPatology1 +' '+sPatology2)
                #self.update_table_pato(*dataPatology[3:])
            except Exception as e:
                print(e)
        self.ids.txtInputPato.text= ''
        self.ids.table_box_pato.clear_widgets()
        #self.data_table_pato = MDDataTable(
        #    use_pagination=True,
        #    pos_hint={'center_x':0.3,'center_y':0.4},
        #    size_hint = (1, 1),
        #    column_data=[(row,dp(30)) for row in ['Patologias','CIE']],
        #    row_data=[('','')],
        #)
        #self.remove_widget(self.ids.table_box_pato)

    def insert_drugs(self):
        ID_patient = self.ids.LabPatientID.text
        ID_consultation = self.ids.idConsultation.text

        fecha= str(datetime.datetime.today())
        try:
            args=[[med,unity,freq]for med,unity,freq in self.data_table_drugs.row_data]
            #InMED=self.ids.txtInputMed.text
            #InUNIT=self.ids.txtInputUnit.text
            #InFreq=self.ids.txtInputFreq.text
            for  i in range(len(args)):
                dataDrugs = (ID_patient,ID_consultation,fecha,args[i][0],args[i][1],args[i][2])
                sDrug1 = '''INSERT INTO Medication(ID_patient,ID_consultation,fecha,medicamento,unidad,frecuencia)'''
                sDrug2 = 'VALUES("%s","%s","%s","%s","%s","%s")' % dataDrugs
                try:
                    self.cursor.execute(sDrug1 +' '+sDrug2)
                    #self.update_table_drugs(*dataDrugs[3:])
                except Exception as e:
                    print(e)
        except:
            print('no hay medicamentos')
            dataDrugs = (ID_patient,ID_consultation,fecha,'None','None','None')
            sDrug1 = '''INSERT INTO Medication(ID_patient,ID_consultation,fecha,medicamento,unidad,frecuencia)'''
            sDrug2 = 'VALUES("%s","%s","%s","%s","%s","%s")' % dataDrugs
            try:
                self.cursor.execute(sDrug1 +' '+sDrug2)
                #self.update_table_drugs(*dataDrugs[3:])
            except Exception as e:
                print(e)
        self.ids.txtInputMed.text= ''
        self.ids.txtInputUnit.text= ''
        self.ids.txtInputFreq.text= ''
        self.ids.table_box_drugs.clear_widgets()
        #self.data_table_drugs = MDDataTable(
        #    use_pagination=True,
        #    pos_hint={'center_x':0.3,'center_y':0.7},
        #    size_hint = (1 , 1),
        #    column_data=[(row,dp(40)) for row in ['Medicamento','Unidad','Frecuencia']],
        #    row_data=[('','','') ],
        #)
        #self.remove_widget(self.ids.table_box_drugs)

        
class Content(MDBoxLayout):
    '''Custom content.'''

class MessagePopup(Popup):
    pass

class RegisterPage(StackLayout):
    pass
 


class App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.icon ="C:\\Users\\ASUS\\Desktop\\clone\\KivyMD\\LUZ2.0\\metadata\\LOGO.png"
        self.title = 'LUZ Software Médico'
        return Main()

if __name__=='__main__':
    App().run()