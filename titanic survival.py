from tkinter import Menu, messagebox as msg, filedialog, Tk, Label, Text, Button, END, StringVar, OptionMenu
from tkinter.constants import E
from tkinter.messagebox import askyesno
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

def aboutmenu():
    """ about menu function """
    msg.showinfo("About", "Titanic survival \nVersion 1.0")

def helpmenu():
    msg.showinfo("Help", "Insert a csv file to predict the titanic survivals")

class Titanicsurvival():
    def __init__(self, master):
        self.master = master
        self.master.title("Titanic Survival")
        self.master.geometry("300x350")
        self.master.resizable(False, False)
        self.filename = ""
        model_filename = 'models/MLPClassifier30798.sav'
        self.loadedmodel = pickle.load(open(model_filename, 'rb'))
        self.importeddf = ""
        self.predictions = ""

        self.nameleb = Label(self.master, text="Enter name")
        self.nameleb.pack()
        
        self.nametext = Text(self.master, height=1)
        self.nametext.pack()

        self.ageleb = Label(self.master, text="Enter age")
        self.ageleb.pack()

        self.agetext = Text(self.master, height=1, width=3)
        self.agetext.pack()

        self.nofsiblleb = Label(self.master, text="Enter the number of Siblings/Spouses")
        self.nofsiblleb.pack()
        
        
        self.nofparentstext = Text(self.master, height=1, width=3)
        self.nofparentstext.pack()

        self.noffammebleb = Label(self.master, text="Enter the number of Parents/Children")
        self.noffammebleb.pack()

        self.noffammebtext = Text(self.master, height=1, width=3)
        self.noffammebtext.pack()

        self.fareleb = Label(self.master, text="Enter fare")
        self.fareleb.pack()

        self.faretext = Text(self.master, height=1, width=7)
        self.faretext.pack()

        self.sexlist = ["Male", "Female"]
        self.sexstring = StringVar(master)
        self.sexstring.set("Select a Sex")
        self.sexpopup = OptionMenu(self.master, self.sexstring, *self.sexlist)
        self.sexpopup.pack()

        self.pclasslist = ["1st", "2nd", '3rd']
        self.pclassstring = StringVar(master)
        self.pclassstring.set("Select a Ticket class")
        self.pclasspopup = OptionMenu(self.master, self.pclassstring, *self.pclasslist)
        self.pclasspopup.pack()

        self.embarkedlist = ["C", "Q", "S"]
        self.embarkedstring = StringVar(master)
        self.embarkedstring.set("Select a Port of Embarkation")
        self.embarkedpopup = OptionMenu(self.master, self.embarkedstring, *self.embarkedlist)
        self.embarkedpopup.pack()

        self.predictbutton = Button(self.master, text="PREDICT", command=self.predict)
        self.predictbutton.pack()

        self.clearbutton = Button(self.master, text="CLEAR", command=self.clear)
        self.clearbutton.pack()

        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Insert a csv", accelerator='Ctrl+O', command=self.insertfile)
        self.file_menu.add_command(label="Close file", accelerator='Ctrl+F4', command=self.closefile)
        self.file_menu.add_command(label="Save file", accelerator='Ctrl+S', command=self.savepredictions)
        self.file_menu.add_command(label="Save to existed file", accelerator='Alt+S', command=self.savetoexisted)
        self.file_menu.add_command(label="Exit", accelerator= 'Alt+F4',command=self.exitmenu)
        self.menu.add_cascade(label = "File", menu=self.file_menu)

        self.show_menu = Menu(self.menu, tearoff=0)
        self.show_menu.add_command(label="Show Predictions", accelerator='Ctrl+ F5',command=self.showpredictions)
        self.menu.add_cascade(label="Show", menu=self.show_menu)
        
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Clear All", accelerator='Ctrl+Z', command=self.clear)
        self.submenuclear = Menu(self.edit_menu, tearoff=0)
        self.submenuclear.add_command(label="Name", accelerator="Ctrl+T", command=lambda: self.clear(self.nametext))
        self.submenuclear.add_command(label="Age", accelerator="Alt+T", command=lambda: self.clear(self.agetext))
        self.submenuclear.add_command(label="Siblings/Spouses", accelerator="Alt+N", command=lambda: self.clear(self.noffammebtext))
        self.submenuclear.add_command(label="Parents/Children", accelerator="Ctrl+N", command=lambda: self.clear(self.nofparentstext))
        self.submenuclear.add_command(label="Fare", accelerator="Alt+Z", command=lambda: self.clear(self.faretext))
        self.edit_menu.add_cascade(label="Clear text",
                                   menu=self.submenuclear, underline=0)
        self.submenureset = Menu(self.edit_menu, tearoff=0)
        self.submenureset.add_command(label="Sex", accelerator="Alt+M", command=lambda: self.clear(toclear=self.sexstring, textflag=False, text="Select a Sex"))
        self.submenureset.add_command(label="Ticket class", accelerator="Ctrl+M", command=lambda: self.clear(toclear=self.pclassstring, textflag=False, text="Select a Ticket class"))
        self.submenureset.add_command(label="Embarkation", accelerator="Ctrl+K", command=lambda: self.clear(toclear=self.embarkedstring, textflag=False, text="Select a Port of Embarkation"))
        self.edit_menu.add_cascade(label="Reset Options",
                                   menu=self.submenureset, underline=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command= aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        self.master.bind('<Control-F5>', lambda event: self.showpredictions())
        self.master.bind('<Control-z>', lambda event: self.clear(None))
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Control-o>', lambda event: self.insertfile())
        self.master.bind('<Control-F4>', lambda evemt: self.closefile())
        self.master.bind('<Control-t>', lambda event: self.clear(self.nametext))
        self.master.bind('<Alt-t>', lambda event: self.clear(self.agetext))
        self.master.bind('<Alt-z>', lambda event: self.clear(self.faretext))
        self.master.bind('<Alt-n>', lambda event: self.clear(self.nofparentstext))
        self.master.bind('<Control-n>', lambda event: self.clear(self.noffammebtext))
        self.master.bind('<Control-m>', lambda event: self.clear(toclear=self.pclassstring, textflag=False, text="Select a Ticket class"))
        self.master.bind('<Alt-m>', lambda event: self.clear(toclear=self.sexstring, textflag=False, text="Select a Sex"))
        self.master.bind('<Control-k>', lambda event: self.clear(toclear=self.embarkedstring, textflag=False, text="Select a Port of Embarkation"))

    def checktosave(self, filename):
        if filename is None or filename == "":
            msg.showerror("ERROR", "NO FILE SAVED")
        else:
            np.savetxt(str(filename)+".csv", self.predictions)
            msg.showinfo("SUCCESS", "CSV FILE SAVED SUCCESSFULLY")

    def savetoexisted(self):
        pass

    def savepredictions(self):
        """ saves the predictions to a csv file"""
        if self.predictions == "":
            msg.showerror("ERROR", "NO PREDICTIONS TO SAVE")
        else:
            filenamesave = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                                filetypes=(("csv files", "*.csv"),
                                                                            ("all files", "*.*")))
            self.checktosave(filenamesave)



    def showpredictions(self):
        """ show predictions function """
        if self.predictions == "":
            msg.showerror("ERROR", "NO PREDICTIONS")
        else:
            msg.showinfo("PREDICTIONS", str(self.predictions))

    def check_columns(self):
        """ checks the columns name from the importrd .csv file """
        if all([item in self.df.columns for item in ['PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']]):
            self.statechange("disable")
            msg.showinfo("SUCCESS", "CSV FILE ADDED SUCCESSFULLY")
            self.importeddf = pd.read_csv(self.filename)
        else:
            self.filename = ""
            msg.showerror("ERROR", "NO PROPER CSV ")

    def exitmenu(self):
        """ exit menu function """
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
    
    def fixinsertedfile(self):
        """ 
        Creates a numpy array in order to make the predictions.
        Returns:
            X: numpy array ready to make the predictions
        
        """
        self.importeddf['Age'] = self.importeddf['Age'].fillna(self.importeddf['Age'].mean())
        self.importeddf['Fare'] = self.importeddf['Fare'].fillna(self.importeddf['Fare'].mean())
        agelabels = ['child','adult','old']
        self.importeddf['age_group'] = pd.cut(self.importeddf['Age'], bins=3, labels=agelabels)
        self.importeddf['age_group'] = self.importeddf['age_group'].fillna('adult')
        labelsfare = ['cheap', 'normal', 'expensive']
        self.importeddf['Fare_group'] = pd.cut(self.importeddf['Fare'], bins=3, labels=labelsfare)
        self.importeddf['Fare_group'] = self.importeddf['Fare_group'].fillna('cheap')
        self.importeddf.drop(columns=['PassengerId', 'Name', 'Cabin', 'Embarked', 'Ticket', 'Fare', 'Age'], inplace=True)
        X = self.importeddf.iloc[:, :].values
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1, 4, -1])], remainder='passthrough')
        X = np.array(ct.fit_transform(X))
        sc = StandardScaler()
        X[:, 2:] = sc.fit_transform(X[:, 2:])
        return X


    def statechange(self, state):
        """ changes the state of buttons, texts etc.. """
        self.agetext.config(state=state)
        self.nametext.config(state=state)
        self.faretext.config(state=state)
        self.sexpopup.config(state=state)
        self.pclasspopup.config(state=state)
        self.embarkedpopup.config(state=state)
        self.noffammebtext.config(state=state)
        self.nofparentstext.config(state=state)


    def file_input_validation(self):
        """ user input validation"""
        if ".csv" in self.filename:
            self.df = pd.read_csv(self.filename)
            self.check_columns()
        else:
            self.filename = ""
            msg.showerror("ERROR", "NO CSV IMPORTED")

    def insertfile(self):
        """ insert csv function """
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
            self.statechange("normal")
            self.filename = ""
            self.predictions = ""
            msg.showinfo("SUSSESS", "YOUR CSV FILE HAS SUCCESFULLY CLOSED")
    

    def checksetoptions(self,userinput):
        """ checks the user's options """
        if self.embarkedstring.get() != "Select a Port of Embarkation" and self.sexstring.get() != "Select a Sex" and self.pclassstring.get() != "Select a Ticket class":
            userinput.append([str(self.embarkedstring.get()), str(self.sexstring.get()), str(self.pclassstring.get())])
        else:
            msg.showerror("VALUE ERROR", "SELECT A VALID OPTION")
            self.clearprediction("set")
    
    def checknumbers(self, userinput):
        """ checks if the user has inserted valid number inputs """
        if self.embarkedstring.get() != "Select a Port of Embarkation" and self.sexstring.get() != "Select a Sex" and self.pclassstring.get() != "Select a Ticket class":
            pass
        else:
            msg.showerror("VALUE ERROR", "ENTER VALID NUMBERS")
            self.clearprediction("number")


    
    def predict(self):
        """ predict button function """

        if self.filename != "" and self.predictions != "":
            msg.showerror("ERROR", "PREDICTIONS HAVE ALREADY BE DONE")
        elif self.filename != "":
            X = self.fixinsertedfile()
            self.predictions= self.loadedmodel.predict(X).tolist()
            answer = askyesno(title='Save predictions',
                    message = 'Do you want to save the predictions?')
            if answer:
                self.savepredictions()
            else:
                msg.showinfo("NO", "NO PREDICTIONS SAVED")
        else:
            userinput = []
            self.checksetoptions(userinput)
            self.checknumbers(userinput)

    
    def clear(self, toclear=None, textflag = True, text  = ""):
        """ reset button function """
        if toclear is None:
            self.pclassstring.set("Select a Ticket class")
            self.sexstring.set("Select a Sex")
            self.embarkedstring.set("Select a Port of Embarkation")
            self.noffammebtext.delete(1.0, END)
            self.agetext.delete(1.0, END)
            self.nametext.delete(1.0, END)
            self.faretext.delete(1.0, END)
            self.nofparentstext.delete(1.0, END)
        elif textflag:
            toclear.delete(1.0,END)
        else:
            toclear.set(str(text))

    def clearprediction(self, option):
        """ clear based on options """
        if option == "set":
            self.pclassstring.set("Select a Ticket class")
            self.sexstring.set("Select a Sex")
            self.embarkedstring.set("Select a Port of Embarkation")
        else:
            self.noffammebtext.delete(1.0, END)
            self.agetext.delete(1.0, END)
            self.nametext.delete(1.0, END)
            self.faretext.delete(1.0, END)
            self.nofparentstext.delete(1.0, END)


def main():
    """ main function"""
    root = Tk()
    Titanicsurvival(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()