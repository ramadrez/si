from fpdf import FPDF
from datetime import datetime

fecha_actual = datetime.now()

class PDF(FPDF):
        #funcion para modificar los encabezados
        def __init__(self, title="PATITAS JUNIN", report_title="Reporte General de Animales", rif="J411393550", *args, **kwargs):
            super().__init__(*args, **kwargs) 
            self.title = title
            self.report_title = report_title
            self.rif = rif

        def header(self):
            # Logo de kelly
            self.image('./media/Animal/logo-patitas.png', 10, 5, 55, 40, 'png')
            # Estilo de texto
            self.set_font('Arial', 'B', 18)
            # Mover para centrarlo
            # Titulo
            self.cell(0, 10, self.title, 0, 1, 'C')
            # Espaciado
            # Reporte general
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, self.report_title, 0, 1, 'C')
            # Fecha y hora
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10,f'Fecha-Hora: {fecha_actual.strftime("%d-%m-%Y %H:%M:%S")}', 0, 1, 'C')
            # RIF
            self.cell(0, 10, self.rif, 0, 1, 'C')
            # Espaciado

        # Page footer
        def footer(self):
            # Posicion no pegada al margen
            self.set_y(-15)
            # Estilo texto
            self.set_font('Arial', 'I', 8)
            # adquirir el numero de pagina
            self.cell(0, 10, 'N° Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

class PDF_animales(FPDF):
        #funcion para modificar los encabezados
        def __init__(self, title="PATITAS JUNIN", report_title="Reporte General de Animales", rif="J411393550",contador_perro=1,contador_gato=1, *args, **kwargs):
            super().__init__(*args, **kwargs) 
            self.title = title
            self.report_title = report_title
            self.rif = rif
            self.contador_perro = contador_perro
            self.contador_gato= contador_gato

        def header(self):
            # Logo de kelly
            self.image('./media/Animal/logo-patitas.png', 10, 5, 55, 40, 'png')
            # Estilo de texto
            self.set_font('Arial', 'B', 18)
            # Mover para centrarlo
            # Titulo
            self.cell(0, 10, self.title, 0, 1, 'C')
            # Espaciado
            # Reporte general
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, self.report_title, 0, 1, 'C')
            # Fecha y hora
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10,f'Fecha-Hora: {fecha_actual.strftime("%d-%m-%Y %H:%M:%S")}', 0, 1, 'C')
            # RIF
            self.cell(0, 10, self.rif, 0, 1, 'C')
            # Contadores
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10,f'Cantidad de perros: {self.contador_perro} Cantidad de Gatos: {self.contador_gato}', 0, 1, 'C')
            # Espaciado

        # Page footer
        def footer(self):
            # Posicion no pegada al margen
            self.set_y(-15)
            # Estilo texto
            self.set_font('Arial', 'I', 8)
            # adquirir el numero de pagina
            self.cell(0, 10, 'N° Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

class PDF_Ficha(FPDF):
    def header(self):
        # Logo de kelly
        self.image('./media/Animal/logo-patitas.png',  10, 10, 55, 40, 'png')
        # Estilo de texto
        self.set_font('Arial', 'B', 18)
        # Mover para centrarlo
        # Titulo
        self.cell(0, 10, 'PATITAS JUNIN', 0, 1, 'C')
        # Espaciado
        # Reporte general
        self.set_font('Arial', 'B', 14)
        self.cell(0, 8, 'Acta de Compromiso', 0, 1, 'C')
        # Fecha y hora
        self.set_font('Arial', 'B', 10)
        #self.cell(0, 10,f'Fecha-Hora: {fecha_actual.strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        # RIF
        self.cell(0, 10, 'RIF: 12809142', 0, 1, 'C')
        # Espaciado

    # Page footer
    def footer(self):
        # Posicion no pegada al margen
        self.set_y(-15)
        # Estilo texto
        self.set_font('Arial', 'I', 8)
        # adquirir el numero de pagina
        self.cell(0, 10, 'N° Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def pdf_sin_esterilizar(pdf,datos):
     # Ejecutar la clase
    
    pdf.alias_nb_pages()

    #funcion para declarar una pagina
    pdf.add_page()
    #texto formato
    pdf.set_font('arial', "B", 10)

    # Establecer color de relleno para los encabezados
    pdf.set_fill_color(246, 132, 46)
    # Establecer color de texto para los encabezados
    pdf.set_text_color(255, 255, 255)

    #celdas
    pdf.cell(w=30, h=15, txt='ID_Animal', border=1, align='C', fill=1)
    pdf.cell(w=30, h=15, txt='Nombre', border=1, align='C', fill=1)
    pdf.cell(w=35, h=15, txt='Fecha Nacimiento', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Especie', border=1, align='C', fill=1)
    pdf.cell(w=30, h=15, txt='Raza', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Esterilizacion', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Tamaño', border=1, align='C', fill=1)
    pdf.multi_cell(w=0, h=15, txt='Genero', border=1, align='C', fill=1)

    # Restablecer color de texto para el contenido
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('arial', "", 10)
    # Alternar color de fondo para las filas
    fill = False

    for i, dato in enumerate(datos, 1):
        # Establecer color de relleno para las filas alternas
        if fill:
            pdf.set_fill_color(240, 240, 240)  # Gris claro
        else:
            pdf.set_fill_color(255, 255, 255)  # Blanco

        #datos
        pdf.cell(w=30, h=8, txt=str(dato[0]), border=1, align='C', fill=1)
        pdf.cell(w=30, h=8, txt=dato[1], border=1, align='C', fill=1)
        pdf.cell(w=35, h=8, txt=dato[2].strftime('%Y-%m-%d'), border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=dato[3], border=1, align='C', fill=1)
        pdf.cell(w=30, h=8, txt=dato[4], border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=dato[5], border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=dato[6], border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=8, txt=dato[7], border=1, align='C', fill=1)

        # Alternar el valor de fill
        fill = not fill



def pdf_ficha (pdf,adopcion):
        
        pdf.alias_nb_pages()
        # Establecer márgenes
        pdf.set_left_margin(24.4)
        pdf.set_right_margin(24.5)
        pdf.set_top_margin(24.5)
            #funcion para declarar una pagina
        pdf.add_page()
        #texto formato
        pdf.set_font('arial', "B", 10)
        # Texto grande
        pdf.set_font('Arial', 'B', 14)
        #pdf.cell(0, 8, 'REUNIDOS', 0, 1, 'C')
        pdf.ln(3)  # Dejar una línea en blanco

        
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 8, f"El Dia {adopcion.Fecha}, como miembros de la organizacion PATITAS DE JUNIN, nos reunimos con el ciudadano {adopcion.Adoptante.name} {adopcion.Adoptante.ape} con la cedula de identidad {adopcion.Adoptante.ced}, y el teléfono {adopcion.Adoptante.tlf} con el fin de concretar el proceso de adopción de la mascota hoy en día conocida {adopcion.Animal.nom } bajo las siguientes estipulaciones:")
        
        #pdf.ln(10)  # Dejar una línea en blanco

        pdf.multi_cell(0, 8, '1.	El adoptante se compromete a proporcionar alimentación, atención veterinaria y un lugar estable para su bienestar')
        pdf.multi_cell(0, 8, '2.	El adoptante se compromete a no abandonar al animal en ninguna circunstancia y a devolverlo a la institución únicamente de sea necesario')
        pdf.multi_cell(0, 8, '3.	El adoptante se compromete a no poner en riesgo su integridad física y psicológica por fines personales como caza, reproducción masiva, experimentación, entre otros.')
        pdf.ln(3)  # Dejar una línea en blanco

        pdf.set_font('Arial', 'B', 14)
        #pdf.ln(10)  # Dejar una línea en blanco

        pdf.set_font('Arial', '', 12)
        pdf.set_fill_color(246, 132, 46)
        pdf.multi_cell(0, 8, 'Habiendo leído el acta de compromiso el adoptante se dispone a adoptar a la mascota con las siguientes características:')
        #pdf.cell(0, 8, '', 0, 1, 'C')
        pdf.ln(4)
        pdf.cell(w=100, h=10, txt=f'\tNOMBRE:\t {adopcion.Animal.nom }', border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt=f'\tESPECIE:\t {adopcion.Animal.fk_esp}', border=1, align='C', fill=0)
        pdf.cell(w=100, h=10, txt=f'\tFECHA NACIMIENTO:\t {adopcion.Animal.edad}', border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt=f'\tRAZA:\t {adopcion.Animal.raza}', border=1, align='C', fill=0)
        pdf.cell(w=100, h=10, txt=f'\tESTERILIZACION:\t {adopcion.Animal.fk_est}', border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt=f'\tTAMAÑO:\t {adopcion.Animal.fk_tam}', border=1, align='C', fill=0)
        pdf.multi_cell(w=100, h=10, txt=f'\tGENERO:\t {adopcion.Animal.fk_gen}', border=1, align='C', fill=0)
        pdf.ln(12)
        # Establecer color de relleno para los encabezados
        #pdf.set_fill_color(246, 132, 46)
        # Establecer color de texto para los encabezados
        #pdf.set_text_color(255, 255, 255)
        pdf.cell(w=85, h=10, txt='____________________', border=0, align='C', fill=0)
        pdf.multi_cell(w=80, h=10, txt='____________________', border=0, align='C', fill=0)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=85, h=7, txt=f'firma de {adopcion.Adoptante.name}', border=0, align='C', fill=0)
        pdf.multi_cell(w=80, h=7, txt='firma del Representante', border=0, align='C', fill=0)
        


def pdf_adoptantes(pdf,datos):
        pdf.alias_nb_pages()

        #funcion para declarar una pagina
        pdf.add_page()
        #texto formato
        pdf.set_font('arial', "B", 10)

        # Establecer color de relleno para los encabezados
        pdf.set_fill_color(246, 132, 46)
        # Establecer color de texto para los encabezados
        pdf.set_text_color(255, 255, 255)
        
        # Page footer
        def footer(self):
            # Posicion no pegada al margen
            self.set_y(-15)
            # Estilo texto
            self.set_font('Arial', 'I', 8)
            # adquirir el numero de pagina
            self.cell(0, 10, 'N° Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

        #celdas
        pdf.cell(w=60, h=15, txt='Cedula-Adoptante', border=1, align='C', fill=1)
        pdf.cell(w=60, h=15, txt='Nombre', border=1, align='C', fill=1)
        pdf.cell(w=60, h=15, txt='Apellido', border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=15, txt='Telefono', border=1, align='C', fill=1)

        # Restablecer color de texto para el contenido
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('arial', "", 12)
        # Alternar color de fondo para las filas
        fill = False

        for i, dato in enumerate(datos, 1):
            # Establecer color de relleno para las filas alternas
            if fill:
                pdf.set_fill_color(240, 240, 240)  # Gris claro
            else:
                pdf.set_fill_color(255, 255, 255)  # Blanco

            #datos
            pdf.cell(w=60, h=8, txt=dato[0], border=1, align='C', fill=1)
            pdf.cell(w=60, h=8, txt=dato[1], border=1, align='C', fill=1)
            pdf.cell(w=60, h=8, txt=dato[2], border=1, align='C', fill=1)
            pdf.multi_cell(w=0, h=8, txt=dato[3], border=1, align='C', fill=1)
            # Alternar el valor de fill
            fill = not fill

def pdf_adopciones(pdf,datos):
        pdf.alias_nb_pages()

        #funcion para declarar una pagina
        pdf.add_page()
        #texto formato
        pdf.set_font('arial', "B", 10)

        # Establecer color de relleno para los encabezados
        pdf.set_fill_color(246, 132, 46)
        # Establecer color de texto para los encabezados
        pdf.set_text_color(255, 255, 255)

        #celdas
        pdf.cell(w=25, h=15, txt='ID_Animal', border=1, align='C', fill=1)
        pdf.cell(w=25, h=15, txt='Nom.Animal', border=1, align='C', fill=1)
        pdf.cell(w=33, h=15, txt='Fecha Nacimiento', border=1, align='C', fill=1)
        pdf.cell(w=20, h=15, txt='Especie', border=1, align='C', fill=1)
        pdf.cell(w=20, h=15, txt='Genero', border=1, align='C', fill=1)
        pdf.set_fill_color(252, 140, 76)
        pdf.cell(w=25, h=15, txt='Cedula', border=1, align='C', fill=1)
        pdf.cell(w=26, h=15, txt='Nombre', border=1, align='C', fill=1)
        pdf.cell(w=26, h=15, txt='Apellido', border=1, align='C', fill=1)
        pdf.cell(w=27, h=15, txt='Telefono', border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=15, txt='Fecha Adoptiva', border=1, align='C', fill=1)

        

        # Restablecer color de texto para el contenido
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('arial', "", 10)
        # Alternar color de fondo para las filas
        fill = False

        for dato in datos:
            # Verificar que no haya valores None y reemplazarlos por cadenas vacías
            id_animal = str(dato[0]) if dato[0] is not None else ''
            nom_animal = str(dato[1]) if dato[1] is not None else ''
            fecha_nacimiento = dato[2].strftime('%Y-%m-%d') if dato[2] is not None else ''
            especie = str(dato[3]) if dato[3] is not None else ''
            genero = str(dato[4]) if dato[4] is not None else ''
            cedula = str(dato[5]) if dato[5] is not None else ''
            nombre = str(dato[6]) if dato[6] is not None else ''
            apellido = str(dato[7]) if dato[7] is not None else ''
            telefono = str(dato[8]) if dato[8] is not None else ''
            fecha_adoptiva = dato[9].strftime('%Y-%m-%d') if dato[9] is not None else ''

            # Establecer color de relleno para las filas alternas
            if fill:
                pdf.set_fill_color(240, 240, 240)  # Gris claro
            else:
                pdf.set_fill_color(255, 255, 255)  # Blanco

            # Añadir los datos a las celdas, asegurando que no haya valores None
            pdf.cell(w=25, h=8, txt=id_animal, border=1, align='C', fill=1)
            pdf.cell(w=25, h=8, txt=nom_animal, border=1, align='C', fill=1)
            pdf.cell(w=33, h=8, txt=fecha_nacimiento, border=1, align='C', fill=1)
            pdf.cell(w=20, h=8, txt=especie, border=1, align='C', fill=1)
            pdf.cell(w=20, h=8, txt=genero, border=1, align='C', fill=1)
            pdf.cell(w=25, h=8, txt=cedula, border=1, align='C', fill=1)
            pdf.cell(w=26, h=8, txt=nombre, border=1, align='C', fill=1)
            pdf.cell(w=26, h=8, txt=apellido, border=1, align='C', fill=1)
            pdf.cell(w=27, h=8, txt=telefono, border=1, align='C', fill=1)
            pdf.multi_cell(w=0, h=8, txt=fecha_adoptiva, border=1, align='C', fill=1)
            
            # Alternar el valor de fill
            fill = not fill

def pdf_voluntarios(pdf,datos):
        pdf.alias_nb_pages()

        #funcion para declarar una pagina
        pdf.add_page()
        #texto formato
        pdf.set_font('arial', "B", 10)

        # Establecer color de relleno para los encabezados
        pdf.set_fill_color(246, 132, 46)
        # Establecer color de texto para los encabezados
        pdf.set_text_color(255, 255, 255)

        #celdas
        pdf.cell(w=35, h=15, txt='Cedula', border=1, align='C', fill=1)
        pdf.cell(w=35, h=15, txt='Nombre', border=1, align='C', fill=1)
        pdf.cell(w=35, h=15, txt='Apellido', border=1, align='C', fill=1)
        pdf.cell(w=40, h=15, txt='Telefono', border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=15, txt='Correo', border=1, align='C', fill=1)
        

        # Restablecer color de texto para el contenido
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('arial', "", 10)
        # Alternar color de fondo para las filas
        fill = False


        for dato in datos:

            cedula = dato[0] if dato[0] is not None else ''
            nombre = dato[1] if dato[1] is not None else ''
            apellido = dato[2] if dato[2] is not None else ''
            telefono = dato[3] if dato[3] is not None else ''
            correo = dato[4] if dato[4] is not None else ''

            # Establecer color de relleno para las filas alternas
            if fill:
                pdf.set_fill_color(240, 240, 240)  # Gris claro
            else:
                pdf.set_fill_color(255, 255, 255)  # Blanco

            # Añadir datos a las celdas, asegurando que no haya valores None
            pdf.cell(w=35, h=8, txt=cedula, border=1, align='C', fill=1)
            pdf.cell(w=35, h=8, txt=nombre, border=1, align='C', fill=1)
            pdf.cell(w=35, h=8, txt=apellido, border=1, align='C', fill=1)
            pdf.cell(w=40, h=8, txt=telefono, border=1, align='C', fill=1)
            pdf.multi_cell(w=0, h=8, txt=correo, border=1, align='C', fill=1)
            #tomar en cuenta que faltan los contadores aqui
            # Alternar el valor de fill
            fill = not fill

def pdf_resguardo(pdf,datos):
    pdf.alias_nb_pages()

    #funcion para declarar una pagina
    pdf.add_page()
    #texto formato
    pdf.set_font('arial', "B", 10)

    # Establecer color de relleno para los encabezados
    pdf.set_fill_color(246, 132, 46)
    # Establecer color de texto para los encabezados
    pdf.set_text_color(255, 255, 255)

    #celdas
    pdf.cell(w=30, h=15, txt='ID_Animal', border=1, align='C', fill=1)
    pdf.cell(w=30, h=15, txt='Nombre', border=1, align='C', fill=1)
    pdf.cell(w=35, h=15, txt='Fecha Nacimiento', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Especie', border=1, align='C', fill=1)
    pdf.cell(w=30, h=15, txt='Raza', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Esterilizacion', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Tamaño', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Genero', border=1, align='C', fill=1)
    pdf.multi_cell(w=0, h=15, txt='CI_Cuidador', border=1, align='C', fill=1)

    # Restablecer color de texto para el contenido
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('arial', "", 10)
    # Alternar color de fondo para las filas
    fill = False
    
    for i, dato in enumerate(datos, 1):
        # Establecer color de relleno para las filas alternas
        if fill:
            pdf.set_fill_color(240, 240, 240)  # Gris claro
        else:
            pdf.set_fill_color(255, 255, 255)  # Blanco
        # Asegúrate de que los valores no sean None
        id_animal = str(dato[0]) if dato[0] is not None else ''
        nombre = str(dato[1]) if dato[1] is not None else ''
        fecha_nacimiento = dato[2].strftime('%Y-%m-%d') if dato[2] is not None else ''
        especie = str(dato[3]) if dato[3] is not None else ''
        raza = str(dato[4]) if dato[4] is not None else ''
        esterilizacion = str(dato[5]) if dato[5] is not None else ''
        tamaño = str(dato[6]) if dato[6] is not None else ''
        genero = str(dato[7]) if dato[7] is not None else ''
        ci_cuidador = str(dato[8]) if dato[8] is not None else ''

        # Datos
        pdf.cell(w=30, h=8, txt=id_animal, border=1, align='C', fill=1)
        pdf.cell(w=30, h=8, txt=nombre, border=1, align='C', fill=1)
        pdf.cell(w=35, h=8, txt=fecha_nacimiento, border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=especie, border=1, align='C', fill=1)
        pdf.cell(w=30, h=8, txt=raza, border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=esterilizacion, border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=tamaño, border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=genero, border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=8, txt=ci_cuidador, border=1, align='C', fill=1)

        # Alternar el valor de fill
        fill = not fill

def pdf_propio (pdf,datos):
    pdf.alias_nb_pages()

    #funcion para declarar una pagina
    pdf.add_page()
    #texto formato
    pdf.set_font('arial', "B", 10)

    # Establecer color de relleno para los encabezados
    pdf.set_fill_color(246, 132, 46)
    # Establecer color de texto para los encabezados
    pdf.set_text_color(255, 255, 255)

    #celdas
    pdf.cell(w=30, h=15, txt='ID_Animal', border=1, align='C', fill=1)
    pdf.cell(w=30, h=15, txt='Nombre', border=1, align='C', fill=1)
    pdf.cell(w=35, h=15, txt='Fecha Nacimiento', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Especie', border=1, align='C', fill=1)
    pdf.cell(w=30, h=15, txt='Raza', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Esterilizacion', border=1, align='C', fill=1)
    pdf.cell(w=25, h=15, txt='Tamaño', border=1, align='C', fill=1)
    pdf.multi_cell(w=0, h=15, txt='Genero', border=1, align='C', fill=1)

    # Restablecer color de texto para el contenido
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('arial', "", 10)
    # Alternar color de fondo para las filas
    fill = False

    for i, dato in enumerate(datos, 1):
        # Establecer color de relleno para las filas alternas
        if fill:
            pdf.set_fill_color(240, 240, 240)  # Gris claro
        else:
            pdf.set_fill_color(255, 255, 255)  # Blanco

        #datos
        pdf.cell(w=30, h=8, txt=str(dato[0]), border=1, align='C', fill=1)
        pdf.cell(w=30, h=8, txt=dato[1], border=1, align='C', fill=1)
        pdf.cell(w=35, h=8, txt=dato[2].strftime('%Y-%m-%d'), border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=dato[3], border=1, align='C', fill=1)
        pdf.cell(w=30, h=8, txt=dato[4], border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=dato[5], border=1, align='C', fill=1)
        pdf.cell(w=25, h=8, txt=dato[6], border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=8, txt=dato[7], border=1, align='C', fill=1)

        # Alternar el valor de fill
        fill = not fill