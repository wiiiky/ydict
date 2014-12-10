import QtQuick 2.0
import Ubuntu.Components 1.1
import Ubuntu.Components.Popups 1.0
import "../components"

Row{
    id: row_query
    anchors.top: content.top
    anchors.left: content.left
    anchors.leftMargin: units.dp(20)
    anchors.rightMargin: units.dp(20)
    anchors.topMargin: units.dp(10)
    spacing: units.dp(15)

    signal query
    signal activate
    onActivate: {
        if(queryText.length>0){
            query()
        }
    }

    property alias queryText: tf_query.text

    OrangeTextField{
        id:tf_query
        width: main_window.width*2/3
        placeholderText: i18n.tr("words to query")
        onAccepted: row_query.activate()
    }

    OrangeButton{
        id: btn_query
        width: main_window.width*1/5
        text: i18n.tr("Query")
        onClicked: row_query.activate()
    }

    // 成员函数
    function clearQueryText(){
        queryText=""
    }
}
