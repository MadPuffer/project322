import sys
import sqlite3

from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QApplication, QPushButton
from PyQt5 import uic
from PyQt5 import Qt

import design  # Это наш конвертированный файл дизайна


class ExampleApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.btnToRow = {}

        self.addBtn.clicked.connect(self.add_row)
        self.saveBtn.clicked.connect(self.save_table)

        self.second_fl_btn.clicked.connect(self.open_fl_table)
        self.third_fl_btn.clicked.connect(self.open_fl_table)
        self.fourth_fl_btn.clicked.connect(self.open_fl_table)
        self.fifth_fl_btn.clicked.connect(self.open_fl_table)

    def add_row(self):
        rowCount = self.residents_main_table.rowCount()
        self.residents_main_table.setRowCount(rowCount + 1)
        self.delete_btn = QPushButton("Удалить", self)
        self.delete_btn.clicked.connect(self.delete_row)
        self.btnToRow[self.delete_btn] = rowCount
        self.residents_main_table.setCellWidget(self.residents_main_table.rowCount() - 1, 10, self.delete_btn)

        ids = []
        for row in range(rowCount):
            ids.append(int(self.residents_main_table.item(row, 1).text()))
        max_id = max(ids) + 1
        self.residents_main_table.setItem(self.residents_main_table.rowCount() - 1, 1, QTableWidgetItem(str(max_id)))

    def save_table(self,):
        connection = sqlite3.connect('DataBase.sqlite')
        c = connection.cursor()

        for row in range(self.residents_main_table.rowCount()):
            writes = []
            for column in range(self.residents_main_table.columnCount()):
                writes.append(self.residents_main_table.item(row, column))

            room = int(writes[0].text())
            try:
                id = int(writes[1].text())
            except:
                id = -1
            name = writes[2].text()
            clas = int(writes[3].text())
            bc = writes[4].text()
            address = writes[5].text()
            dob = writes[6].text()
            st_num = writes[7].text()
            par_num = writes[8].text()
            try:
                status = writes[9].text()
            except:
                status = "-"

            request = f'SELECT * FROM "residents main table" WHERE room LIKE "{self.floor}%"'
            residents_main_table_items = c.execute(request).fetchall()
            isIn = False

            for i in residents_main_table_items:
                tableIds = []
                for j in range(self.residents_main_table.rowCount()):

                    tableIds.append(int(self.residents_main_table.item(j, 1).text()))
                if i[1] not in tableIds:
                    request = f'DELETE FROM "residents main table" WHERE id = {i[1]}'
                    c.execute(request)
                    print(i[1], tableIds)

                if id in i:
                    isIn = True
                    request = f"UPDATE 'residents main table' SET room = {room}, name = '{name}', class = {clas}, 'b/c' = '{bc}', address = '{address}', date_of_birth = '{dob}', st_num = '{st_num}', par_num = '{par_num}', status = '{status}' WHERE id = {id}"

            if not isIn:
                request = f"INSERT INTO 'residents main table' (room, id, name, class, 'b/c', address, date_of_birth, st_num, par_num, status) VALUES ({room}, {id}, '{name}', {clas}, '{bc}', '{address}', '{dob}', '{st_num}', '{par_num}', '{status}')"
            try:
                c.execute(request)
                connection.commit()
            except:
                print("error")

    def delete_row(self):
        self.residents_main_table.removeRow(self.btnToRow[self.sender()])
        request = f"DELETE FROM 'residents main table' WHERE id = 5"

    def open_fl_table(self):
        self.floor = self.sender().text().split()[0]
        connection = sqlite3.connect('DataBase.sqlite')
        c = connection.cursor()
        request = f'SELECT * FROM "residents main table" WHERE room LIKE "{self.floor}%"'
        residents_main_table_items = c.execute(request).fetchall()
        self.residents_main_table.setRowCount(len(residents_main_table_items))

        for row in range(len(residents_main_table_items)):
            for column in range(len(residents_main_table_items[row])):
                self.residents_main_table.setItem(row, column,
                                                  QTableWidgetItem(str(residents_main_table_items[row][column])))
            self.delete_btn = QPushButton("Удалить", self)
            self.delete_btn.clicked.connect(self.delete_row)
            self.btnToRow[self.delete_btn] = row
            self.residents_main_table.setCellWidget(row, len(residents_main_table_items[row]), self.delete_btn)

        c.close()
        self.residents_main_table.resizeColumnsToContents()


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
