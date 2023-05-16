# CloudShot v1.0

CloudShot is a nimble and efficient script engineered for Windows, designed for capturing and handling screenshots with ease.

This tool provides you with the ability to:

 - Select a specific section of your screen.
 - Perform quick edits using a red marker.
 - Copy the screenshot to your clipboard for immediate use.
 - Save the screenshot locally on your device for future reference.
 - Extract text from the image using Tesseract OCR technology and copy it to the clipboard.
 - Upload the screenshot to a private server using SCP, making it compatible with platforms like Oracle, Amazon, or Google VPS.

It requires an average of 48 MB of RAM and is available for Windows.

Based on:
[Lightshot](https://app.prntscr.com/)
[Gyazo](https://gyazo.com/)
[Textshot](https://github.com/ianzhao05/textshot/)

# Instalation/Configuration

### Prerequisites
To use the tool, you need to have the following prerequisites installed:

##### Required
 - [Python](https://www.python.org/downloads/): Python is a programming language required to run the tool. You should download and install Python from the official Python website. Make sure to choose the appropriate version for your operating system.
 - [pip - package python installer](https://pypi.org/project/pip/): pip is a package installer for Python that allows you to install additional libraries and dependencies. It is usually included with Python installation, but you may need to check if it's properly installed and working.
 
##### Optional
 - [OpenSSH (or any which provides the scp command)](https://www.openssh.com/): OpenSSH is a widely-used suite of secure networking utilities that includes the scp command. This command is used for secure file transfer between systems. You can install OpenSSH or any alternative that provides the scp command if you want to use the tool's functionality related to uploading screenshots to a server.
 - [Google's Tesseract OCR Engine](https://github.com/UB-Mannheim/tesseract/wiki/): Tesseract is an open-source OCR engine that is used for text extraction from images. You should follow the installation instructions provided in the link to set up Tesseract on your system.

Once you have installed the prerequisites, you can proceed with the tool's installation and configuration process.

### Configuration
First of all, you need to rename the file ".env_default" to ".env". Then, you can proceed to edit the configuration.
```
# REQUIRED
ACTIVATE_KEY=
ALERT=
SERVER=
TESSERACT=

# SERVER
SCP=
IMAGE_SERVER_URL=
```
##### Required:
ACTIVATE_KEY - The key or key combination to take a screenshot. Once the screenshot is taken, you have access to options like cropping, editing, saving, and copying the screenshot, examples:  
✅ctrl+p  
✅ins  
✅F8  

ALERT - Enable or disable notifications. It can be set to "true" or "false".

SERVER - Enable or disable uploading to a private server (Ctrl+F). It can be set to "on" or any other value for disable it.

TESSERACT - Enable or disable text detection (Ctrl+A). It can be set to "on" or any other value for disable it.

##### Server (if the "SERVER" key is set to "on"):
SCP - The command for file upload, using the word "image" instead the file. Examples:  
✅scp image user@cloudshot.com:/var/www/screenshots  
❌scp picture user@cloudshot.com:/var/www/screenshots  
✅scp image user@192.168.1.1:/home/user  
❌scp any user@192.168.1.1:/home/user  

IMAGE_SERVER_URL - The URL where the images will be uploaded (with a "/" at the end). Examples:  
✅https://cloudshot.com/screenshots/  
❌https://cloudshot.com/screenshots  

You can configure an Apache2/Nginx server on your system to provide immediate access to the uploaded screenshots.

### Instalation
 - Clone this repository:
```
git clone git@github.com:borrageiros/cloudshot.git
```
 - Navigate to the directory:
```
cd cloudshot
```
 - Install the dependencies:
```
pip install -r requirements.txt
```
 - Run the "cloudshot.pyw" file to activate the program.

## IMPORTANT
I recommend placing the script in the Windows startup folder so that it runs automatically on system startup. By default, the startup folder is located at:
(The "cloudshot.pyw" and ".env" files)
```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```
# Use
Tutorial in coming
