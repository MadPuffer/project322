import xlrd
import sqlite3

from xlrd import xldate_as_datetime

connection = sqlite3.connect(input("DB name"))
c = connection.cursor()

request = "SELECT id from 'residents main table'"
ids = c.execute(request).fetchall()
try:
    max_id_for_session = max([int(i[0]) for i in ids])
except ValueError:
    max_id_for_session = 0

filename = input("Filename: ")
workbook = xlrd.open_workbook(filename)
worksheet = workbook.sheet_by_name(input("Sheet name: "))
count_of_rows = int(input("Row count: "))
count_of_columns = int(input("Column count: "))
all_rows = []
for row in range(2, count_of_rows):
    try:
        max_id_for_session += 1
        local_row = []
        for column in range(count_of_columns):
            if column in [1, 4]:
                continue
            elif column == 11:
                if worksheet.cell(row, column).value in ["1", "м", "М"]:
                    local_row.append("М")
                else:
                    local_row.append("Ж")
            elif column == 0:
                try:
                    local_row.append(str(int(worksheet.cell(row, column).value)))
                except ValueError:
                    local_row.append(worksheet.cell(row, column).value)
            elif column == 6:
                local_row.append(str(xldate_as_datetime(int(worksheet.cell(row, column).value), 0)).split()[0])
            else:
                local_row.append(str(worksheet.cell(row, column).value))
        if not local_row[0].isdigit():
            local_row[0] = all_rows[-1][0]
        if not local_row[2].split(".")[0].isdigit():
            local_row[2] = 0
        all_rows.append(local_row)
        print(local_row)

        try:
            request = f"INSERT INTO 'residents main table' (room, id, name, class, 'b/c', address, " \
                  f"date_of_birth, st_num, par_num, status, gender) VALUES ({local_row[0]}, {max_id_for_session}, " \
                  f"'{local_row[1]}', {local_row[2]}, '{local_row[3]}', '{local_row[4]}', '{local_row[5]}', '{int(local_row[6])}', " \
                  f"'{int(local_row[7])}', '{local_row[8]}', 'М')"
            c.execute(request)
        except ValueError:
            request = f"INSERT INTO 'residents main table' (room, id, name, class, 'b/c', address, " \
                      f"date_of_birth, st_num, par_num, status, gender) VALUES ({local_row[0]}, {max_id_for_session}, " \
                      f"'{local_row[1]}', {local_row[2]}, '{local_row[3]}', '{local_row[4]}', '{local_row[5]}', '{int(local_row[6].split('.')[0])}', " \
                      f"'{int(local_row[7].split('.')[0])}', '{local_row[8]}', 'М')"
            c.execute(request)
        print("Suc. executed!")
    except ValueError:
        pass


connection.commit()
connection.close()
