from PySide2.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QProgressBar
from PySide2.QtGui import QFont, QPixmap
from PySide2.QtCore import Qt, QTimer
import random
import os
import sys


def find_image_path(image_name):
    """
    Traverses through each path in sys.path to find the full path of the given image name.
    
    Parameters:
    - image_name: Name of the image file to search for within the directories listed in sys.path
    
    Returns:
    - Image path if found, otherwise None
    """
    for path in sys.path:
        image_path = os.path.join(path, "helldivers2_icon", image_name)
        if os.path.isfile(image_path):
            return image_path
    return None

# List of images used in the game, representing different actions or items 
image_list = ["Resupply.png", "Reinforcement.png", "Eagle Airstrike.png",
              "Orbital Precision Strike.png", "Orbital Smoke Strike.png",
              "Eagle Cluster Bomb.png", "Eagle Rearm.png"
             ]

# Initialize a list to store valid image paths
image_path = []
for image in image_list:
    path = find_image_path(image)
    print(path)
    image_path.append(path)

# Main class for the Direction Game
class DirectionGame(QMainWindow):
    
    def __init__(self):
        super(DirectionGame, self).__init__()

        self.setWindowTitle('Helldivers Simulator')
        self.setFixedSize(300, 200)

        # Initialize main widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        # Timer for updating on-screen labels
        self.now_number = 5000
        self.timer_update_label = QTimer(self)
        self.timer_update_label.timeout.connect(self.update_display)
        self.timer_update_label.start(100)
        
        # Variables for managing game difficulty
        self.hard_level = 5000
        self.decrement = 200
        
        # Define fixed direction sequences for the game challenges
        self.fixed_direction_sequences = [
            ['⭣', '⭣', '⭡', '⭢'],
            ['⭡', '⭣', '⭢', '⭠', '⭡'],
            ['⭡', '⭢', '⭣', '⭢'],
            ['⭢', '⭢', '⭡'],
            ['⭢', '⭢', '⭣', '⭡'],
            ['⭡', '⭢', '⭣', '⭣', '⭢'],
            ['⭡', '⭡', '⭠', '⭡', '⭢']
        ]
        
        # Store the image paths for use within the game
        self.image_paths = image_path
        
        # List of possible directions for the game
        self.directions = ['⭡', '⭣', '⭠', '⭢']
        self.labels_list = []  # Stores all QLabel objects
        self.current_direction = []
        self.current_index = 0

        # Initialize the user interface elements
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface elements for the game window.
        """
        # Add a label to display the start message of the game
        self.start_label = QLabel('Helldivers Simulator', alignment=Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.start_label.setFont(font)
        
        # Create labels for image and progress bar and add them to the layout
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(self.now_number)
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.setValue(self.now_number)
        
        self.layout.addWidget(self.start_label)
        
        # Add horizontal layout to place labels for displaying directions
        self.labels_layout = QHBoxLayout()
        self.layout.addLayout(self.labels_layout)
        self.show()
        
        # Update the display with the first set of directions
        self.updateDirectionsDisplay()

    def updateDirectionsDisplay(self):
        """
        Updates the display with a new sequence of direction labels.
        """
        # Empty current label list and layout
        for label in self.labels_list:
            self.labels_layout.removeWidget(label)
            label.deleteLater()
        self.labels_list.clear()
        
        # Choose a random direction sequence from predefined combinations
        chosen_sequence = random.choice(self.fixed_direction_sequences)
        self.current_direction = chosen_sequence
        self.current_index = 0
        
        # Select corresponding image for the chosen sequence
        chosen_sequence_index = self.fixed_direction_sequences.index(self.current_direction)
        chosen_image_path = self.image_paths[chosen_sequence_index]
        
        # Set image label properties and display the chosen image
        self.image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(chosen_image_path)
        scaled_pixmap = pixmap.scaledToWidth(40, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        
        # Create new QLabel for every element in the chosen sequence and add it to the layout and list
        for direction in chosen_sequence:
            label = QLabel(direction)
            label.setFont(QFont('Arial', 24))
            label.setAlignment(Qt.AlignCenter)
            self.labels_layout.addWidget(label)
            self.labels_list.append(label)
        
        # Adjust game difficulty and update the progress bar to match the new level
        self.hard_level = self.hard_level - self.decrement
        self.now_number = self.hard_level
        self.progress_bar.setValue(self.now_number)
        self.timer_update_label.start(100)

    def keyPressEvent(self, event):
        """
        Event handler for key presses. Checks if the user input matches the expected direction.
        """
        if not event.isAutoRepeat():  # Prevent auto-repeat for keyboard keys
            direction_map = {
                Qt.Key_Up: '⭡',
                Qt.Key_Down: '⭣',
                Qt.Key_Left: '⭠',
                Qt.Key_Right: '⭢'
            }
            direction = direction_map.get(event.key())
            if direction:
                self.checkUserInput(direction)

    def checkUserInput(self, direction):
        """
        Validates the user's input against the current direction sequence.
        """
        if self.current_index < len(self.current_direction):
            if direction == self.current_direction[self.current_index]:
                # Change color to green using stylesheet to indicate correctness
                self.labels_list[self.current_index].setStyleSheet('color: green')
                print('Correct!')
                self.current_index += 1
                if self.current_index >= len(self.current_direction):  # If all elements are judged
                    print("Sequence complete, updating directions!")
                    self.timer_update_label.stop()
                    self.updateDirectionsDisplay()  # Display new direction sequence
            else:
                # Change color to red to indicate incorrect input
                self.labels_list[self.current_index].setStyleSheet('color: red')
                print('Incorrect!')

    def onTimeout(self):
        """
        Called when timer runs out. Stops the timer and signals end of time to the player.
        """
        print("Time's up!")
        self.timer_update_label.stop()  # Stop the timer
        for label in self.labels_list:
            # Set label color to red to indicate timeout
            label.setStyleSheet('color: red; font-weight: bold')

        # After a short delay, initiate a new game sequence
        QTimer.singleShot(500, self.updateDirectionsDisplay)  
        
    def update_display(self):
        """
        Decrements the timer and updates the progress bar accordingly.
        """
        self.now_number -= 100  # Decrement the timer by 100 ms
        self.progress_bar.setValue(self.now_number)

        if self.now_number == 0:
            print("stop")
            self.onTimeout()
            self.now_number = 5000
            self.timer_update_label.stop()

    def closeEvent(self, event):
        """
        Cleans up resources and deletes existing game instance upon closing the game window.
        """
        self.timer_update_label.stop()

        # Check if the game window instance exists and closes it if it does
        global game_instance
        if 'game_instance' in globals():
            del globals()['game_instance']
            
        event.accept()  # Accept the close event and allow the window to close normally

# Create and show the game window if running as a standalone script
if __name__ == "__main__":
    try:
        game_instance.close()  # Close the existing game instance if it exists
        del game_instance
    except:
        pass
    
    game_instance = DirectionGame()
    game_instance.show()
