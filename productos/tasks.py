from celery import shared_task
from time import sleep

@shared_task
def estado_tarea(id_consulta):
    print(f"Estado de la tarea: {id_consulta}")
    sleep(5)
    print(f"Finalizo la tarea: {id_consulta}")
    return 'Finalizo la aejecución de la tarea'