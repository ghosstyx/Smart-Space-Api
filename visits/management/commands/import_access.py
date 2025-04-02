import pyodbc
from django.core.management.base import BaseCommand
from visits.models import NaturalPerson
from visits.models import MarkTrack

class Command(BaseCommand):
    help = "Импорт данных из MS Access в Django"

    def handle(self, *args, **kwargs):
        db_path = r"C:\Program Files\web\сайты\smart-space-backend\att2000.mdb"
        conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("SELECT checkTime, checkType, id FROM CHECKINOUT;")

        for row in cursor.fetchall():
          try:
            person = NaturalPerson.objects.get(id=row.id)
            print(person)
            MarkTrack.objects.create(
                # id=row.id,
                checkTime=row.checkTime,
                checkType=row.checkType,
                person=person,
            )
          except:
              print(f"❌ Пользователь с ID {row.id} не найден!")
        conn.close()

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))






 # Вывод информации из базы данных
 #    conn = pyodbc.connect(
 #        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
 #        f"DBQ={db_path};"
 #    )
 #    cursor = conn.cursor()
 #
 #    # Пример запроса
 #    cursor.execute("SELECT * FROM schClass")
 #    for row in cursor.fetchall():
 #        print(row)
 #
 #    conn.close()