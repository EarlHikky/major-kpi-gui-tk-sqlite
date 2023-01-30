import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime


class Main(tk.Frame):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('sales.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS sales (id integer primary key, fio text, extradition integer,
                            ti real, trener real, client real, total real, time text)''')
        self.conn.commit()
        self.init_main()

    def view_records(self, n, p):
        self.c.execute('''UPDATE sales SET total = extradition +  ti +  trener + client ''')
        self.conn.commit()
        if p == 'all':
            self.c.execute('''SELECT id, fio, extradition, ti, trener, client, total, time 
                                FROM sales  
                                ORDER BY id DESC''')
            [n.delete(i) for i in n.get_children()]
            [n.insert('', 'end', values=row) for row in self.c.fetchall()]   
        elif p == 'month':
            self.c.execute('''SELECT fio, SUM(extradition), SUM(ti), SUM(trener), SUM(client), SUM(total)
                             FROM sales
                             WHERE time >= datetime('now','-1 months')
                             GROUP BY fio
                             ORDER BY SUM(total) DESC''')
            [n.delete(i) for i in n.get_children()]
            [n.insert('', 'end', values=row) for row in self.c.fetchall()]
        elif p == 'kvart':
            self.c.execute('''SELECT fio, SUM(extradition), SUM(ti), SUM(trener), SUM(client), SUM(total)
                             FROM sales
                             WHERE time >= datetime('now','-4 months')
                             GROUP BY fio
                             ORDER BY SUM(total) DESC''')
            [n.delete(i) for i in n.get_children()]
            [n.insert('', 'end', values=row) for row in self.c.fetchall()]
        else:
            self.c.execute('''SELECT fio, SUM(extradition), SUM(ti), SUM(trener), SUM(client), SUM(total)
                             FROM sales
                             WHERE time >= datetime('now','-1 year')
                             GROUP BY fio
                             ORDER BY SUM(total) DESC''')
            [n.delete(i) for i in n.get_children()]
            [n.insert('', 'end', values=row) for row in self.c.fetchall()]

    def init_main(self):
        notebook = ttk.Notebook()
        notebook.grid()

        fstyle = {'bd': 2, 'relief': 'solid'}
        dataframe = tk.Frame(bg='#1082D2', **fstyle)
        frame2 = tk.Frame(notebook, **fstyle)
        frame3 = tk.Frame(notebook, **fstyle)
        frame4 = tk.Frame(notebook, **fstyle)

        dataframe.grid()
        frame2.grid()
        frame3.grid()
        frame4.grid()

        notebook.add(dataframe, text="Данные", sticky='we')
        notebook.add(frame2, text="Месяц", sticky='we')
        notebook.add(frame3, text="Квартал", sticky='we')
        notebook.add(frame4, text="Год", sticky='we')

        bstyle = {"bg": '#d7d8e0', "bd": 3, "width": 15, "relief": 'raised'}
        bposition = {"column": 0, "ipadx": 6, "ipady": 6, "padx": 4, "pady": 4, "sticky": 'sn'}

        btn_add = tk.Button(dataframe, command=self.open_add, text='Добавить', **bstyle)
        btn_add.grid(row=0, **bposition)

        btn_edit = tk.Button(dataframe, command=self.open_edit, text='Редактировать', **bstyle)
        btn_edit.grid(row=1, **bposition)

        btn_del = tk.Button(dataframe, command=self.delete_data, text='Удалить', **bstyle)
        btn_del.grid(row=2, **bposition)

        btn_search = tk.Button(dataframe, command=self.open_search, text='Поиск', **bstyle)
        btn_search.grid(row=3, **bposition)

        btn_staff = tk.Button(dataframe, command=lambda: Staff(), text='Сотрудники', **bstyle)
        btn_staff.grid(row=4, **bposition)

        ar = {'columns': ('fio', 'extradition', 'ti', 'trener', 'client', 'total'), 'height': 15, 'show': 'headings'}

        self.tree = ttk.Treeview(dataframe, columns=('ID', 'fio', 'extradition', 'ti', 'trener', 'client', 'total', 'time'),
                                 height=15, show='headings')
        self.tree2 = ttk.Treeview(frame2, **ar)
        self.tree3 = ttk.Treeview(frame3, **ar)
        self.tree4 = ttk.Treeview(frame4, **ar)

        names = {'fio': 'ФИО', 'extradition': 'Выдачи', 'ti': 'ТИ', 'trener': 'Доп. тренер', 'client': 'Недов. клиент',
                 'total': 'Итого'}
        pos = {'width': 88, 'anchor': 'center'}

        self.tree.column('ID', width=24, anchor='center')
        for name in names.keys():
            self.tree.column(name, **pos)
        self.tree.column('time', width=80, anchor='center')

        self.tree.heading('ID', text='id')
        for name, t in names.items():
            self.tree.heading(name, text=t)
        self.tree.heading('time', text='Дата')

        pos2 = {'width': 118, 'anchor': 'center'}
        self.tree2.column('fio', width=183, anchor='center')
        for name in list(names.keys())[1:]:
            self.tree2.column(name, **pos2)
        for name, t in names.items():
            self.tree2.heading(name, text=t)

        self.tree3.column('fio', width=183, anchor=tk.CENTER)
        for name in list(names.keys())[1:]:
            self.tree3.column(name, **pos2)
        for name, t in names.items():
            self.tree3.heading(name, text=t)

        self.tree4.column('fio', width=183, anchor=tk.CENTER)
        for name in list(names.keys())[1:]:
            self.tree4.column(name, **pos2)
        for name, t in names.items():
            self.tree4.heading(name, text=t)

        self.tree.grid(row=0, column=2, rowspan=5, sticky='we')
        self.tree2.grid()
        self.tree3.grid()
        self.tree4.grid()

        self.view_records(self.tree, 'all')
        self.view_records(self.tree2, 'month')
        self.view_records(self.tree3, 'kvart')
        self.view_records(self.tree4, 'year')

    @staticmethod
    def open_add():
        Add()

    @staticmethod
    def open_edit():
        Edit()

    @staticmethod
    def open_search():
        Search()

    def delete_data(self):
        try:
            for selection_item in self.tree.selection():
                self.c.execute('''DELETE FROM sales WHERE id=?''', (self.tree.set(selection_item, '#1'),))
            self.conn.commit()
            self.view_records(self.tree, 'all')
            self.view_records(self.tree2, 'month')
            self.view_records(self.tree3, 'kvart')
            self.view_records(self.tree4, 'year')

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


class Add(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.data = app
        self.init_add()

    def init_add(self):
        self.title('Добавить продажу')
        self.resizable(False, False)
        self.iconphoto(False, photo)

        toolbar3 = tk.Frame(self, bg='#1082D2', bd=2)
        toolbar3.grid(sticky='we')

        pos = {'ipadx': 6, 'ipady': 3, 'padx': 4, 'pady': 3}
        label = ttk.Label(toolbar3, text="Выдачи", width=20)
        label.grid(row=0, column=0, **pos)
        self.entry_extradition = ttk.Entry(toolbar3, width=30)
        self.entry_extradition.grid(row=0, column=1, **pos)

        label2 = ttk.Label(toolbar3, text="ТИ", width=20)
        label2.grid(row=1, column=0, ipadx=6, ipady=3, padx=4, pady=3)
        self.entry_ti = ttk.Entry(toolbar3, width=30)
        self.entry_ti.grid(row=1, column=1, ipadx=6, ipady=3, padx=4, pady=3)

        label3 = ttk.Label(toolbar3, text="Доп. трен", width=20)
        label3.grid(row=2, column=0, ipadx=6, ipady=3, padx=4, pady=3)
        self.entry_trener = ttk.Entry(toolbar3, width=30)
        self.entry_trener.grid(row=2, column=1, ipadx=6, ipady=3, padx=4, pady=3)

        label4 = ttk.Label(toolbar3, text="Недов. клиент", width=20)
        label4.grid(row=3, column=0, ipadx=6, ipady=3, padx=4, pady=3)
        self.entry_client = ttk.Entry(toolbar3, width=30)
        self.entry_client.grid(row=3, column=1, ipadx=6, ipady=3, padx=4, pady=3)

        persons = []
        with open('staff.txt', 'r', encoding='utf-8') as f:
            for name in f.readlines():
                persons.append(name.strip('\n'))

        self.combobox = ttk.Combobox(toolbar3, values=persons, state="readonly")
        self.combobox.current(0)
        self.combobox.grid(row=4, column=0, rowspan=2, columnspan=2, ipadx=6, ipady=3, padx=4, pady=3)

        self.btn_ok = ttk.Button(toolbar3, command=lambda: self.destroy(), text='Добавить')
        self.btn_ok.grid(row=6, column=0, columnspan=2, ipadx=6, ipady=3, padx=4, pady=3, sticky='ew')
        self.btn_ok.bind('<Button-1>', lambda event: self.insert_data(self.combobox.get(), self.entry_extradition.get(),
                                                self.entry_ti.get(), self.entry_trener.get(), self.entry_client.get()))

        self.grab_set()
        self.focus_set()

    def insert_data(self, fio, extradition, ti, trener, client):
        self.data.c.execute('''INSERT INTO sales ('fio', 'extradition', 'ti', 'trener', 'client', 'time') 
                            VALUES (?, ?, ?, ?, ?, ?)''', (fio, extradition, ti, trener, client, datetime.date.today()))
        self.data.conn.commit()
        self.data.view_records(self.data.tree, 'all')
        self.data.view_records(self.data.tree2, 'month')
        self.data.view_records(self.data.tree3, 'kvart')
        self.data.view_records(self.data.tree4, 'year')


class Edit(Add):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.data = app
        self.default_data()

    def init_edit(self):
        self.title('Редактор')

        self.btn_ok.destroy()
        self.combobox.destroy()

        toolbar4 = tk.Frame(self, bg='#1082D2', bd=2)
        toolbar4.grid(sticky='we')

        label5 = ttk.Label(toolbar4, text="Итого", width=20)
        label5.grid(row=4, column=0, ipadx=6, ipady=3, padx=4, pady=3)
        self.entry_total = ttk.Entry(toolbar4, width=30)
        self.entry_total.grid(row=4, column=1, ipadx=6, ipady=3, padx=4, pady=3)

        btn_edit = ttk.Button(toolbar4, text='Редактировать')
        btn_edit.grid(row=5, column=0, columnspan=2, ipadx=6, ipady=3, padx=4, pady=3, sticky='ew')
        btn_edit.bind('<Button-1>', lambda event: self.edit_data(self.entry_extradition.get(), self.entry_ti.get(),
                                        self.entry_trener.get(), self.entry_client.get(), self.entry_total.get()))

    def edit_data(self, extradition, ti, trener, client, total):
        self.data.c.execute('''UPDATE sales SET extradition=?, ti=?, trener=?, client=?, total=? WHERE ID=?''',
                            (extradition, ti, trener, client, total, self.data.tree.set(self.data.tree.selection()[0],
                                                                                        '#1'),))

        self.data.conn.commit()
        self.data.view_records(self.data.tree, 'all')
        self.data.view_records(self.data.tree2, 'month')
        self.data.view_records(self.data.tree3, 'kvart')
        self.data.view_records(self.data.tree4, 'year')
        self.destroy()

    def default_data(self):
        self.data.c.execute('''SELECT * FROM sales WHERE id=?''',
                            (self.data.tree.set(self.data.tree.selection()[0], '#1'),))
        row = self.data.c.fetchone()
        self.entry_extradition.insert(0, row[2])
        self.entry_ti.insert(1, row[3])
        self.entry_trener.insert(2, row[4])
        self.entry_client.insert(3, row[5])
        self.entry_total.insert(4, row[6])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(bg='#1082D2')
        self.init_search()
        self.data = app

    def init_search(self):
        self.title('Поиск')
        self.resizable(False, False)
        self.iconphoto(False, photo)

        toolbar = tk.Frame(self, bg='#1082D2', bd=2)
        toolbar.grid(sticky='we')

        persons = []
        with open('staff.txt', 'r', encoding='utf-8') as f:
            for name in f.readlines():
                persons.append(name.strip('\n'))

        combobox = ttk.Combobox(toolbar, values=persons, state="readonly")
        combobox.current(0)
        combobox.grid(row=0, column=0,  columnspan=2, ipadx=6, ipady=3, padx=4, pady=3)

        btn_cancel = ttk.Button(toolbar, text='Закрыть', command=self.destroy)
        btn_cancel.grid(row=1, column=0, ipadx=6, ipady=3, padx=4, pady=3, sticky='ew')

        btn_search = ttk.Button(toolbar, text='Поиск')
        btn_search.grid(row=1, column=1, ipadx=6, ipady=3, padx=4, pady=3, sticky='ew')
        btn_search.bind('<Button-1>', lambda event: self.search_records(combobox.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

    def search_records(self, fio):
        fio = ('%' + fio + '%',)
        self.data.c.execute('''SELECT * FROM sales WHERE fio LIKE ?''', fio)
        [self.data.tree.delete(i) for i in self.data.tree.get_children()]
        [self.data.tree.insert('', 'end', values=row) for row in self.data.c.fetchall()]


class Staff(tk.Toplevel):
    def __init__(self):
        super().__init__(bg='#1082D2')
        self.init_staff()

    def init_staff(self):
        self.title('Сотрудники')
        self.resizable(False, False)
        self.iconphoto(False, photo)

        toolbar = tk.Frame(self, bg='#1082D2', bd=2)
        toolbar.grid(sticky='we')

        persons = []
        with open('staff.txt', 'r+', encoding='utf-8') as f:
            for name in f.readlines():
                persons.append(name.strip('\n'))

        combobox = ttk.Combobox(toolbar, values=persons)
        combobox.current(0)
        combobox.grid(row=0, column=0,  columnspan=2, ipadx=6, ipady=3, padx=4, pady=3)

        btn_add = ttk.Button(toolbar, text='Добавить', command=lambda: self.add_staff(combobox.get()))
        btn_add.grid(row=1, column=0, ipadx=6, ipady=3, padx=4, pady=3, sticky='ew')

        btn_del = ttk.Button(toolbar, text='Удалить', command=lambda: self.del_staff(combobox.get()))
        btn_del.grid(row=1, column=1, ipadx=6, ipady=3, padx=4, pady=3, sticky='ew')

    def add_staff(self, name):
        with open('staff.txt', 'r+', encoding='utf-8') as f:
            if name not in f.read().split():
                f.write(name + '\n')
        self.destroy()

    def del_staff(self, name):
        with open('staff.txt', 'r', encoding='utf-8') as f:
            data = f.read().split()

        if name in data:
            data.remove(name)
            with open('staff.txt', 'w', encoding='utf-8') as f:
                for name in data:
                    f.write(name + '\n')

        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    ttk.Style().configure("TLabel", font="helvetica 9", background="#1082D2")
    root.title("Major Auto")
    root.resizable(False, False)
    photo = tk.PhotoImage(file='1.png')
    root.iconphoto(False, photo)
    app = Main()
    # app.grid()
    root.mainloop()
