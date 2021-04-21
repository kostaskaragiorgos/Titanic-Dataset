from tkinter import Menu, messagebox as msg, filedialog, Tk, Label, Text, Button, END
import pandas as pd


def aboutmenu():
    """ about menu function """
    msg.showinfo("About", "Titanic survival \nVersion 1.0")

class Titanicsurvival():
    def __init__(self,master):
        self.master = master
        self.master.title("Titanic Survival")
        self.master.geometry("250x200")
        self.master.resizable(False, False)
        self.filename = ""

        self.nameleb = Label(self.master, text="Enter name")
        self.nameleb.pack()
        
        self.nametext = Text(self.master, height=1)
        self.nametext.pack()

        self.ageleb = Label(self.master, text="Enter age")
        self.ageleb.pack()

        self.agetext = Text(self.master, height=1, width=3)
        self.agetext.pack()

        self.fareleb = Label(self.master, text="Enter fare")
        self.fareleb.pack()

        self.faretext = Text(self.master, height=1, width=7)
        self.faretext.pack()

        self.predictbutton = Button(self.master, text="PREDICT", command=self.predict)
        self.predictbutton.pack()

        self.clearbutton = Button(self.master, text="CLEAR", command=self.clear)
        self.clearbutton.pack()

        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu,tearoff = 0)
        self.file_menu.add_command(label="Insert a csv", accelerator='Ctrl+O', command = self.insertfile)
        self.file_menu.add_command(label="Close file", accelerator='Ctrl+F4', command=self.closefile)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.about_menu = Menu(self.menu,tearoff = 0)
        self.about_menu.add_command(label = "About",accelerator= 'Ctrl+I',command= aboutmenu)
        self.menu.add_cascade(label="About",menu=self.about_menu)
        
        self.help_menu = Menu(self.menu,tearoff = 0)
        self.help_menu.add_command(label = "Help",accelerator = 'Ctrl+F1',command=self.helpmenu)
        self.menu.add_cascade(label="Help",menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event: self.helpmenu())
        self.master.bind('<Control-i>',lambda event: aboutmenu())
        self.master.bind('<Control-o>', lambda event: self.insertfile())
        self.master.bind('<Control-F4>', lambda evemt: self.closefile())

    

    def check_columns(self):
        """ checks the columns name from the importrd .csv file """
        if all([item in self.df.columns for item in ['PassengerId','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']]):
            msg.showinfo("SUCCESS", "CSV FILE ADDED SUCCESSFULLY")
        else:
            self.filename = ""
            msg.showerror("ERROR", "NO PROPER CSV ")

    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
    
    def helpmenu(self):
        pass

    def file_input_validation(self):
        """ user input validation"""
        if ".csv" in self.filename:
            self.df = pd.read_csv(self.filename)
            self.check_columns()
        else:
            self.filename = ""
            msg.showerror("ERROR", "NO CSV IMPORTED")

    def insertfile(self):
        if ".csv" in self.filename:
            msg.showerror("ERROR", "A CSV FILE IS ALREADY OPEN")
        else:
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select csv file",
                                                       filetypes=(("csv files", "*.csv"),
                                                                  ("all files", "*.*")))
            self.file_input_validation()

    def closefile(self):
        """ closes the csv file """
        if not ".csv" in self.filename:
            msg.showerror("ERROR", "NO CSV TO CLOSE")
        else:
            self.filename = ""
            msg.showinfo("SUSSESS", "YOUR CSV FILE HAS SUCCESFULLY CLOSED")

    
    def predict(self):
        pass

    def clear(self):
        self.agetext.delete(1.0, END)
        self.nametext.delete(1.0, END)

def main():
    root=Tk()
    Titanicsurvival(root)
    root.mainloop()
    
if __name__=='__main__':
    main()