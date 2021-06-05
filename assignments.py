import tkinter as tk
import tkinter.messagebox
import json

def adddata(data):
    try:
        fhand = open("data.txt","r") #opening the file in read mode
        filestuff = json.load(fhand) #converting the data to JSON and loading to data variable
        fhand.close()
    except:
        filestuff =[] #makes a list data in case there is no file

    filestuff.append(data) #adds the data from the dictionary data_to_add to data list

    try:
        fhand = open("data.txt","w") #opening a file in write mode
        json.dump(filestuff,fhand) #converting the data to JSON and writing to that file
        fhand.close()
    except:
        print("Some error occured")

    tkinter.messagebox.showinfo("Success","Successfully added. Please restart the app to see update")



def delete(index):
    fhand = open("data.txt","r") #opening the file in read mode
    filestuff = json.load(fhand) #converting the data to JSON and loading to data variable
    fhand.close()
    try:
        index = int(index)
        if index > len(filestuff) or index < 0:
            tkinter.messagebox.showinfo("Error","Enter valid index")
        else:
            del filestuff[index-1]

            fhand = open("data.txt","w") #opening a file in write mode
            json.dump(filestuff,fhand) #converting the data to JSON and writing to that file
            fhand.close()

            tkinter.messagebox.showinfo("Success","Successfully removed. Please restart the app to see the update")

    except:
        tkinter.messagebox.showinfo("Error","Entera numeric value")


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='yellow')
        label = tk.Label(self,bg="yellow",text='Manage your assignment',height="3",width="50",font='Helvetica 18 bold')
        label.pack()

        Button = tk.Button(self, text="View assignment", font= "Helvetica 18",height="7",width="50", command=lambda: controller.show_frame(ThirdPage))
        Button.pack(side="bottom")
        Button = tk.Button(self, text="Add assignment", font= "Helvetica 18",height="7",width="50", command=lambda: controller.show_frame(SecondPage))
        Button.pack(side="bottom")



class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='yellow')

        label = tk.Label(self,bg="yellow",text='Manage your assignment',height="3",width="50",font='Helvetica 18 bold')
        label.pack()
        e1 = tk.Entry(self,width="60",)
        e1.insert("end",'Enter you assignment Here')
        e1.pack()
        e2 = tk.Entry(self,width="60")
        e2.insert("end",'Enter deadline here')
        e2.pack()
        Button = tk.Button(self, text="Add", font= "Helvetica 18",height="5",width="50",command=lambda:[adddata({"assignment":e1.get(),"deadline":e2.get(),"status":"Not started"}), controller.show_frame(SecondPage),e1.delete(0, 'end'),e2.delete(0, 'end')])
        Button.pack(side="bottom")
        Button = tk.Button(self, text="Home", font= "Helvetica 18",height="6",width="50", command=lambda:controller.show_frame(FirstPage))
        Button.pack(side="bottom")




class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self,bg="yellow",text='Your assignments',height="3",width="50",font='Helvetica 18 bold')
        label.pack()
        try:
            fhand = open("data.txt","r") #opening the file in read mode
            filestuff = json.load(fhand) #converting the data to JSON and loading to data variable
            fhand.close()
        except:
            filestuff =[]

        if len(filestuff) < 1:
            label = tk.Label(self,bg="yellow",text='No assignments added',height="3",width="50",font='Helvetica 18')
            label.pack()
            Button = tk.Button(self, text="Home", font= "Helvetica 18",height="3",width="50", command=lambda: controller.show_frame(FirstPage))
            Button.pack(side="bottom")
        else:
            count= 1
            for subject in filestuff:
                assignments = subject["assignment"]
                deadline = subject["deadline"]
                status = subject["status"]

                label = tk.Label(self,text=f'{count}){assignments}**{deadline}**',width="55",font='Helvetica 17',anchor='w')
                count+=1
                label.pack()

            e = tk.Entry(self,width="60")
            e.insert("end",'Enter assignment number to remove')
            Button1 = tk.Button(self, text="Delete", font= "Helvetica 18",height="3",width="50", command=lambda:[delete(e.get()), e.delete(0, 'end')])
            Button2 = tk.Button(self, text="Home", font= "Helvetica 18",height="3",width="50", command=lambda: controller.show_frame(FirstPage))
            Button2.pack(side="bottom")
            Button1.pack(side="bottom")
            e.pack(side="bottom")


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a window
        window = tk.Frame(self)
        window.pack()


        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Assignment management")


app = Application()
app.mainloop()
