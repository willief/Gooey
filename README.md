# Gooey
SAFE Command Line GUI 

GUI application built with the tkinter module in Python. It provides a simple interface for interacting with the safe command-line utility for the Safe Network.

The application has two main functions:

"GET" - retrieves a file from the Safe Network and opens it.
"PUT" - uploads a file to the Safe Network.
The user can either enter a XorUrl in the input field and "GET", or select a file using the "Browse Files" button and "PUT". The output of the "PUT" function is displayed in a text box.

The code makes use of the subprocess module to run shell commands, and the os module to open the retrieved file. The filedialog module from the tkinter library is used for selecting a file.

The "Clear" and "Clear PUT" buttons allow the user to clear the input fields, and the "PUT" output box respectively.

Very basic, please contribute if you find it useful.

To run this code (only tested on linux), you need to have Python installed on your system. Additionally, the code uses the Tkinter and subprocess modules, so you need to make sure that these are installed in your Python environment. To check if you have these modules installed, you can run the following command in your terminal or command prompt:

`pip show tkinter` <br />
`pip show subprocess`

If the modules are not installed, you can install them by running the following command:

`pip install tkinter` <br />
`pip install subprocess`

From a terminal you can start Gooey with: <br />
`python3 gooey.py`
