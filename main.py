import os
import sys
import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QApplication, QPushButton, QFileDialog, QWidget, \
    QInputDialog, QMessageBox
from PyQt5 import uic
from datetime import date
import xlwt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowTitle(f"Residents")

        self.btnToRow = {}
        self.idsToDelete = set()
        self.residents_main_table.setVisible(False)
        self.data_base = "DataBase.sqlite"
        self.maxId = 0
        self.floor = -1
        self.backUpRows = []
        self.is_table_saved = True

        self.open_fl_table(1, False)

        self.second_fl_btn.clicked.connect(self.open_fl_table)
        self.first_fl_btn.clicked.connect(self.open_fl_table)
        self.third_fl_btn.clicked.connect(self.open_fl_table)
        self.fourth_fl_btn.clicked.connect(self.open_fl_table)
        self.fifth_fl_btn.clicked.connect(self.open_fl_table)

        self.stat_btn.clicked.connect(self.show_statistic)
        self.evicted_btn.clicked.connect(self.show_evicted)

        self.addRowAction.triggered.connect(self.add_row)
        self.printAction.triggered.connect(self.table_to_excel)
        self.openAction.triggered.connect(self.open_file)
        self.saveAction.triggered.connect(self.save_table)
        self.backupRowAction.triggered.connect(self.backup_row)
        self.createDataBaseAction.triggered.connect(self.create_new_database)

        self.addRowAction.setShortcut('Ctrl+N')
        self.openAction.setShortcut('Ctrl+O')
        self.saveAction.setShortcut('Ctrl+S')

        self.setStyleSheet('''
            #first_fl_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }#second_fl_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #third_fl_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #fourth_fl_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #fifth_fl_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #stat_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #evicted_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            
            #first_fl_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }#second_fl_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #third_fl_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #fourth_fl_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #fifth_fl_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #stat_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #evicted_btn::focus {
                background-color: #b3bfc4;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
                        
            #delete_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            
            #throw_out_btn {
                background-color: #217346;
                color: #ffffff;
                font: 100 10pt "Microsoft YaHei UI";
                border-style: solid;
            }
            QTableView::item::selected {border: 2px solid green; border-radius: 0px;border-bottom-right-radius: 0px;
            border-style: solid;color: black;}
            QTableView::item::focus {border: 2px solid green; border-radius: 0px;border-bottom-right-radius: 0px;
            border-style: solid;color: black;}}
        ''')

    def table_to_excel(self):
        rows = []
        writes = []
        for column in range(self.residents_main_table.columnCount() - 2):
            if column != 1:
                writes.append(self.residents_main_table.horizontalHeaderItem(column))
        rows.append(writes)
        for row in range(self.residents_main_table.rowCount()):
            writes = []
            for column in range(self.residents_main_table.columnCount() - 2):
                if column != 1:
                    writes.append(self.residents_main_table.item(row, column))
            rows.append(writes)
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("Sheet")
        for row in range(len(rows)):
            for column in range(len(rows[row])):
                sheet.write(row, column, rows[row][column].text())
        book.save("readyToPrint.xls")
        os.startfile("readyToPrint.xls", "print")

    def show_save_warning(self):
        return QMessageBox.question(self, "Предупреждение", "Сохранить изменения в таблице?", QMessageBox.Yes |
                                    QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

    def create_new_database(self):
        text, ok = QInputDialog.getText(self, 'Создание БД',
                                        'Введите название БД')

        if ok:
            self.data_base = f"{text}.sqlite"
        else:
            return None
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()
        c.execute('''
            create table "residents main table"
                (room int, id int, name text, class int,      
                   "b/c" char,
                   address text,
                   date_of_birth text,
                   st_num text,
                   par_num text,
                   status text default '-',
                   gender text,
                   isEvicted int default 0,
                   date_of_eviction text
                )
        ''')

        self.open_fl_table(1)

        connection.commit()
        c.close()

    def evict_row(self):
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()

        row = self.residents_main_table.indexFromItem(self.btnToRow[self.sender()]).row()
        writes = []
        for i in range(self.residents_main_table.columnCount()):
            writes.append(self.residents_main_table.item(row, i))
        id = int(writes[1].text())
        datetime = date.today().strftime("%d/%m/%Y")

        request = f"UPDATE 'residents main table' SET isEvicted = 1, date_of_eviction = '{datetime}' WHERE id = {id}"

        c.execute(request)
        c.close()

        self.residents_main_table.removeRow(row)

        self.is_table_saved = False

    def show_evicted(self, *args):
        if False not in args or not self.is_table_saved:
            is_need_to_save = self.show_save_warning()
            if is_need_to_save == QMessageBox.Yes:
                self.save_table()
            elif is_need_to_save == QMessageBox.Cancel:
                return None

        self.addRowAction.setDisabled(True)
        self.backupRowAction.setDisabled(True)

        self.residents_main_table.setVisible(True)
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()
        request = f'SELECT room, id, name, class, "b/c", address, date_of_birth, st_num, par_num, status, gender, ' \
                  f'date_of_eviction FROM "residents main table" WHERE isEvicted = 1'
        evicted_residents = c.execute(request).fetchall()
        self.residents_main_table.setRowCount(0)
        self.residents_main_table.setRowCount(len(evicted_residents))
        self.residents_main_table.setHorizontalHeaderItem(self.residents_main_table.columnCount() - 2,
                                                          QTableWidgetItem("Дата выселения"))
        self.residents_main_table.setHorizontalHeaderItem(self.residents_main_table.columnCount() - 1,
                                                          QTableWidgetItem("Удалить"))

        for row in range(len(evicted_residents)):
            for column in range(len(evicted_residents[row])):
                self.residents_main_table.setItem(row, column,
                                                  QTableWidgetItem(str(evicted_residents[row][column])))
            self.delete_btn = QPushButton("Удалить", self)
            self.delete_btn.clicked.connect(self.delete_row)
            self.btnToRow[self.delete_btn] = self.residents_main_table.item(row, 1)
            self.residents_main_table.setCellWidget(row, len(evicted_residents[row]), self.delete_btn)

        for row in range(len(evicted_residents)):
            self.residents_main_table.setItem(row, 11, QTableWidgetItem(str(evicted_residents[row][11])))

        self.residents_main_table.resizeColumnsToContents()
        c.close()

        self.is_table_saved = True

    def show_statistic(self, *args):
        if False not in args or not self.is_table_saved:
            is_need_to_save = self.show_save_warning()
            if is_need_to_save == QMessageBox.Yes:
                self.save_table()
            elif is_need_to_save == QMessageBox.Cancel:
                return None

        self.stat_window = Statistic(self.data_base)
        self.stat_window.show()

        self.is_table_saved = True

    def open_file(self):
        selected_filter = "DataBase (*.sqlite)"
        fileName = QFileDialog.getOpenFileName(self, " Выберите Базу Данных ", os.getcwd(), selected_filter)
        self.data_base = fileName[0]
        self.setWindowTitle(f"Residents - {self.data_base}")

    def add_row(self):
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()
        request = "SELECT id from 'residents main table'"
        ids = c.execute(request).fetchall()
        try:
            max_id_for_session = max([int(i[0]) for i in ids])
        except ValueError:
            max_id_for_session = 0
        if self.maxId <= max_id_for_session:
            self.maxId = max_id_for_session + 1
        ids = []
        for i in range(self.residents_main_table.rowCount()):
            ids.append(int(self.residents_main_table.item(i, 1).text()))
        if self.maxId in ids:
            self.maxId = max(ids) + 1

        rowCount = self.residents_main_table.rowCount()
        self.residents_main_table.setRowCount(rowCount + 1)
        self.delete_btn = QPushButton("Удалить", self)
        self.delete_btn.clicked.connect(self.delete_row)
        self.residents_main_table.setCellWidget(rowCount, 11, self.delete_btn)

        self.residents_main_table.setItem(self.residents_main_table.rowCount() - 1, 1,
                                          QTableWidgetItem(str(self.maxId)))

        self.throw_out = QPushButton("Выселить", self)
        self.throw_out.clicked.connect(self.evict_row)
        self.btnToRow[self.throw_out] = self.residents_main_table.item(rowCount, 1)
        self.residents_main_table.setCellWidget(rowCount, self.residents_main_table.columnCount() - 1, self.throw_out)
        self.btnToRow[self.delete_btn] = self.residents_main_table.item(rowCount, 1)

        self.residents_main_table.setItem(rowCount, 0, QTableWidgetItem(self.floor))

        self.backUpRows = []
        self.is_table_saved = False

    def save_table(self, ):
        if self.floor == -1:
            return None
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()

        for i in self.idsToDelete:
            c.execute(f'DELETE FROM "residents main table" WHERE id = {i}')
        connection.commit()

        for row in range(self.residents_main_table.rowCount()):
            writes = []
            for column in range(self.residents_main_table.columnCount()):
                writes.append(self.residents_main_table.item(row, column))

            try:
                room = int(writes[0].text())
            except:
                room = self.floor

            id = int(writes[1].text())
            try:
                name = writes[2].text()
            except:
                name = " "
            try:
                clas = int(writes[3].text())
            except:
                clas = 0
            try:
                bc = writes[4].text().upper()
            except:
                bc = ""
            try:
                address = writes[5].text()
            except:
                address = ""
            try:
                dob = writes[6].text()
            except:
                dob = ""
            try:
                st_num = writes[7].text()
            except:
                st_num = ""
            try:
                par_num = writes[8].text()
            except:
                par_num = ""
            try:
                status = writes[9].text()
            except:
                status = "-"
            try:
                gender = writes[10].text().upper()
            except:
                gender = ""

            request = f'SELECT room, id, name, class, "b/c", address, date_of_birth, st_num, par_num, ' \
                      f'status, gender FROM "residents main table" WHERE room LIKE "{self.floor}%"'
            residents_main_table_items = c.execute(request).fetchall()
            isIn = False

            for i in residents_main_table_items:
                if id in i:
                    isIn = True
                    request = f"UPDATE 'residents main table' SET room = {room}, name = '{name}', class = {clas}," \
                              f" 'b/c' = '{bc}', address = '{address}', date_of_birth = '{dob}', st_num = '{st_num}'," \
                              f" par_num = '{par_num}', status = '{status}', gender = '{gender}' WHERE id = {id}"
            if not isIn:
                request = f"INSERT INTO 'residents main table' (room, id, name, class, 'b/c', address, " \
                          f"date_of_birth, st_num, par_num, status, gender) VALUES ({room}, {id}, " \
                          f"'{name}', {clas}, '{bc}', '{address}', '{dob}', '{st_num}', " \
                          f"'{par_num}', '{status}', '{gender}')"
            try:
                c.execute(request)
            except:
                print("error")

        self.is_table_saved = True

        connection.commit()
        c.close()
        self.open_fl_table(self.floor, False)

    def backup_row(self):
        if not self.backUpRows:
            return None
        row = self.residents_main_table.rowCount()
        self.residents_main_table.setRowCount(row + 1)
        for i in range(self.residents_main_table.columnCount() - 2):
            self.residents_main_table.setItem(row, i, QTableWidgetItem(self.backUpRows[-1][i]))
        self.backUpRows.remove(self.backUpRows[-1])

        self.delete_btn = QPushButton("Удалить", self)
        self.delete_btn.clicked.connect(self.delete_row)
        self.residents_main_table.setCellWidget(row, 11, self.delete_btn)

        self.throw_out = QPushButton("Выселить", self)
        self.throw_out.clicked.connect(self.evict_row)
        self.btnToRow[self.throw_out] = self.residents_main_table.item(row, 1)
        self.residents_main_table.setCellWidget(row, self.residents_main_table.columnCount() - 1, self.throw_out)
        self.btnToRow[self.delete_btn] = self.residents_main_table.item(row, 1)

        self.is_table_saved = False

    def delete_row(self):
        row = self.residents_main_table.indexFromItem(self.btnToRow[self.sender()]).row()

        rowData = []
        for i in range(self.residents_main_table.columnCount() - 2):
            try:
                rowData.append(self.residents_main_table.item(row, i).text())
            except AttributeError:
                if i == 3:
                    rowData.append("0")
                else:
                    rowData.append("")
        self.backUpRows.append(rowData)

        self.idsToDelete.add(int(self.residents_main_table.item(row, 1).text()))
        self.residents_main_table.removeRow(row)

        self.is_table_saved = False

    def open_fl_table(self, *args):
        if False not in args or not self.is_table_saved:
            is_need_to_save = self.show_save_warning()
            if is_need_to_save == QMessageBox.Yes:
                self.save_table()
            elif is_need_to_save == QMessageBox.Cancel:
                return None

        self.saveAction.setDisabled(False)
        self.addRowAction.setDisabled(False)
        self.backupRowAction.setDisabled(False)

        if args[0]:
            self.floor = args[0]
        else:
            self.floor = self.sender().text().split()[0]
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()
        request = f'SELECT room, id, name, class, "b/c", address, date_of_birth, st_num, par_num, status, gender ' \
                  f'FROM "residents main table" WHERE room LIKE "{self.floor}%" AND isEvicted = 0'
        residents_main_table_items = c.execute(request).fetchall()
        self.residents_main_table.setRowCount(0)
        self.residents_main_table.setRowCount(len(residents_main_table_items))
        self.residents_main_table.showColumn(self.residents_main_table.columnCount() - 1)
        self.residents_main_table.setHorizontalHeaderItem(self.residents_main_table.columnCount() - 1,
                                                          QTableWidgetItem("Выселить"))
        self.residents_main_table.setHorizontalHeaderItem(self.residents_main_table.columnCount() - 2,
                                                          QTableWidgetItem("Удалить"))

        for row in range(len(residents_main_table_items)):
            for column in range(len(residents_main_table_items[row])):
                self.residents_main_table.setItem(row, column,
                                                  QTableWidgetItem(str(residents_main_table_items[row][column])))
            self.delete_btn = QPushButton("Удалить", self)
            self.delete_btn.clicked.connect(self.delete_row)
            self.btnToRow[self.delete_btn] = self.residents_main_table.item(row, 1)
            self.residents_main_table.setCellWidget(row, len(residents_main_table_items[row]), self.delete_btn)

            self.throw_out = QPushButton("Выселить", self)
            self.throw_out.clicked.connect(self.evict_row)
            self.btnToRow[self.throw_out] = self.residents_main_table.item(row, 1)
            self.residents_main_table.setCellWidget(row, len(residents_main_table_items[row]) + 1, self.throw_out)

        c.close()
        self.residents_main_table.resizeColumnsToContents()
        self.residents_main_table.setVisible(True)

        self.is_table_saved = True


class Statistic(QWidget):
    def __init__(self, data_base):
        super(Statistic, self).__init__()
        uic.loadUi('statisticWidget.ui', self)
        self.data_base = data_base

        self.refresh_btn.clicked.connect(self.refresh_table)

    def refresh_table(self):
        connection = sqlite3.connect(self.data_base)
        c = connection.cursor()

        count_of_male3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE gender = "М" AND room LIKE "3%" AND'
                f' isEvicted = 0').fetchall())
        count_of_male4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE gender = "М" AND room LIKE "4%" AND'
                f' isEvicted = 0').fetchall())
        count_of_male5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE gender = "М" AND room LIKE "5%" AND'
                f' isEvicted = 0').fetchall())
        count_of_female2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE gender = "Ж" AND room LIKE "2%" AND'
                f' isEvicted = 0').fetchall())
        count_of_female5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE gender = "Ж" AND room LIKE "5%" AND'
                f' isEvicted = 0').fetchall())

        count_of_budget2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "Б" AND room LIKE "2%" AND'
                f' isEvicted = 0').fetchall())
        count_of_budget3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "Б" AND room LIKE "3%" AND'
                f' isEvicted = 0').fetchall())
        count_of_budget4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "Б" AND room LIKE "4%" AND'
                f' isEvicted = 0').fetchall())
        count_of_budget5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "Б" AND room LIKE "5%" AND'
                f' isEvicted = 0').fetchall())

        count_of_commercial2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "К" AND room LIKE "2%" AND'
                f' isEvicted = 0').fetchall())
        count_of_commercial3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "К" AND room LIKE "3%" AND'
                f' isEvicted = 0').fetchall())
        count_of_commercial4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "К" AND room LIKE "4%" AND'
                f' isEvicted = 0').fetchall())
        count_of_commercial5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "b/c" = "К" AND room LIKE "5%" AND'
                f' isEvicted = 0').fetchall())

        count_of_lot_child2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "многодетные" AND room LIKE "2%"'
                f' AND isEvicted = 0').fetchall())
        count_of_lot_child3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "многодетные" AND room LIKE "3%"'
                f' AND isEvicted = 0').fetchall())
        count_of_lot_child4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "многодетные" AND room LIKE "4%"'
                f' AND isEvicted = 0').fetchall())
        count_of_lot_child5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "многодетные" AND room LIKE "5%"'
                f' AND isEvicted = 0').fetchall())

        count_of_poor2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "малоимущие" AND room LIKE "2%"'
                f' AND isEvicted = 0').fetchall())
        count_of_poor3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "малоимущие" AND room LIKE "3%" '
                f'AND isEvicted = 0').fetchall())
        count_of_poor4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "малоимущие" AND room LIKE "4%" '
                f'AND isEvicted = 0').fetchall())
        count_of_poor5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "малоимущие" AND room LIKE "5%" '
                f'AND isEvicted = 0').fetchall())

        count_of_orphan2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "сироты" AND room LIKE "2%" AND '
                f'isEvicted = 0').fetchall())
        count_of_orphan3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "сироты" AND room LIKE "3%" AND '
                f'isEvicted = 0').fetchall())
        count_of_orphan4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "сироты" AND room LIKE "4%" AND '
                f'isEvicted = 0').fetchall())
        count_of_orphan5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "сироты" AND room LIKE "5%" AND '
                f'isEvicted = 0').fetchall())

        count_of_alone2 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "воспитывает один родитель" AND room LIKE "2%"'
                f' AND isEvicted = 0').fetchall())
        count_of_alone3 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "воспитывает один родитель" AND room LIKE "3%"'
                f' AND isEvicted = 0').fetchall())
        count_of_alone4 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "воспитывает один родитель" AND room LIKE "4%"'
                f' AND isEvicted = 0').fetchall())
        count_of_alone5 = len(
            c.execute(
                f'SELECT id FROM "residents main table" WHERE "status" = "воспитывает один родитель" AND room LIKE "5%"'
                f' AND isEvicted = 0').fetchall())

        self.statisitc_table.setItem(0, 0, QTableWidgetItem("-"))
        self.statisitc_table.setItem(0, 1, QTableWidgetItem(str(count_of_male3)))
        self.statisitc_table.setItem(0, 2, QTableWidgetItem(str(count_of_male4)))
        self.statisitc_table.setItem(0, 3, QTableWidgetItem(str(count_of_male5)))
        self.statisitc_table.setItem(0, 4, QTableWidgetItem(str(count_of_male3 + count_of_male4 + count_of_male5)))

        self.statisitc_table.setItem(1, 0, QTableWidgetItem(str(0)))
        self.statisitc_table.setItem(1, 1, QTableWidgetItem("-"))
        self.statisitc_table.setItem(1, 2, QTableWidgetItem("-"))
        self.statisitc_table.setItem(1, 3, QTableWidgetItem(str(count_of_female5)))
        self.statisitc_table.setItem(1, 4, QTableWidgetItem(str(count_of_female5 + count_of_female2)))

        self.statisitc_table.setItem(2, 0, QTableWidgetItem(str(count_of_budget2)))
        self.statisitc_table.setItem(2, 1, QTableWidgetItem(str(count_of_budget3)))
        self.statisitc_table.setItem(2, 2, QTableWidgetItem(str(count_of_budget4)))
        self.statisitc_table.setItem(2, 3, QTableWidgetItem(str(count_of_budget5)))
        self.statisitc_table.setItem(2, 4, QTableWidgetItem(str(count_of_budget2 + count_of_budget3 + count_of_budget4
                                                                + count_of_budget5)))

        self.statisitc_table.setItem(3, 0, QTableWidgetItem(str(count_of_commercial2)))
        self.statisitc_table.setItem(3, 1, QTableWidgetItem(str(count_of_commercial3)))
        self.statisitc_table.setItem(3, 2, QTableWidgetItem(str(count_of_commercial4)))
        self.statisitc_table.setItem(3, 3, QTableWidgetItem(str(count_of_commercial5)))
        self.statisitc_table.setItem(3, 4, QTableWidgetItem(
            str(count_of_commercial2 + count_of_commercial3 + count_of_commercial4
                + count_of_commercial5)))

        self.statisitc_table.setItem(4, 0, QTableWidgetItem(str(count_of_lot_child2)))
        self.statisitc_table.setItem(4, 1, QTableWidgetItem(str(count_of_lot_child3)))
        self.statisitc_table.setItem(4, 2, QTableWidgetItem(str(count_of_lot_child4)))
        self.statisitc_table.setItem(4, 3, QTableWidgetItem(str(count_of_lot_child5)))
        self.statisitc_table.setItem(4, 4, QTableWidgetItem(
            str(count_of_lot_child2 + count_of_lot_child3 + count_of_lot_child4
                + count_of_lot_child5)))

        self.statisitc_table.setItem(5, 0, QTableWidgetItem(str(count_of_poor2)))
        self.statisitc_table.setItem(5, 1, QTableWidgetItem(str(count_of_poor3)))
        self.statisitc_table.setItem(5, 2, QTableWidgetItem(str(count_of_poor4)))
        self.statisitc_table.setItem(5, 3, QTableWidgetItem(str(count_of_poor5)))
        self.statisitc_table.setItem(5, 4, QTableWidgetItem(str(count_of_poor2 + count_of_poor3 + count_of_poor4
                                                                + count_of_poor5)))

        self.statisitc_table.setItem(6, 0, QTableWidgetItem(str(count_of_orphan2)))
        self.statisitc_table.setItem(6, 1, QTableWidgetItem(str(count_of_orphan3)))
        self.statisitc_table.setItem(6, 2, QTableWidgetItem(str(count_of_orphan4)))
        self.statisitc_table.setItem(6, 3, QTableWidgetItem(str(count_of_orphan5)))
        self.statisitc_table.setItem(6, 4, QTableWidgetItem(str(count_of_orphan2 + count_of_orphan3 + count_of_orphan4
                                                                + count_of_orphan5)))

        self.statisitc_table.setItem(7, 0, QTableWidgetItem(str(count_of_alone2)))
        self.statisitc_table.setItem(7, 1, QTableWidgetItem(str(count_of_alone3)))
        self.statisitc_table.setItem(7, 2, QTableWidgetItem(str(count_of_alone4)))
        self.statisitc_table.setItem(7, 3, QTableWidgetItem(str(count_of_alone5)))
        self.statisitc_table.setItem(7, 4, QTableWidgetItem(str(count_of_alone2 + count_of_alone3 + count_of_alone4
                                                                + count_of_alone5)))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
