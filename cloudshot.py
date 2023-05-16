import argparse
import sys
import os
from io import BytesIO
import datetime
import subprocess
import pytesseract

# GUI related imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

# Clipboard related imports
import win32clipboard
from PIL import Image

class Snipper(QtWidgets.QWidget):

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle("ScreenShot")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        # Get the screen that contains the mouse cursor
        self._screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())

        # Set the background of the widget to be the screenshot of the screen
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.getWindow()))
        self.setPalette(palette)

        # Set the cursor to crosshair
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        # Initialize start and end points for the screenshot rectangle
        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()

        # Drawing mode attribute
        self.drawing = False

        # List to store the points of the drawing
        self.drawing_points = []



    def getWindow(self):
        # Get a screenshot of the whole screen
        return self._screen.grabWindow(0)



    def keyPressEvent(self, event):
        # If Ctrl+A is pressed, take the screenshot and convert it to text using Tesseract OCR
        if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            self.take_screenshot_and_convert_to_text()
            QtWidgets.QApplication.quit()

        # If Ctrl+S is pressed, save the screenshot to a file
        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_screenshot()
            QtWidgets.QApplication.quit()

        # If Ctrl+D is pressed, Start/stop drawing
        elif event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.drawing = not self.drawing
            # If drawing is started, add an empty list to store the points
            if self.drawing:
                self.drawing_points.append([])
            else:
                # If drawing is stopped, add an empty list to separate lines
                self.drawing_points.append([])

        # If Ctrl+F is pressed, upload the screenshot to the server
        elif event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.send_screenshot()
            QtWidgets.QApplication.quit()

        # If Ctrl+C is pressed, take the screenshot and put it into the clipboard
        elif event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.take_screenshot()
            QtWidgets.QApplication.quit()



        # If the escape key is pressed, quit the application
        elif event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)



    def send_screenshot(self):
        # Get the screenshot
        screenshot = self.get_screenshot()
        
        # Save the screenshot to a temporary file
        filename = "cloudshot_" + datetime.datetime.now().strftime("(%d.%m.%Y_at_%H.%M)")
        screenshot.save(filename, "PNG")
        
        # Add the filename to the SCP command
        SCP_COMMAND = os.getenv("SCP")
        scp_command = SCP_COMMAND.replace("image", filename)
        
        # Execute the SCP command
        subprocess.run(scp_command, shell=True)

        # Delete the temporary file
        os.remove(filename)

        # Copy the filename to the clipboard
        send_to_clipboard(win32clipboard.CF_UNICODETEXT, os.getenv("IMAGE_SERVER_URL")+filename)



    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # Draw a semi-transparent black overlay on the whole screen
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        # If we have not started to draw the rectangle for the screenshot area, just return
        if self.start == self.end:
            return super().paintEvent(event)

        # Draw the rectangle for the screenshot area
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))

        # Draw the lines for the annotations
        if self.drawing_points:
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 3))  # Red color
            for points in self.drawing_points:
                if points:
                    for i in range(len(points) - 1):
                        painter.drawLine(points[i], points[i+1])

        return super().paintEvent(event)



    def mousePressEvent(self, event):
        # Add a condition to handle drawing
        if self.drawing:
            self.drawing_points[-1].append(event.pos())
            self.update()
        else:
            # When the mouse button is pressed, save the current cursor position
            # and update the display
            self.start = self.end = event.pos()
            self.update()

        return super().mousePressEvent(event)



    def mouseMoveEvent(self, event):
        # Add a condition to handle drawing
        if self.drawing:
            self.drawing_points[-1].append(event.pos())
            self.update()
        else:
            # When the mouse is moving, update the end point and the display
            self.end = event.pos()
            self.update()

        return super().mouseMoveEvent(event)



    def mouseReleaseEvent(self, event):
        # If in drawing mode, add an empty list to separate lines
        if self.drawing:
            self.drawing_points.append([])
        else:
            # If not in drawing mode, update the end point
            self.end = event.pos()
            self.update()

        return super().mouseReleaseEvent(event)



    def take_screenshot(self):
        # Get the screenshot and put it into the clipboard
        screenshot = self.get_screenshot()
        # Convert the screenshot to a QImage
        qimg = screenshot.toImage()

        # Save the QImage to a buffer, then create a PIL image from the buffer
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.ReadWrite)
        qimg.save(buffer, "PNG")

        # Create a BytesIO object and write the buffer data to it
        strio = BytesIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        img = Image.open(strio)

        # Convert the PIL image to BMP and remove the BMP header
        output = BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        # Send the image data to the clipboard
        send_to_clipboard(win32clipboard.CF_DIB, data)



    def save_screenshot(self):
        # Get the screenshot
        screenshot = self.get_screenshot()
        
        # Ask the user for a filename
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Screenshot", "cloudshot_" + datetime.datetime.now().strftime("(%d.%m.%Y_at_%H.%M)"), "PNG files (*.png);;All Files (*)"
        )
        if filename:
            # Save the screenshot to the file
            screenshot.save(filename, "PNG")



    def get_screenshot(self):
        return self.getWindow().copy(
            min(self.start.x(), self.end.x()) + 2,
            min(self.start.y(), self.end.y()) + 2,
            abs(self.start.x() - self.end.x()) - 2,
            abs(self.start.y() - self.end.y()) - 2,
        )



    def take_screenshot_and_convert_to_text(self):
        # Get the screenshot and convert it to a PIL Image
        screenshot = self.get_screenshot()
        
        # Convert the screenshot to a QImage
        qimg = screenshot.toImage()

        # Save the QImage to a buffer, then create a PIL image from the buffer
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.ReadWrite)
        qimg.save(buffer, "PNG")

        # Create a BytesIO object and write the buffer data to it
        strio = BytesIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        img = Image.open(strio)

        # Use Tesseract to convert the image to text
        text = pytesseract.image_to_string(img)

        # Send the text to the clipboard
        send_to_clipboard(win32clipboard.CF_UNICODETEXT, text)



def send_to_clipboard(clip_type, data):
    # Open the clipboard, clear it, then set the clipboard data
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()



def take_screenshot():
    # Disable High DPI scaling
    QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)

    # Create a QApplication instance
    app = QtWidgets.QApplication(sys.argv)

    # Create the main window and the snipper widget, then show the snipper
    window = QtWidgets.QMainWindow()
    snipper = Snipper(window)
    snipper.show()

    # Enter the application main loop
    sys.exit(app.exec_())



arg_parser = argparse.ArgumentParser(description=__doc__)
def main():
    # Parse the command line arguments
    args = arg_parser.parse_args()

    # Take the screenshot
    take_screenshot()

if __name__ == "__main__":
    main()