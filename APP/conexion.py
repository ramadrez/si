from django.db import connection

def ejecutar_consulta(consulta):
    with connection.cursor() as cursor:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
    return resultados

def consulta_pdf_propio(consulta,cedula):
    with connection.cursor() as cursor:
        cursor.execute(consulta,cedula)
        resultados = cursor.fetchall()
    return resultados
