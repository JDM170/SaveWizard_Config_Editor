#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent, QCloseEvent, QClipboard
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication
from ast import literal_eval
from json import dump, load, decoder
from hashlib import md5
from .form import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=Qt.Window)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_path = ""
        self.win_title = self.tr("{}".format(self.windowTitle()))

        self.ui.textEdit.document().contentsChanged.connect(self.content_changed)

        for action, method in {
            self.ui.actionOpen: self.open_file,
            self.ui.actionSave: self.save_file,
            self.ui.actionSave_As: self.save_as,
            self.ui.actionMD5: self.copy_hash,
            self.ui.actionCloseFile: self.close_file,
            self.ui.actionExit: self.exit
        }.items():
            action.triggered.connect(method)

    def resizeEvent(self, event: QResizeEvent):
        window = self.ui.centralwidget.geometry().getCoords()
        edit = self.ui.textEdit.geometry().getCoords()
        self.ui.textEdit.setGeometry(edit[0], edit[1], window[2], window[3]-25)

    def closeEvent(self, event: QCloseEvent):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def save_handler(path, data):
        with open(path, encoding="utf-8", mode="w") as f:
            dump(data, f, indent=4, sort_keys=True, separators=(",", " : "))
        try:
            with open(path, encoding="utf-8") as f:
                load(f)
        except decoder.JSONDecodeError:
            return False
        return True

    @staticmethod
    def generate_md5(fn):
        hash_md5 = md5()
        try:
            with open(fn, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except FileNotFoundError:
            return False

    def content_changed(self):
        self.setWindowModified(self.ui.textEdit.document().isModified())

    def open_file(self):
        file_path, file_name = QFileDialog.getOpenFileName(parent=self,
                                                           caption=self.tr("Choose config..."),
                                                           filter=self.tr("*.json"))
        if file_path != "":
            self.file_path = file_path
            with open(file_path) as f:
                self.ui.textEdit.setPlainText(f.read())
            self.setWindowTitle(self.tr("[*]{} - {}".format(file_path, self.win_title)))
            self.ui.textEdit.document().setModified(False)
            self.setWindowModified(False)

    def save_file(self):
        if self.file_path != "":
            data = literal_eval(self.ui.textEdit.toPlainText())
            ret = self.save_handler(self.file_path, data)
            if ret:
                self.ui.textEdit.document().setModified(False)
                self.setWindowModified(False)
            return ret

    def save_as(self):
        file_path, file_name = QFileDialog.getSaveFileName(parent=self,
                                                           caption=self.tr("Select position"),
                                                           filter=self.tr("*.json"))
        file_data = literal_eval(self.ui.textEdit.toPlainText())
        ret = self.save_handler(file_path, file_data)
        if ret:
            self.file_path = file_path
            self.setWindowTitle(self.tr("[*]{} - {}".format(file_path, self.win_title)))
            self.ui.textEdit.document().setModified(False)
            self.setWindowModified(False)

    def copy_hash(self):
        if self.maybe_save():
            result = self.generate_md5(self.file_path)
            clip = QApplication.clipboard()
            QClipboard.setText(clip, result)
            box = QMessageBox(QMessageBox.Information, "Information", "Hash successfully copied into your clipboard.")
            box.exec()

    def close_file(self):
        if self.maybe_save():
            self.setWindowTitle(self.win_title)
            self.ui.textEdit.clear()
            self.file_path = ""

    def exit(self):
        self.close()

    def maybe_save(self):
        if not self.ui.textEdit.document().isModified():
            return True
        box = QMessageBox.warning(self,
                                  self.tr("App"),
                                  self.tr("The document has been modified.\nDo you want to save your changes?"),
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if box == QMessageBox.Save:
            return self.save_file()
        elif box == QMessageBox.Discard:
            return True
        elif box == QMessageBox.Cancel:
            return False
        return True
