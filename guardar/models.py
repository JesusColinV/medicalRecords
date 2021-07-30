class Patient:
    nombres=''
    apellidoPaterno=''
    apellidoMaterno=''
    codigoPostal=''
    calle=''
    numero=''
    telefono=''
    correo=''

    def __init__(self, nombres, apellidoPaterno, apellidoMAterno, codigoPostal, calle, numero, telefono, correo):
        self.nombres = nombres
        self.apellidoPaterno= apellidoPaterno
        self.apellidoMaterno=apellidoMAterno
        self.codigoPostal=codigoPostal
        self.calle= calle
        self.numero= numero
        self.telefono= telefono
        self.correo= correo