import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs

import io.qt.textproperties 1.0

ApplicationWindow {
    id: page
    width: 500
    height: 200
    minimumWidth: 500
    minimumHeight: 200
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Purple
    title: qsTr("Report Generator")
    ReportCreator {
        id: reportCreator
    }
    FolderDialog {
        id: folderDialog
        onAccepted: {
            output.text = "Selected image folder: " + reportCreator.setFolder(currentFolder)
            output.visible = true
            startReport.enabled = true

        }
    }

    ColumnLayout {
        anchors.fill: parent
        Layout.alignment: Qt.AlignTop
        RowLayout {
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            Layout.topMargin: 20
            Layout.preferredWidth: parent.width
            Layout.preferredHeight: 200
            Button {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                text: "Select Folder"
                onClicked: {
                    folderDialog.open()
            }
            }
            TextArea{
                id: tag
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                placeholderText: "Tag"
            }
            TextArea{
                id: reportName
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                placeholderText: "Report Name"
            }
        }
        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Button {
                id: startReport
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: "Create Report"
                enabled: false
                onClicked: {
                        output.text = reportCreator.createReport(tag.text, reportName.text)
                }
            }
            Text {
                id : output
                visible: false
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                color: "white"
                font.pixelSize: 15
                text: ""
            }
        }
    }
}