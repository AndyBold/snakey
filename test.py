import sys, requests, yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import ldclient
from ldclient.config import Config
from ldclient import Context

# Connect to LD at init. Must be a Singleton, so it's here.
# Singletonness is enforced by the get(), but let's make sure
# we only call it once.
ldclient.set_config(Config("sdk-62284ff5-1b09-4a56-83a2-dfc64f0af575"))
client = ldclient.get()


class GUIApp(QWidget):
    def __init__(self, onoroff, showNewFeature):
        # Initialise the app
        super().__init__()
        self.initUI(onoroff, showNewFeature)

        def perform_cleanup():
            # Close down the FF service link, and flush any remaining info
            print("Cleaning up")
            ldclient.get().close()

        # Configure app clean up
        QApplication.instance().aboutToQuit.connect(perform_cleanup)


    def initUI(self, onoroff, showNewFeature):
        # Set the initial layout
        self.outerLayout = QVBoxLayout()

        # Choose the context
        self.selectUserRow = QHBoxLayout()
        self.userSelectLabel = QLabel("Who are you?", self)
        self.selectUserRow.addWidget(self.userSelectLabel)

        # Create a dropdown (QComboBox)
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["randomuser@somewhere.com", "andy@somewhere.com", "alice@somewhere.com", "bob@somewhere.com", "barb@somewhere.com", "ciara@somewhere.com", "charlie@somewhere.com"])
        self.comboBox.currentIndexChanged.connect(self.on_selection_changed)
        self.selectUserRow.addWidget(self.comboBox)

        self.outerLayout.addLayout(self.selectUserRow)

        # Make somewhere to show the current flag variant
        self.flagRow = QHBoxLayout()
        self.flagLabel = QLabel("Current Flag Value:", self)
        self.flagRow.addWidget(self.flagLabel)

        # Create a QLineEdit
        self.textField = QLineEdit(self)
        self.textField.setText(onoroff)  # Set initial text based on 'onoroff' value
        self.flagRow.addWidget(self.textField)

        self.outerLayout.addLayout(self.flagRow)

        #################
        # 🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄
        # ✨ !!! SHINY NEW FEATURE !!! ✨
        # 🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄🌈🦄
        #################

        # This is our new feature - A BUTTON! - that will only be visible to people
        # in the beta test program when the feature is enabled.
        # Start by adding the button, but invisible.
        self.newFeatureRow = QHBoxLayout()
        self.newButton = QPushButton('🦄 HELLO SHINY NEW WORLD 🌈', self)
        self.newFeatureRow.addWidget(self.newButton)
        self.newButton.setVisible(False)
        self.newButton.clicked.connect(self.display_image)
        self.outerLayout.addLayout(self.newFeatureRow)

        #################
        # 😢 The end.
        #################

        # Set the layout and window title
        self.setLayout(self.outerLayout)
        self.setWindowTitle('Flagomaton (Working Title)')


    # Wrangle unicorns
    #
    # TODO: Make this a new row in the main window
    def display_image(arg1, arg2):
        window = QWidget()

        url = 'https://static.vecteezy.com/system/resources/previews/000/302/539/original/a-unicorn-on-rainbow-template-vector.jpg'

        window.setWindowTitle('Display Image from URL')
        window.setGeometry(100, 100, 600, 400)  # Adjust size as needed

        layout = QVBoxLayout()

        # Fetch the image data
        response = requests.get(url)
        image = QPixmap()
        image.loadFromData(response.content)

        # Create a QLabel and set the QPixmap
        label = QLabel()
        label.setPixmap(image)
        label.setAlignment(Qt.AlignCenter)  # Center the image in the QLabel

        layout.addWidget(label)
        window.setLayout(layout)
        window.show()


    # Handle changes to the combobox
    def on_selection_changed(self, index):
        self.selected_text = self.comboBox.itemText(index)

        # Update our context key based on the user name.
        self.username = self.selected_text.split('@')[0]

        self.context = Context.builder(self.username + "-context-key").name(self.selected_text).build()
        onoroff = client.variation("node-test", self.context, False)
        showNewFeature = client.variation("super-new-feature", self.context, False)

        self.textField.setText(str(onoroff))

        if onoroff and showNewFeature:
            self.newButton.setVisible(True)
            print("🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄")
        else:
            self.newButton.setVisible(False)
            print("😢😢😢😢😢😢😢😢😢😢")


        # Also check if we should serve


def main():
    app = QApplication(sys.argv)
    onoroff = "Welcome to this simple demo!"  # This value can be dynamically changed
    showNewFeature = False
    ex = GUIApp(onoroff, showNewFeature)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
