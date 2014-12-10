import QtQuick 2.0
import Ubuntu.Components 1.1
import Ubuntu.Components.Popups 1.0
Rectangle {
	color: Theme.palette.normal.background
	width: units.gu(80)
	height: units.gu(80)
	Component {
		id: popoverComponent
		Popover {
			id: popover

			Label{
				text:"hello world"
			}
		}
	}
	Button {
		id: popoverButton
		anchors.centerIn: parent
		text: "open"
		onClicked: PopupUtils.open(popoverComponent, popoverButton)
	}
}
