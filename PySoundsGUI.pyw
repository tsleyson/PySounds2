# PySoundsGUI.py
# A simple GUI to work with PySounds from. 

import sys, os, classPySounds2, testPySounds2
from tkinter import *
from tkinter.filedialog import Open
from tkinter.messagebox import askyesno, showwarning
from tkinter.scrolledtext import ScrolledText
from FileOpenLEB import FileOpenLEB

class PySoundsGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.populate_widgets()
        self.changer = None
        self.fileOnly = False
        self.pack()
        
    def populate_widgets(self):
        # Make a frame to put the frames for the file open dialogs inside.
        self.fileFrames = Frame(self)
        self.lexFrame = FileOpenLEB(self.fileFrames, "Enter the path of a .lex file.",
            "Browse...", "I:/PySounds", [("Wordlists", ".lex")])
        self.scFrame = FileOpenLEB(self.fileFrames, "Enter the path of a .sc file.", 
            "Browse...", "I:/PySounds", [("Sound change files", ".sc")])
    
        # Now make the button to apply changes to the wordlist.
        self.buttonFrame = Frame(self, relief="groove", border=3)
        Button(self.buttonFrame, text="Apply changes", 
            bg="#8080FF", fg="white", padx=20, 
            command=self.change_words).pack(fill=BOTH,
            expand=YES)
        
        # The display options panel comes next.
        self.displayOptions = Frame(self, border=3)
        self.printmode = StringVar(self, '-a')
        Radiobutton(self.displayOptions, text="original word ==> new word",
            variable=self.printmode, value="-a").pack(anchor=NW)
        Radiobutton(self.displayOptions, text="original word [new word]",
            variable=self.printmode, value="-b").pack(anchor=NW)
        Radiobutton(self.displayOptions, text="new word alone",
            variable=self.printmode, value="-o").pack(anchor=NW)
        Checkbutton(self.displayOptions, text="Do not print output to screen",
            command=self.toggle_file_only).pack(side="right")
            
        # Now deal with the text display.
        self.displayWindow = ScrolledText(self, width=80, bg="light blue",
            font=('Times New Roman', 12, 'normal'))
            
        # Now pack everything that wasn't autopacked above.
        self.lexFrame.pack(side="top")
        self.scFrame.pack(side="bottom")
        #self.changeButton.pack()
        self.fileFrames.pack(side="top")
        self.displayOptions.pack(side="left")
        self.buttonFrame.pack(side="top")
        self.displayWindow.pack(side="top")
        
    def change_words(self):
        #self.set_printmode('-a')
        try:
            # Only assign scname to a variable since we'll need it later
            # for the .pso file; not so with the lexicon.
            scfile = self.scFrame.get_filePath()
            if not self.changer:
                self.changer = classPySounds2.PySounds2(self.lexFrame.get_filePath(),
                    scfile)
                    
            # cont = True
            originals = self.changer.getUnalteredWords()
            # while cont:
            out = open(os.path.splitext(scfile)[0] + '.pso', "w")
            new = self.changer.applyRules(scfile)
            formattedWords = []
            self.displayWindow.delete('1.0', END)
            if self.printmode.get() == '-a':
                formattedWords = testPySounds2.print_with_arrow(originals, 
                    new, out)
            elif self.printmode.get() == '-b':
                formattedWords = testPySounds2.print_with_brackets(originals, 
                    new, out)
            elif self.printmode.get() == '-o':
                formattedWords = testPySounds2.print_alone(new, out)
            
            if not self.fileOnly:
                self.displayWindow.insert('1.0', '\n'.join(formattedWords))
                    
               # cont = askyesno("Repeat?", "Make changes to rules and run again?")
        except IOError as i:
            showwarning("Invalid file", i.msg)
        except SyntaxError as s:
            showwarning("Invalid rule or category", s.msg)
        
    
    #~ def set_printmode(self, printmode):
        #~ self.printmode = printmode
        
    def toggle_file_only(self):
        self.fileOnly = not self.fileOnly
    
if __name__ == '__main__':
    mainWin = Tk()
    mainWin.title("PySounds")
    mainWin.iconbitmap("Nino.ico")
    mainGUI = PySoundsGUI(mainWin)
    mainWin.mainloop()
