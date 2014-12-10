import QtQuick 2.0
import QtQuick.Window 2.0
import Ubuntu.Components 1.1
import Ubuntu.Components.Popups 1.0
import YDict 1.0
import "ui"
import "components"

/*!
    \brief MainView with Tabs element.
           First Tab has a single Label and
           second Tab has a single ToolbarAction.
*/

MainView {
    id: main_window
    // objectName for functional testing purposes (autopilot-qt5)
    objectName: "mainView"

    // Note! applicationName needs to match the "name" field of the click manifest
    applicationName: "wl.org.ydict"

    /*
     This property enables the application to change orientation
     when the device is rotated. The default is false.
    */
    //automaticOrientation: true

    // Removes the old toolbar and enables new features of the new header.
    useDeprecatedToolbar: false

    width: units.dp(480)
    height: units.dp(300)

    YouDaoQuery{    /* 没有界面元素 */
        id:yd_query
        onResult: {
            console.debug('result',translation)
            row_basic.translation=translation
            row_query.queryText=query
        }
    }


    Rectangle{
        id: content

        InputField{
            id : row_query
            onQuery: {
                console.debug("query:",queryText)
                yd_query.query=queryText
            }
        }

        BasicField{
            id : row_basic
            anchors.left: row_query.left
            anchors.top: row_query.bottom
            anchors.topMargin: units.dp(35)
        }
    }
}

