from tkinter import *
from tkinter.filedialog import Open

class FileOpenLEB(Frame):
    """
    This class gives a label, button, and text entry box, all on a single
    line, which can be shoved wherever the user likes and used to open files
    with a file open dialog. It subclasses Frame and so supports all the usual 
    methods. Best if used inside a class so the file path can be stored somewhere.
    """
    def __init__(self, parent=None, labelText='', buttonText='', diadir='', 
        diatype=None):
        Frame.__init__(self, parent)
        self.ourLabel = Label(self, text=labelText, width=30)
        self.ourText = Entry(self, width=45)
        self.ourButton = Button(self, text=buttonText, command=self.retrieve_path)
        
        self.ourLabel.pack(side="left", fill="x")
        self.ourText.pack(side="left", padx=5, pady=5, fill="x")
        self.ourButton.pack(side="left", padx=5, pady=5, fill="x")
        
        self.initialDir = diadir
        self.filetypes = diatype
        self.filePath = None
    
    def change_label_text(self, newText):
        self.ourLabel.config(text=newText)
    
    def change_button_text(self, newText):
        self.ourButton.config(text=newText)
        
    def retrieve_path(self):
        self.filePath = Open(initialdir=self.initialDir, 
            filetypes=self.filetypes).show()
        self.change_textbox(self.filePath)
    
    def change_textbox(self, newText):
        self.ourText.delete(0, END)
        self.ourText.insert(0, newText)
        
    def get_filePath(self):
        return self.filePath
