# Uncomment the following lines and comment out the next two to make
# this program work with Python 2.x.

#~ from Tkinter import *
#~ from tkFileDialog import Open

from tkinter import *
from tkinter.filedialog import Open

def retrieve_lexfile(lexEntry):
    lexname = Open(initialdir="I:/Elmian final", filetypes=[("Wordlists",
        ".lex")]).show()
    if lexEntry.get() != '':
        # Then there's already text that we need to get rid of.
        lexEntry.delete(0, END)
    lexEntry.insert(0, lexname)
# End retrieve_lexfile

def retrieve_scfile(scEntry):
    scname = Open(initialdir="C:/Users/Mario Batali", 
        filetypes=[("Sound Change Files", ".sc")]).show()
    if scEntry.get() != '':
        scEntry.delete(0, END)
    scEntry.insert(0, scname)
# End retrieve_scfile
    
class LabelEntryButtonTriad(Frame):
    pass

class DisplayWindow(Frame):
    pass
    
if __name__ == '__main__':
    # Initialize the main window and frames.
    top = Tk()
    mainWindow = Frame(top, relief="groove", border=3, pady=5)
    mainWindow.pack(side="top")
    mainWindow.master.title("PySounds")
    
    # Define the label and entry for the lex file.
    lexLabel = Label(mainWindow, text="Enter the path of a .lex file")
    lexLabel.pack(side="left", fill="x", padx=5, pady=5)
    lexEntry = Entry(mainWindow)
    lexEntry.pack(side="left", padx=5, pady=5)
    
    # Define the button and dialog for the lex file.
    lexButton = Button(mainWindow, text="Browse...", 
        command=lambda : retrieve_lexfile(lexEntry))
    lexButton.pack(side="left", padx=5, pady=5)
    
    # Define the frame for getting the sc file.
    scFrame = Frame(top, relief="groove", border=3, pady=5)
    scFrame.pack(side="bottom")
    
    scLabel = Label(scFrame, text="Enter the path of a .sc file.")
    scLabel.pack(side="left", fill="x", padx=5, pady=5)
    scEntry = Entry(scFrame)
    scEntry.pack(side="left", padx=5, pady=5)
    
    # Define button and dialog for sound change file.
    scButton=Button(scFrame, text="Browse...",
        command=lambda : retrieve_scfile(scEntry))
    scButton.pack(side="left", padx=5, pady=5)
    
    # Define the 
    
    top.mainloop()
