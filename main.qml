import QtQuick 2.14
import QtQuick.Window 2.14
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.2

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    Button {
        text: "Добавить .wav файл"
        anchors.left: parent.left
        anchors.right: parent.right
        height: 100
        onClicked: {
            fileDialog.visible = true;
        }
    }

    FileDialog {
            id: fileDialog
            //selectFolder: true
            title: qsTr("Select the data directory")
            folder: shortcuts.home
            nameFilters: [ "(*.wav)" ]
            onAccepted: {
                file_manager.file_url = fileDialog.fileUrl // <---
            }
    }
}
