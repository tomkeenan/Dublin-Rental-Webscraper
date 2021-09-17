import webbrowser
from tkinter import *
from tkinter import ttk
import pandas as pd
from Scraper import Scraper


def center(win,w,h):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    # get screen width and height
    ws = win.winfo_screenwidth()  # width of the screen
    hs = win.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))


# creates a pop to let user know data has been loaded
def create_popup():
    pop_up = Toplevel()
    pop_up.title("Window")
    center(pop_up, 200, 50)
    label = Label(pop_up, text="Data loaded!", height=0, width=50)
    ok_button = Button(pop_up, text="OK", command=lambda: pop_up.destroy())
    label.pack()
    ok_button.pack()


class GUI:
    current_file = ''

    @staticmethod
    def start():
        """
        runs the web-scraper to pull rental data to display
        opens a popup window when complete
        """
        scraper = Scraper()
        scraper.search()
        create_popup()

    def filter(self, min_price, max_price, min_beds, max_beds):
        """
        filters the data to show only data within parameters entered
        :param text from all entry boxes in the gui
        """
        df = pd.read_csv(self.current_file)
        try:
            filtered_df = df[((float(min_price) <= df['Price per month €']) & (df['Price per month €'] <= float(max_price))) & ((float(min_beds) <= df['Beds']) & (df['Beds'] <= float(max_beds)))]
            self.load_df(filtered_df)
        except ValueError:
            try:
                filtered_df = df[((float(min_price) <= df['Price per month €']) & (df['Price per month €'] <= float(max_price)))]
                self.load_df(filtered_df)
            except ValueError:
                try:
                    filtered_df = df[(float(min_beds) <= df['Beds']) & (df['Beds'] <= float(max_beds))]
                    self.load_df(filtered_df)
                except ValueError:
                    print('catch empty value')

    def on_double_click(self, event):
        """
        opens link in db on double click
        :param event from double click
        """
        selected_item = self.tree.focus()
        col = self.tree.identify_column(event.x)
        if col == '#5':
            link = list(self.tree.item(selected_item).values())[2][4]
            webbrowser.open_new(f"{link}")

    def load_df(self, df):
        """
        loads a dataframe to the tree view to display for the user
        adds tags to each entry to allow the colouring of alternative rows
        :param df:
        """
        self.clear_data()
        self.tree['columns'] = list(df.columns)
        self.tree['show'] = 'headings'
        for i in range(0, len(self.tree['columns'])):
            if i == 0:
                self.tree.column(self.tree['columns'][i], width=550, stretch=0)
            elif i == 1:
                self.tree.column(self.tree['columns'][i], width=150, stretch=0)
            elif i == 2:
                self.tree.column(self.tree['columns'][i], width=50, stretch=0)
            elif i == 3:
                self.tree.column(self.tree['columns'][i], width=250, stretch=0)
            else:
                self.tree.column(self.tree['columns'][i], width=400, stretch=0)

            self.tree.heading(self.tree['columns'][i], text=self.tree['columns'][i])

        df_rows = df.to_numpy().tolist()
        for i in range(0, len(df_rows)):
            if i % 2 == 0:
                self.tree.insert('', 'end', values=df_rows[i], tags='even')
            else:
                self.tree.insert('', 'end', values=df_rows[i], tags='odd')

    # converts csv to a dataframe
    def csv_to_df(self, filename):
        self.current_file = filename
        df = pd.read_csv(filename)
        self.load_df(df)

    # clears data from tree view
    def clear_data(self):
        self.tree.delete(*self.tree.get_children())

    # builds window
    def __init__(self):

        # creates initial window for gui
        window = Tk()
        center(window,1440,700)
        window.configure(bg="#ffffff")
        window.title("Dublin Rental Property WebScraper")
        canvas = Canvas(
            window,
            bg="#ffffff",
            height=700,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        # places a tree view onto the window
        # displays the data
        # uses tags from entries to colour
        self.tree = ttk.Treeview(canvas)
        self.tree.place(height=480, width=1400, x=20, y=20)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.tag_configure('even', background='#B4E8BF')
        self.tree.tag_configure('odd', background='white')

        canvas.create_rectangle(
            20, 520, 20 + 1400, 520 + 160,
            fill="#c4c4c4",
            outline="")

        canvas.create_rectangle(
            20, 20, 20 + 1400, 20 + 480,
            fill="#c4c4c4",
            outline="")

        entry0 = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        entry0.place(
            x=1040, y=540,
            width=100,
            height=18)

        canvas.create_text(
            995.0, 550.0,
            text="min Price",
            fill="#000000",
            font=("None", int(15.0)))

        entry1 = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        entry1.place(
            x=1040, y=583,
            width=100,
            height=18)

        canvas.create_text(
            995.0, 590.0,
            text="max Price",
            fill="#000000",
            font=("None", int(15.0)))

        entry2 = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        entry2.place(
            x=1280, y=540,
            width=100,
            height=18)

        canvas.create_text(
            1235.0, 550.0,
            text="min Beds",
            fill="#000000",
            font=("None", int(15.0)))

        entry3 = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        entry3.place(
            x=1280, y=583,
            width=100,
            height=18)

        entry0.bind()
        canvas.create_text(
            1235.0, 593.0,
            text="max Beds",
            fill="#000000",
            font=("None", int(15.0)))

        b0 = Button(
            borderwidth=0,
            highlightthickness=0,
            text='START',
            command=lambda: self.start(),
            relief="flat")

        b0.place(
            x=620, y=540,
            width=200,
            height=60)

        # on click loads all properties to tree view
        all_properties_button = Button(
            borderwidth=0,
            highlightthickness=0,
            text='Load all properties',
            command=lambda: self.csv_to_df('resources/all_properties_sorted.csv'),
            relief="flat")

        all_properties_button.place(
            x=150, y=552,
            width=300,
            height=35)

        # on click loads all new properties to tree view
        new_properties_button = Button(
            #image=img2,
            borderwidth=0,
            highlightthickness=0,
            text='Load new properties',
            command=lambda:self.csv_to_df('resources/new_properties.csv'),
            relief="flat")

        new_properties_button.place(
            x=150, y=617,
            width=300,
            height=35)

        # on click filters current data frame in tree view based on parameters in entry boxes
        filter_button = Button(
            borderwidth=0,
            highlightthickness=0,
            text='Filter',
            command=lambda:self.filter(entry0.get(),entry1.get(),entry2.get(),entry3.get()),
            relief="flat")

        filter_button.place(
            x=1280, y=627,
            width=100,
            height=35)

        window.resizable(False, False)
        window.mainloop()


run = GUI()
