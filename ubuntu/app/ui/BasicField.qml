import QtQuick 2.0
import Ubuntu.Components 1.1
import Ubuntu.Components.Popups 1.0
import "../components"

Row{
    id: row_basic
    spacing: units.dp(20)

    property alias translation: tf_result.text

    GreyLabel{
        id: basic_label

        anchors.top:  parent.top
        anchors.topMargin: units.dp(5)
//        anchors.verticalCenter: parent.verticalCenter
        text: i18n.tr("Basic:")
    }
    UbuntuShape{

        id: shape
        radius : "large"

//        width:units.dp(250)
        width:parent.width*0.5

        OrangeLabel{
            id: tf_result
            anchors.left: shape.left
            anchors.top: shape.top
            anchors.right: shape.right

            anchors.topMargin: units.dp(10)
            anchors.rightMargin: units.dp(10)
            anchors.leftMargin: units.dp(10)

            wrapMode: Text.Wrap

            onHeightChanged: {
                shape.height=height+units.dp(20)
            }

            states: [
                State {
                    name: "from"
                    PropertyChanges {
                        target: tf_result
                        color:UbuntuColors.coolGrey
                        font.pixelSize: 1
                    }
                },
                State {
                    name : "to"
                    PropertyChanges {
                        target: tf_result
                        color: UbuntuColors.orange
                        font.pixelSize: 15
                    }
                }
            ]

            transitions: [
                Transition {
                    from : "from"
                    to: "to"
                    ColorAnimation { from: UbuntuColors.coolGrey; to: UbuntuColors.orange; duration: 200 }
                    NumberAnimation { target: tf_result; property: "font.pixelSize"; duration: 200; easing.type: Easing.InOutQuad }
                }
            ]

            onTextChanged: {
                state="from"
                state="to"
            }
        }
    }
}
