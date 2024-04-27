import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Controls.Material
import QtQuick.Dialogs

import ReportGenerator

ApplicationWindow {
    id: page
    width: 1500
    height: 800
    minimumWidth: 1500
    minimumHeight: 800
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Purple
    title: qsTr("Report Generator")

    ReportGenerator {
        id: reportGenerator
    }
    FolderDialog {
        id: folderDialog
        onAccepted: {
            reportGenerator.folder = currentFolder
            startReport.enabled = true
        }
    }
    RowLayout {
        anchors.fill: parent
        spacing: 0
        ColumnLayout {
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            Layout.margins: 20
            Layout.maximumWidth: 300
            Layout.fillHeight: true
            Button {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                text: "Select Image Folder"
                onClicked: {
                    folderDialog.open()
                }
            }
            Button {
                id: startReport
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: "Create Report"
                enabled: false
                onClicked: {
                    reportGenerator.createReport()
                }
            }
        }
        ColumnLayout {
            Layout.fillWidth : true
            Layout.fillHeight : true
            Layout.margins: 20
            Layout.leftMargin: 0
            Text {
                text: "Current folder: " + reportGenerator.folder
                font.pointSize : 10
                color: "white"
                }
            Flickable {
            id: flickable
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: 20

            TextArea.flickable: TextArea {
                id: output
                text: reportGenerator.output
                font.letterSpacing: 1
                }

            ScrollBar.vertical: ScrollBar { }
            ScrollBar.horizontal: ScrollBar { }
            }
        }
    }
}