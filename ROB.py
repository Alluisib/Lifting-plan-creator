import tkinter as tk

#Dictionary for ships and Max/Min ROBs
ships = ["AIDAaura", "AIDAdiva"]
Max = {"AIDAaura":(("HFO","MGO"),(1600,1300)),"AIDAbella":(("HFO","MGO"),(1600,1300)),"AIDAblu":(("HFO","MGO"),(1600,1300)),
       "AIDAcosma":(("LNG","MGO"),(1600,1300)),"AIDAdiva":(("HFO","MGO"),(1600,1300))}
Min = {"AIDAaura":(("HFO","MGO"),(300,300)),"AIDAbella":(("HFO","MGO"),(600,300)), "AIDAblu":(("HFO","MGO"),(600,300)),
       "AIDAcosma":(("LNG","MGO"),(300,300)), "AIDAdiva":(("HFO","MGO"),(300,300))}

global Starting_ROB_Dict
Starting_ROB_Dict = {"AIDAaura":(0,400), "AIDAbella":(1000,500),"AIDAblu":(1000,500),"AIDAcosma":(1000,500),"AIDAdiva":(1000,500)}

def get_starting_ROBs(ships):

    def get_values():
        # Pressing submit closes the window and sets the two ROB figures based on the entries
        Starting_ROB_Dict[ship] = (entry_First_ROB.get(), entry_Second_ROB.get())
        window_ROB_entry.destroy()

    for ship in ships:
        window_ROB_entry = tk.Tk()
        window_ROB_entry.geometry('300x150')
        window_ROB_entry.title("Enter/confirm ROB Information")

        # Create a new frame `frm_form` to contain the Label
        # and Entry widgets for entering address information
        frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=4)
        # Pack the frame into the window
        frm_form.pack(fill="both", expand = True)

        label_First_ROB = tk.Label(master=frm_form, text="Start " + Max[ship][0][0] + " ROB")
        entry_First_ROB = tk.Entry(master=frm_form, width = 10)
        entry_First_ROB.insert(0, str(round(0.7 * Max[ship][1][0], 1)))

        label_First_ROB.grid(row=0,column=0, sticky="e")
        entry_First_ROB.grid(row=0, column=1)

        label_Second_ROB = tk.Label(master=frm_form, text="Start " + Max[ship][0][1] + " ROB")
        entry_Second_ROB = tk.Entry(master=frm_form, width = 10)
        entry_Second_ROB.insert(0, str(round(0.7 * Max[ship][1][1], 1)))

        label_Second_ROB.grid(row=1, column=0)
        entry_Second_ROB.grid(row=1, column=1)

        # Create a new frame `frm_buttons` to contain the
        # Submit and Clear buttons. This frame fills the
        # whole window in the horizontal direction and has
        # 5 pixels of horizontal and vertical padding.
        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

        # Create the "Submit" button and pack it to the
        # right side of `frm_buttons`
        btn_submit = tk.Button(master=frm_buttons, text="Submit",command = get_values)
        btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

        window_ROB_entry.mainloop()
