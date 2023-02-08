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
