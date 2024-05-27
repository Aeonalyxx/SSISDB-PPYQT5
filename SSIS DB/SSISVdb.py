import sys
import os
import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui

#CHRIS ADRIAN GUMISAD               CCC-151

#STUDENT DIALOGS ======================================================================================


class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self, Course_Codes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student")
        self.setFixedSize(500, 210)
        self.Course_Codes = Course_Codes

        self.I_label = QtWidgets.QLabel("Student ID:")
        self.Name_label = QtWidgets.QLabel("Student Name:")
        self.Gender_label = QtWidgets.QLabel("Student Gender:")
        self.course_label = QtWidgets.QLabel("Course Code:")
        self.Year_label = QtWidgets.QLabel("Student Year:")

        self.I_edit = QtWidgets.QLineEdit(self)
        self.Name_edit = QtWidgets.QLineEdit(self)
        
        self.Gender_combobox = QtWidgets.QComboBox(self)
        self.Gender_combobox.addItems(["Male", "Female"])

        self.course_combobox = QtWidgets.QComboBox(self)
        self.course_combobox.addItems(self.Course_Codes)  

        self.Year_combobox = QtWidgets.QComboBox(self)
        self.Year_combobox.addItems(["1", "2", "3", "4"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Create layouts
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.I_label, self.I_edit)
        form_layout.addRow(self.Name_label, self.Name_edit)
        form_layout.addRow(self.Gender_label, self.Gender_combobox)
        form_layout.addRow(self.course_label, self.course_combobox)
        form_layout.addRow(self.Year_label, self.Year_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)
        
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.I_edit, self.Name_edit, self.Gender_combobox, self.course_combobox, self.Year_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            student_data = [
                self.I_edit.text(),
                self.Name_edit.text(),
                self.Gender_combobox.currentText(),
                self.course_combobox.currentText(), 
                self.Year_combobox.currentText()
            ]
            if self.check_Student_ID_unique(student_data[0]):
                self.save_to_db(student_data)
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Student ID already exists. Please enter a unique ID.")
    
    def check_Student_ID_unique(self, new_ID):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM studentlist WHERE Student_ID = ?', (new_ID,))
        result = cursor.fetchone()
        conn.close()
        return result is None

    def save_to_db(self, student_data):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO studentlist (Student_ID, Name, Gender, Course_Code, Year) VALUES (?, ?, ?, ?, ?)', student_data)
        conn.commit()
        conn.close()
        
class EditStudentDialog(QtWidgets.QDialog):
    data_changed = QtCore.pyqtSignal(list)

    def __init__(self, student_data, Course_Codes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.setFixedSize(500, 210)
        self.Course_Codes = Course_Codes 

        self.I_label = QtWidgets.QLabel("Student ID:")
        self.Name_label = QtWidgets.QLabel("Student Name:")
        self.Gender_label = QtWidgets.QLabel("Student Gender:")
        self.course_label = QtWidgets.QLabel("Course Code:")
        self.Year_label = QtWidgets.QLabel("Student Year:")

        self.I_edit = QtWidgets.QLineEdit(self)
        self.Name_edit = QtWidgets.QLineEdit(self)
        
        self.Gender_combobox = QtWidgets.QComboBox(self)
        self.Gender_combobox.addItems(["Male", "Female"])

        self.course_combobox = QtWidgets.QComboBox(self)
        self.course_combobox.addItems(self.Course_Codes)

        self.Year_combobox = QtWidgets.QComboBox(self)
        self.Year_combobox.addItems(["1", "2", "3", "4"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Create layouts
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.I_label, self.I_edit)
        form_layout.addRow(self.Name_label, self.Name_edit)
        form_layout.addRow(self.Gender_label, self.Gender_combobox)
        form_layout.addRow(self.course_label, self.course_combobox)
        form_layout.addRow(self.Year_label, self.Year_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)

        self.setStudentData(student_data)
        self.original_student_data = student_data
        
    def setStudentData(self, student_data):
        self.I_edit.setText(student_data[0])
        self.Name_edit.setText(student_data[1])
        self.Gender_combobox.setCurrentText(student_data[2])
        self.course_combobox.setCurrentText(student_data[3])
        self.Year_combobox.setCurrentText(student_data[4])
        
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.I_edit, self.Name_edit, self.Gender_combobox, self.course_combobox, self.Year_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            edited_student_data = [
                self.I_edit.text(),
                self.Name_edit.text(),
                self.Gender_combobox.currentText(),
                self.course_combobox.currentText(),
                self.Year_combobox.currentText()
            ]
            if edited_student_data[0] != self.original_student_data[0]:
                if not self.check_I_unique(edited_student_data[0]):
                    QtWidgets.QMessageBox.warning(self, "Warning", "Student ID already exists. Please enter a unique ID.")
                    return
              
            self.update_student_data(edited_student_data)
            self.data_changed.emit(edited_student_data)
            self.accept()
    
    def check_I_unique(self, new_I):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM studentlist WHERE I = ?', (new_I,))
        result = cursor.fetchone()
        conn.close()
        return result is None

    def update_student_data(self, edited_student_data):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE studentlist
            SET Student_ID = ?, Name = ?, Gender = ?, Course_Code = ?, Year = ?
            WHERE Student_ID = ?
        ''', edited_student_data + [self.original_student_data[0]])
        conn.commit()
        conn.close()

#COURSE DIALOGS===========================================================================================

class AddCourseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Course")
        self.setFixedSize(500, 210)

        self.Course_Code_label = QtWidgets.QLabel("Course Code:")
        self.Name_label = QtWidgets.QLabel("Course Name:")
        self.Building_label = QtWidgets.QLabel("Course Bldg. :")

        self.Course_Code_edit = QtWidgets.QLineEdit(self)
        
        self.Course_Name_edit = QtWidgets.QLineEdit(self)
        
        self.Building_combobox = QtWidgets.QComboBox(self)
        self.Building_combobox.addItems(["CCS", "CASS", "COE", "CBAA", "CON", "CSM", "CED"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.Course_Code_label, self.Course_Code_edit)
        form_layout.addRow(self.Name_label, self.Course_Name_edit)
        form_layout.addRow(self.Building_label, self.Building_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)
        
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.Course_Code_edit, self.Course_Name_edit, self.Building_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            course_data = [
                self.Course_Code_edit.text(),
                self.Course_Name_edit.text(),
                self.Building_combobox.currentText()
            ]
            if self.check_Course_Code_unique(course_data[0]):
                self.save_to_db(course_data)
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Course Code already exists. Please enter a unique ID.")
    
    def check_Course_Code_unique(self, new_Course_Code):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courselist WHERE Course_Code = ?', (new_Course_Code,))
        result = cursor.fetchone()
        conn.close()
        return result is None

    def save_to_db(self, course_data):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO courselist (Course_Code, Course_Name, Building) VALUES (?, ?, ?)', course_data)
        conn.commit()
        conn.close()
        
class EditCourseDialog(QtWidgets.QDialog):
    data_changed = QtCore.pyqtSignal(list)

    def __init__(self, course_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Course")
        self.setFixedSize(500, 210)

        self.Course_Code_label = QtWidgets.QLabel("Course Code:")
        self.Course_Name_label = QtWidgets.QLabel("Course Name:")
        self.Building_label = QtWidgets.QLabel("Course Bldg. :")

        self.Course_Code_edit = QtWidgets.QLineEdit(self)
        
        self.Course_Name_edit = QtWidgets.QLineEdit(self)
        
        self.Building_combobox = QtWidgets.QComboBox(self)
        self.Building_combobox.addItems(["CCS", "CASS", "COE", "CBAA", "CON", "CSM", "CED"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.Course_Code_label, self.Course_Code_edit)
        form_layout.addRow(self.Course_Name_label, self.Course_Name_edit)
        form_layout.addRow(self.Building_label, self.Building_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)
        
        self.setCourseData(course_data)
        self.original_course_data = course_data
        
    def setCourseData(self, course_data):
        self.Course_Code_edit.setText(course_data[0])
        self.Course_Name_edit.setText(course_data[1])
        self.Building_combobox.setCurrentText(course_data[2])
        
    def get_course_data(self):
        new_Course_Code = self.Course_Code_edit.text()
        new_Course_Name = self.Course_Name_edit.text()
        new_Building = self.Building_combobox.currentText()
        return [new_Course_Code, new_Course_Name, new_Building]
    
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.Course_Code_edit, self.Course_Name_edit, self.Building_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            edited_course_data = [
                self.Course_Code_edit.text(),
                self.Course_Name_edit.text(),
                self.Building_combobox.currentText()
            ]
            if edited_course_data[0] != self.original_course_data[0]:
                if not self.check_Course_Code_unique(edited_course_data[0]):
                    QtWidgets.QMessageBox.warning(self, "Warning", "Course Code already exists. Please enter a unique code.")
                    return

            self.update_course_data(edited_course_data)
            self.data_changed.emit(edited_course_data)
            self.accept()
    
    def check_Course_Code_unique(self, new_Course_Code):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courselist WHERE Course_Code = ?', (new_Course_Code,))
        result = cursor.fetchone()
        conn.close()
        return result is None

    def update_course_data(self, edited_course_data):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courselist
            SET Course_Code = ?, Course_Name = ?, Building = ?
            WHERE Course_Code = ?
        ''', edited_course_data + [self.original_course_data[0]])
        conn.commit()
        conn.close()
        
#MAINWINDOW UI==========================================================================================        
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1176, 705)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.SSIS = QtWidgets.QLabel(self.centralwidget)
        self.SSIS.setGeometry(QtCore.QRect(320, 10, 691, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.SSIS.setFont(font)
        self.SSIS.setObjectName("SSIS")
        
    #TAB BUTTONS
        self.TabButtons = QtWidgets.QTabWidget(self.centralwidget)
        self.TabButtons.setGeometry(QtCore.QRect(30, 60, 1121, 591))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TabButtons.setFont(font)
        self.TabButtons.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TabButtons.setObjectName("TabButtons")
        
#Student TAB =================================================================================================

        self.Students = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Students.setFont(font)
        
    #STUDENT SEARCH BAR
        self.StudentIDLineEdit = QtWidgets.QLineEdit(self.Students)
        self.StudentIDLineEdit.setGeometry(QtCore.QRect(130, 510, 210, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.StudentIDLineEdit.setFont(font)
        self.StudentIDLineEdit.setMaxLength(50) 
        self.StudentIDLineEdit.setPlaceholderText("Search...")
        self.StudentIDLineEdit.setObjectName("StudentIDLineEdit")
        self.StudentIDLineEdit.returnPressed.connect(self.search_studentlist)
        
    #SEARCH STUDENT BUTTON
        self.SearchStudentIDButton = QtWidgets.QPushButton(self.Students)
        self.SearchStudentIDButton.setGeometry(QtCore.QRect(339, 510, 93, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SearchStudentIDButton.setFont(font)
        self.SearchStudentIDButton.setObjectName("SearchStudent")
        self.SearchStudentIDButton.clicked.connect(self.search_studentlist)
        
    #STUDENT FILTER BOX
        self.StudentfilterComboBox = QtWidgets.QComboBox(self.Students)
        self.StudentfilterComboBox.setGeometry(QtCore.QRect(10, 510, 120, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.StudentfilterComboBox.setFont(font)
        self.StudentfilterComboBox.setObjectName("filterComboBox")
        self.StudentfilterComboBox.addItems(["Student_ID", "Name", "Gender", "Course_Code", "Year"])
        
    #STUDENT TABLE
        self.StudentTable = QtWidgets.QTableWidget(self.Students)
        self.StudentTable.setGeometry(QtCore.QRect(120, 10, 981, 491))
        self.StudentTable.setColumnCount(5)
        self.StudentTable.setHorizontalHeaderLabels(["Student ID", "Name", "Gender", "Course Code", "Year"])
        self.StudentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.StudentTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        # Adjust column widths
        self.StudentTable.setColumnWidth(0, 170)  # Student ID
        self.StudentTable.setColumnWidth(1, 360)  # Student Name
        self.StudentTable.setColumnWidth(2, 100)  # Gender
        self.StudentTable.setColumnWidth(3, 200)  # Course Code
        self.StudentTable.setColumnWidth(4, 70)  # Year

    #ADD STUDENT BUTTON 
        self.AddStudentButton = QtWidgets.QPushButton(self.Students)
        self.AddStudentButton.setGeometry(QtCore.QRect(10, 120, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.AddStudentButton.setFont(font)
        self.AddStudentButton.clicked.connect(self.open_add_student_dialog)
        
    #EDIT STUDENT BUTTON   
        self.EditStudentButton = QtWidgets.QPushButton(self.Students)
        self.EditStudentButton.setGeometry(QtCore.QRect(10, 210, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.EditStudentButton.setFont(font)
        self.EditStudentButton.clicked.connect(self.open_edit_student_dialog)
        
    #DELETE STUDENT BUTTON    
        self.DeleteStudentButton = QtWidgets.QPushButton(self.Students)
        self.DeleteStudentButton.setGeometry(QtCore.QRect(10, 300, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DeleteStudentButton.setFont(font)
        self.DeleteStudentButton.clicked.connect(self.delete_student)
        self.TabButtons.addTab(self.Students, "")
        
#COURSE TAB =================================================================================================

        self.Courses = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Courses.setFont(font)
        
    #SEARCH COURSE ID BUTTON
        self.SearchCourseIDButton = QtWidgets.QPushButton(self.Courses)
        self.SearchCourseIDButton.setGeometry(QtCore.QRect(339, 510, 93, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SearchCourseIDButton.setFont(font)
        self.SearchCourseIDButton.clicked.connect(self.search_courselist)
        
    #COURSE SEARCH BAR
        self.CourseIDLineEdit = QtWidgets.QLineEdit(self.Courses)
        self.CourseIDLineEdit.setGeometry(QtCore.QRect(130, 510, 210, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.CourseIDLineEdit.setFont(font)
        self.CourseIDLineEdit.setMaxLength(80) 
        self.CourseIDLineEdit.setPlaceholderText("Search...")
        self.CourseIDLineEdit.returnPressed.connect(self.search_courselist)
        
    #FILTER BOX
        self.CoursefilterComboBox = QtWidgets.QComboBox(self.Courses)
        self.CoursefilterComboBox.setGeometry(QtCore.QRect(10, 510, 120, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.CoursefilterComboBox.setFont(font)
        self.CoursefilterComboBox.setObjectName("filterComboBox")
        self.CoursefilterComboBox.addItems(["Course_Code", "Course_Name", "Building"])
        
    #COURSE TABLE   
        self.CourseTable = QtWidgets.QTableWidget(self.Courses)
        self.CourseTable.setGeometry(QtCore.QRect(120, 10, 981, 491))
        self.CourseTable.setColumnCount(3)
        self.CourseTable.setHorizontalHeaderLabels(["Course Code", "Course Name", "Bldg."])
        self.CourseTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.CourseTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.CourseTable.setColumnWidth(0, 155) #COURSE CODE
        self.CourseTable.setColumnWidth(1, 680) #COURSE NAME
        self.CourseTable.setColumnWidth(2, 80) #COURSE BLDG
    
    #ADD COURSE BUTTON 
        self.AddCourseButton = QtWidgets.QPushButton(self.Courses)
        self.AddCourseButton.setGeometry(QtCore.QRect(10, 120, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.AddCourseButton.setFont(font)
        self.AddCourseButton.clicked.connect(self.open_add_course_dialog)

    #EDIT COURSE BUTTON   
        self.EditCourseButton = QtWidgets.QPushButton(self.Courses)
        self.EditCourseButton.setGeometry(QtCore.QRect(10, 210, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.EditCourseButton.setFont(font)
        self.EditCourseButton.clicked.connect(self.open_edit_course_dialog)

    #DELETE COURSE BUTTON  
        self.DeleteCourseButton = QtWidgets.QPushButton(self.Courses)
        self.DeleteCourseButton.setGeometry(QtCore.QRect(10, 300, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DeleteCourseButton.setFont(font)
        self.DeleteCourseButton.clicked.connect(self.delete_course)
        self.TabButtons.addTab(self.Courses, "")

#MAIN WINDOW =================================================================================================

        MainWindow.setCentralWidget(self.centralwidget)
        self.translateUi(MainWindow)
        self.TabButtons.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
#RETRANSLATE UI =================================================================================================

    def translateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SSIS"))
        self.SSIS.setText(_translate("MainWindow", "Simple Student Information System"))
        
        self.SearchStudentIDButton.setText(_translate("MainWindow", "Search"))
        self.AddStudentButton.setText(_translate("MainWindow", "Add"))
        self.EditStudentButton.setText(_translate("MainWindow", "Edit"))
        self.DeleteStudentButton.setText(_translate("MainWindow", "Delete"))
        self.TabButtons.setTabText(self.TabButtons.indexOf(self.Students), _translate("MainWindow", "Students"))
        
        self.SearchCourseIDButton.setText(_translate("MainWindow", "Search"))
        self.AddCourseButton.setText(_translate("MainWindow", "Add"))
        self.EditCourseButton.setText(_translate("MainWindow", "Edit"))
        self.DeleteCourseButton.setText(_translate("MainWindow", "Delete"))
        self.TabButtons.setTabText(self.TabButtons.indexOf(self.Courses), _translate("MainWindow", "Programs"))
#=========================================================================================================================

#STUDENT FUNCTIONS=========================================================================================================

    #GET ALL STUDENT FROM DB
    def get_all_student_data(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM studentlist")
        all_student_data = cursor.fetchall()

        conn.close()
        return all_student_data
    
    #SEARCH STUDENT
    def search_studentlist(self):
        filter_option = self.StudentfilterComboBox.currentText()
        search_query = self.StudentIDLineEdit.text().strip().upper()  # Ensure the search query is in uppercase
        self.StudentTable.setRowCount(0)
        matches_found = False

        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM studentlist")

        for row_data in cursor.fetchall():
            if filter_option == "Gender" and search_query == row_data[2].upper():
                self.add_row_to_student_table(row_data)
                matches_found = True
            elif not search_query:  # If no search query, display all rows
                self.add_row_to_student_table(row_data)
                matches_found = True
            elif filter_option != "Gender" and search_query in row_data:
                self.add_row_to_student_table(row_data)
                matches_found = True

        conn.close()

        if not matches_found:  # No match found for the given filter and search query
            QtWidgets.QMessageBox.warning(self.StudentIDLineEdit, "No Match", f"No student found with the given {filter_option}.")

    def add_row_to_student_table(self, student_data):
        row_position = self.StudentTable.rowCount()
        self.StudentTable.insertRow(row_position)
        for column, value in enumerate(student_data):
            item = QtWidgets.QTableWidgetItem(value)
            self.StudentTable.setItem(row_position, column, item)

    #ADD STUDENT 
    def open_add_student_dialog(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Course_Code FROM courselist")
        Course_Codes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        dialog = AddStudentDialog(Course_Codes)
        if dialog.exec_():
            self.update_student_table()

    #EDIT STUDENT
    def open_edit_student_dialog(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Course_Code FROM courselist")
        Course_Codes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        selected_row = self.StudentTable.currentRow()
        if selected_row >= 0:
            student_data = []
            for column in range(self.StudentTable.columnCount()):
                item = self.StudentTable.item(selected_row, column)
                student_data.append(item.text() if item else "")

            dialog = EditStudentDialog(student_data, Course_Codes)
            dialog.data_changed.connect(self.update_student_table)
            if dialog.exec_():
                self.update_student_table()
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to edit.")

    # DELETE STUDENT
    def delete_student(self):
        selected_row = self.StudentTable.currentRow()
        if selected_row >= 0:
            confirmation = QtWidgets.QMessageBox.question(self.centralwidget, "Confirmation", "Are you sure you want to delete this student?",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                I_item = self.StudentTable.item(selected_row, 0)
                if I_item is not None:
                    I = I_item.text()
                    self.StudentTable.removeRow(selected_row)
                    self.update_db_for_students(I)
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to delete.")

    #UPDATE STUDENT AFTER DELETE DB
    def update_db_for_students(self, deleted_Student_ID):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM studentlist WHERE Student_ID = ?", (deleted_Student_ID,))
        conn.commit()
        
        conn.close()


    # UPDATE STUDENT TABLE FROM DB
    def update_student_table(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Student_Id, Name, Gender, Course_Code, Year FROM studentlist")
        students = cursor.fetchall()

        self.StudentTable.setRowCount(0)
        for row_number, row_data in enumerate(students):
            self.StudentTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))  # Ensure data is converted to string
                font = QtGui.QFont()
                font.setPointSize(14)
                item.setFont(font)
                self.StudentTable.setItem(row_number, column_number, item)

        conn.close()

    # SAVE STUDENT DATA
    def save_student_data(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Students")

        student_data = []
        for row in range(self.StudentTable.rowCount()):
            row_data = []
            for column in range(self.StudentTable.columnCount()):
                item = self.StudentTable.item(row, column)
                row_data.append(item.text() if item else "")
            student_data.append(tuple(row_data))

        cursor.executemany("INSERT INTO studentlist (Student_Id, Name, Gender, Course_Code, Year) VALUES (?, ?, ?, ?, ?)", student_data)

        conn.commit()
        conn.close()

#COURSE FUNCTIONS================================================================================================================

    #GET COURSE DATA
    def get_all_course_data(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Course_Code, Course_Name, Building FROM courselist")
        all_course_data = cursor.fetchall()

        conn.close()

        return all_course_data

    #SEARCH COURSE
    def search_courselist(self):
        filter_option = self.CoursefilterComboBox.currentText()
        search_query = self.CourseIDLineEdit.text().strip().lower()
        self.CourseTable.setRowCount(0)
        matches_found = False
        
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        
        query = f"SELECT * FROM courselist WHERE LOWER({filter_option.replace(' ', '')}) LIKE ?"
        cursor.execute(query, ('%' + search_query + '%',))
        
        for row_data in cursor.fetchall():
            self.add_row_to_course_table(row_data)
            matches_found = True
        
        conn.close()

        if not matches_found:
            QtWidgets.QMessageBox.warning(self.CourseIDLineEdit, "No Match", f"No course found with the given {filter_option}.")

  
    def add_row_to_course_table(self, course_data):
        row_position = self.CourseTable.rowCount()
        self.CourseTable.insertRow(row_position)
        for column, value in enumerate(course_data):
            item = QtWidgets.QTableWidgetItem(value)
            self.CourseTable.setItem(row_position, column, item)
            
    #ADD COURSE
    def open_add_course_dialog(self):
        dialog = AddCourseDialog()
        if dialog.exec_():
            self.update_course_table()
            
    #EDIT COURSE
    def open_edit_course_dialog(self):
        selected_row = self.CourseTable.currentRow()
        if selected_row >= 0:
            course_data = []
            for column in range(self.CourseTable.columnCount()):
                item = self.CourseTable.item(selected_row, column)
                course_data.append(item.text() if item else "")
        
            dialog = EditCourseDialog(course_data)
            if dialog.exec_():
                new_course_data = dialog.get_course_data()
                self.update_course_table()
                
                old_Course_Code = course_data[0]
                new_Course_Code = new_course_data[0]
                
                if old_Course_Code != new_Course_Code:
                    self.update_student_Course_Code(old_Course_Code, new_Course_Code)
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to edit.")

    #UPDATE COURSE CODE (STUDENT)
    def update_student_Course_Code(self, old_Course_Code, new_Course_Code):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE studentlist SET Course_Code = ? WHERE Course_Code = ?", (new_Course_Code, old_Course_Code))
        conn.commit()
        conn.close()
        ui.update_student_table()
    
    #DELETE COURSE
    def delete_course(self):
        selected_row = self.CourseTable.currentRow()
        if selected_row >= 0:
            confirmation = QtWidgets.QMessageBox.question(self.centralwidget, "Confirmation", "Are you sure you want to delete this course?",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                course_code_item = self.CourseTable.item(selected_row, 0)
                if course_code_item is not None:
                    course_code = course_code_item.text()
                    
                    conn = sqlite3.connect('ssis.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM studentlist WHERE Course_Code = ?", (course_code,))
                    conn.commit()
                    conn.close()
                    
                    ui.update_student_table()

                    self.CourseTable.removeRow(selected_row)
                    self.update_db_for_courses(course_code)
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to delete.")

    #UPDATE DATABASE
    def update_db_for_courses(self, delete_course):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM courselist WHERE Course_Code = ?", (delete_course,))
        conn.commit()

        conn.close()

    #UPDATE COURSE TABLE
    def update_course_table(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Course_Code, Course_Name, Building FROM courselist")
        courses = cursor.fetchall()

        self.CourseTable.setRowCount(0)
        for row_number, row_data in enumerate(courses):
            self.CourseTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(data)
                font = QtGui.QFont()
                font.setPointSize(14)
                item.setFont(font)
                self.CourseTable.setItem(row_number, column_number, item)

        conn.close()

    #SAVE COURSE DATA
    def save_course_data(self):
        conn = sqlite3.connect('ssis.db')
        cursor = conn.cursor()

        # Clear the current course data in the database
        cursor.execute("DELETE FROM courselist")

        # Insert the new course data from the UI table
        for row in range(self.CourseTable.rowCount()):
            Course_Code = self.CourseTable.item(row, 0).text() if self.CourseTable.item(row, 0) else ""
            Course_Name = self.CourseTable.item(row, 1).text() if self.CourseTable.item(row, 1) else ""
            Building = self.CourseTable.item(row, 2).text() if self.CourseTable.item(row, 2) else ""

            cursor.execute(
                "INSERT INTO courselist (Course_Code, Course_Name, Building) VALUES (?, ?, ?)",
                (Course_Code, Course_Name, Building)
            )

        conn.commit()
        conn.close()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    db_file_path = 'ssis.db'
    if not os.path.exists(db_file_path):
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS studentlist (
                Student_ID TEXT PRIMARY KEY,
                Name TEXT NOT NULL,
                Gender TEXT NOT NULL,
                Course_Code TEXT NOT NULL,
                Year TEXT NOT NULL,
                FOREIGN KEY (Course_Code) REFERENCES courselist (Course_Code) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS courselist (
                          Course_Code TEXT PRIMARY KEY,
                          Course_Name TEXT,
                          Building TEXT)''')

        conn.close()
    else:
        conn = sqlite3.connect(db_file_path)

    if os.path.exists(db_file_path):
        ui.update_student_table()
        ui.update_course_table()

    conn.close()

    sys.exit(app.exec_())