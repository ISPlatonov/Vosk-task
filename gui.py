# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import threading

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2 import QtCore, QtGui, QtQml

from main import make_text


class FileManager(QtCore.QObject):
    file_url_Changed = QtCore.Signal(QtCore.QUrl)

    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent)
        self._file_url = QtCore.QUrl()

    def get_file_url(self):
        return self._file_url

    def set_file_url(self, file_url):
        if self._file_url != file_url:
            self._file_url = file_url
            self.file_url_Changed.emit(self._file_url)

    file_url = QtCore.Property(QtCore.QUrl, fget=get_file_url, fset=set_file_url, notify=file_url_Changed)


@QtCore.Slot(QtCore.QUrl)
def on_file_url_changed(file_url):
    #print(file_url.toLocalFile())
    
    make_text(file_url.toLocalFile())


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    file_manager = FileManager()
    file_manager.file_url_Changed.connect(on_file_url_changed)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("file_manager", file_manager)
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
