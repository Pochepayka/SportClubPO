from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from bd import *

#класс для вывода таблицы
class Table(ttk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, anchor=CENTER)

        for row in rows:
            table.insert('', END, values=tuple(row))

        scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=1, fill=BOTH)


#основной класс визуального интерфейса
class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Добро пожаловать в приложение PythonRu")
        #self.geometry('1375x844+10+10')
        self.minsize(1440,1000)

        self.maxsize(3000,2000)
        self['background'] = "#EBEBEB"
        self.bold_font = 'Helvetica 13 bold'
        self.PutFrames()
        self.bd = 10
        self.bg = 'red'
        self['borderwidt'] = 2
        self['relief'] = "groove"

    #обновление всех фреймов
    def refrash(self,nw):
        self.tableFrame.table1.destroy()
        allFrames = [f for f in self.children]
        for fName in allFrames:
            self.nametowidget(fName).destroy()
        nw.destroy()
        self.PutFrames()

    #прорисовка фреймов
    def PutFrames(self):

        self.outputFrame = OutputForm(self)
        #self.outputFrame.grid(row=0, column=1,columnspan=1, sticky='nswe',pady=20,padx=20)
        self.outputFrame.place(relx=0,rely=0,relwidth=0.5,relheight=0.5)
        self.outputFrame.PutWidgets()
        self.settingFrame = SettingForm(self)
        ##elf.settingFrame.grid(row=0, column=0, columnspan=1,sticky='nswe',pady=20,padx=20)
        self.settingFrame.place(relx=0.5,rely=0,relwidth=0.5,relheight=0.5)
        self.settingFrame.PutWidgets()
        self.tableFrame = TableForm(self)
        #self.tableFrame.grid(row=1,column=0,columnspan=2,sticky='nswe',pady=20,padx=20)
        self.tableFrame.place(relx=0,rely=0.5,relwidth=1,relheight=0.5)
        self.tableFrame.PutWidgets()


#дочений класс левый верхний фрейм
class OutputForm(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #self['background'] = self.master['background']
        self['borderwidth']=self.master['borderwidth']
        self['relief']=self.master['relief']

    #вызов и прорисовка таблицы
    def bufer(self,frame,w1,w2,a1,a2,win1,win2):
        newWindow = Tk()
        newWindow.title("Отфильтрованные кандидаты")
        newWindow.geometry('1440x300')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)
        data=MainFind(w1,w2,a1,a2,win1,win2)
        table1 = Table(frame, headings=("Имя", "Возраст", "Вес","Рост","Тренер","lvl","Побед","Травмы","Реабилитации"),
                       rows=data)
        # table1.grid(row=2, column=1, padx=0, pady=0, columnspan=10, rowspan=10)
        table1.place(relx=0, rely=0.2, relwidth=1)

    #прорисовка фреймов
    def PutWidgets(self):
        self.place()
        colorate=ttk.Frame(self)
        colorate.place(relheight=1,relwidth=1,relx=0,rely=0)
        text=Label(colorate,text="Поиск кандидатов на следующие соревнования:")
        text.grid()

        text1=Label(colorate,text="Вес")
        text1.grid()
        ot1 = Label(colorate, text="от")
        ot1.grid()
        boxOtWeight= Entry(colorate,)

        boxOtWeight.insert(END, '0')
        boxOtWeight.grid()
        do1 = Label(colorate, text="до")
        do1.grid()

        boxDoWeight= Entry(colorate)
        boxDoWeight.insert(END, '100')
        boxDoWeight.grid()
        #ttk.Combobox(colorate,values=["<65","65-70","71-75","76-80","81-85","86-90",">90"])

        text2 = Label(colorate, text="Возраст")
        text2.grid()
        ot2 = Label(colorate, text="от")
        ot2.grid()
        boxOtAge = Entry(colorate)
        boxOtAge.insert(END, '0')
        boxOtAge.grid()
        do2 = Label(colorate, text="до")
        do2.grid()
        boxDoAge = Entry(colorate)
        boxDoAge.insert(END, '100')
        boxDoAge.grid()

        text3 = Label(colorate, text="Побед")
        text3.grid()
        ot3 = Label(colorate, text="от")
        ot3.grid()
        boxOtWin = Entry(colorate)
        boxOtWin.insert(END, '0')
        boxOtWin.grid()
        do3 = Label(colorate, text="до")
        do3.grid()
        boxDoWin = Entry(colorate)
        boxDoWin.insert(END, '100')
        boxDoWin.grid()

        #text4 = Label(colorate, text="Дата")
        #text4.grid()
        #date = DateEntry(colorate)
        #date.grid()

        But = ttk.Button(colorate, text="Найти",
                         command=lambda: self.bufer(colorate,boxOtWeight.get(),boxDoWeight.get(),boxOtAge.get(),boxDoAge.get(),boxOtWin.get(),boxDoWin.get()))#,date.get()))
        But.grid()#row=3, column=3, padx=10, pady=10, columnspan=1)
        pass


#дочерний класс правый верхний фрейм
class SettingForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #self['background'] = self.master['background']
        self['borderwidth']=self.master['borderwidth']
        self['relief']=self.master['relief']
        self.items=[]

    #вызов и прорисовка таблицы
    def bufer(self,name,frame):
        self.items=AllInfoSportsmen(name)
        table1 = Table(frame,headings=("Имя", "Возраст", "Вес"), rows=[[self.items[0][0],self.items[0][1],self.items[0][2]]])
        #table1.grid(row=2, column=1, padx=0, pady=0, columnspan=10, rowspan=10)
        table1.place(relx=0,rely=0.2,relwidth=1)
        table2 = Table(frame, headings=("Рост", "Тренер", "Рейтинг тренера"),rows=[[self.items[0][3],self.items[0][4],self.items[0][5]]])
        #table2.grid(row=3, column=1, padx=0, pady=0, columnspan=10, rowspan=10)
        table2.place(relx=0,rely=0.4,relwidth=1)
        table3 = Table(frame, headings=( "Счетчик побед", "Дата травмы", "Продолжитедльность"),rows=[[self.items[0][6],self.items[0][7],self.items[0][8]]])
        #table3.grid(row=4, column=1, padx=0, pady=0, columnspan=10, rowspan=10)

        table3.place(relx=0,rely=0.6,relwidth=1)

    #добавление спортсмена
    def NewSpotrsman(self):
        newWindow = Tk()
        newWindow.title("Добавление спортсмена")
        newWindow.geometry('750x150+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)
        text = Label(frame, text="Имя")
        text.grid(row=1, column=1, padx=10, pady=10, columnspan=1)
        box = Entry(frame)
        box.grid(row=2, column=1, padx=10, pady=10, columnspan=1)
        text2 = Label(frame, text="Возраст")
        text2.grid(row=1, column=2, padx=10, pady=10, columnspan=1)
        box2 = Entry(frame)
        box2.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
        text3 = Label(frame, text="Вес")
        text3.grid(row=1, column=3, padx=10, pady=10, columnspan=1)
        box3 = Entry(frame)
        box3.grid(row=2, column=3, padx=10, pady=10, columnspan=1)
        text4 = Label(frame, text="Рост")
        text4.grid(row=1, column=4, padx=10, pady=10, columnspan=1)
        box4 = Entry(frame)
        box4.grid(row=2, column=4, padx=10, pady=10, columnspan=1)
        text5 = Label(frame, text="Тренер")
        text5.grid(row=1, column=5, padx=10, pady=10, columnspan=1)

        items=OutCoachsName()

        box5 = ttk.Combobox(frame,values=items)
        #box5 = Entry(frame)
        box5.grid(row=2, column=5, padx=10, pady=10, columnspan=1)
        But = ttk.Button(frame, text="Добавить",
                         command=lambda: InsertSportsmen([(box.get(), box2.get(), box3.get(), box4.get(), box5.get())]))
        But.grid(row=3, column=3, padx=10, pady=10, columnspan=1)
        But.grid(row=3, column=3, padx=10, pady=10, columnspan=1)
        ttk.Button(frame, text="Сохранить", command=lambda: self.master.refrash(newWindow)).grid(row=3, column=4, padx=10, pady=10,
                                                                                      columnspan=1)
        # But.bind('<Button-1>', newWindow.quit())  # Обработчик событий
        # newSpotrsmanBut.pack(expand=YES,anchor="nw")

        pass

    #добавление тренера
    def NewCoach(self):
        newWindow = Tk()
        newWindow.title("Добавление тренера")
        newWindow.geometry('300x150+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)
        text = Label(frame, text="Имя")
        text.grid(row=1, column=1, padx=10, pady=10, columnspan=1)
        box = Entry(frame)
        box.grid(row=2, column=1, padx=10, pady=10, columnspan=1)
        text2 = Label(frame, text="Рейтинг")
        text2.grid(row=1, column=2, padx=10, pady=10, columnspan=1)
        box2 = Entry(frame)
        box2.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
        But = ttk.Button(frame, text="Добавить", command=lambda: InsertCoach([(box.get(), box2.get())]))
        But.grid(row=3, column=1, padx=10, pady=10, columnspan=1)
        ttk.Button(frame, text="Сохранить", command=lambda:
        self.master.refrash(newWindow)) .grid(row=3, column=2, padx=10, pady=10,columnspan=1)
        pass

    #добавление травмы
    def NewTrauma(self):
        newWindow = Tk()
        newWindow.title("Внесение травмы")
        newWindow.geometry('750x150+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)
        text = Label(frame, text="Имя")
        text.grid(row=1, column=1, padx=10, pady=10, columnspan=1)
        box = ttk.Combobox(frame,values=OutName())
        box.grid(row=2, column=1, padx=10, pady=10, columnspan=1)
        text2 = Label(frame, text="Тип")
        text2.grid(row=1, column=2, padx=10, pady=10, columnspan=1)
        box2 = ttk.Combobox(frame, values=["Тяжелая","Средняя","Легкая"])
        box2.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
        text3 = Label(frame, text="Дата получения")
        text3.grid(row=1, column=3, padx=10, pady=10, columnspan=1)
        box3 = DateEntry(frame)
        box3.grid(row=2, column=3, padx=10, pady=10, columnspan=1)
        text4 = Label(frame, text="Реабилитация (в днях)")
        text4.grid(row=1, column=4, padx=10, pady=10, columnspan=1)
        box4 = Entry(frame)
        box4.grid(row=2, column=4, padx=10, pady=10, columnspan=1)
        But = ttk.Button(frame, text="Добавить",
                         command=lambda: InsertTrauma([(box.get(), box3.get(), box2.get(), box4.get())]))
        But.grid(row=3, column=2, padx=10, pady=10, columnspan=1)
        ttk.Button(frame, text="Сохранить", command=lambda: self.master.refrash(newWindow)) .grid(row=3, column=3, padx=10, pady=10,
                                                                                      columnspan=1)
        pass

    #добавление результата сорев
    def NewCompetition(self):
        newWindow = Tk()
        newWindow.title("Внесение соревнования")
        newWindow.geometry('750x150+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)
        text = Label(frame, text="Название")
        text.grid(row=1, column=1, padx=10, pady=10, columnspan=1)
        box = Entry(frame)
        box.grid(row=2, column=1, padx=10, pady=10, columnspan=1)
        text2 = Label(frame, text="Дата")
        text2.grid(row=1, column=2, padx=10, pady=10, columnspan=1)
        box2 = DateEntry(frame)
        box2.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
        text3 = Label(frame, text="Первый спортсмен")
        text3.grid(row=1, column=3, padx=10, pady=10, columnspan=1)
        box3 = ttk.Combobox(frame,values=OutName())
        box3.grid(row=2, column=3, padx=10, pady=10, columnspan=1)
        text4 = Label(frame, text="Второй спортсмен")
        text4.grid(row=1, column=4, padx=10, pady=10, columnspan=1)
        box4 = ttk.Combobox(frame,values=OutName())
        box4.grid(row=2, column=4, padx=10, pady=10, columnspan=1)
        text5 = Label(frame, text="Победитель")
        text5.grid(row=1, column=5, padx=10, pady=10, columnspan=1)
        box5 = ttk.Combobox(frame,values=OutName())
        #box5 = Entry(frame)
        box5.grid(row=2, column=5, padx=10, pady=10, columnspan=1)

        But = ttk.Button(frame, text="Добавить",
                         command=lambda: InsertCompetition([(box.get(), box2.get(), box3.get(), box4.get(), box5.get())]))
        But.grid(row=3, column=3, padx=10, pady=10, columnspan=1)
        ttk.Button(frame, text="Сохранить", command=lambda: self.master.refrash(newWindow)) .grid(row=3, column=4, padx=10, pady=10,
                                                                                      columnspan=1)
        pass

    #изменение тренера
    def ChangeCoach(self):
        newWindow = Tk()
        newWindow.title("Замена тренера ")
        newWindow.geometry('600x150+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)
        text = Label(frame, text="Имя")
        text.grid(row=1, column=1, padx=10, pady=10, columnspan=1)
        box = ttk.Combobox(frame, values=OutName())
        box.grid(row=2, column=1, padx=10, pady=10, columnspan=1)
        text5 = Label(frame, text="Новый тренер")
        text5.grid(row=1, column=2, padx=10, pady=10, columnspan=1)
        items = OutCoachsName()
        box5 = ttk.Combobox(frame, values=items)
        # box5 = Entry(frame)
        box5.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
        But = ttk.Button(frame, text="Добавить",
                         command=lambda: ChangeSportsmenInfo(box.get(), box5.get()))
        But.grid(row=3, column=3, padx=10, pady=10, columnspan=1)
        ttk.Button(frame, text="Сохранить", command=lambda: self.master.refrash(newWindow)) .grid(row=3, column=4, padx=10, pady=10,
                                                                                      columnspan=1)
        # But.bind('<Button-1>', newWindow.quit())  # Обработчик событий
        # newSpotrsmanBut.pack(expand=YES,anchor="nw")
        pass
        """{{{table.grid(row=2, column=1, padx=0, pady=0, columnspan=20, rowspan=3)
        table = Table(frame, ["name", "age", "weigth", "height", "coach", "lvlCoach", "win", "traumaBeg", "traumaLong"],
                      self.items)
            table.grid(row=2, column=1, padx=0, pady=0, columnspan=20, rowspan=3)}}}"""

    #добавление спортсмена
    def Info(self):
        newWindow = Tk()
        newWindow.title("Информация спортсмена")
        newWindow.geometry('800x300+100+30')
        frame = ttk.Frame(newWindow)

        frame.pack(expand=YES, fill=BOTH)
        text = Label(frame, text="Имя")
        #text.grid(row=1, column=1, padx=10, pady=10, columnspan=1)
        text.place(relx=0,rely=0,relwidth=0.2)
        box = ttk.Combobox(frame, values=OutName())
        #box.grid(row=1, column=2, padx=10, pady=10, columnspan=2)

        box.place(relx=0.2,rely=0,relwidth=0.2)
        But = ttk.Button(frame, text="Добавить",
                         command=lambda:self.bufer(box.get(),frame))
        #But.grid(row=1, column=4, padx=10, pady=10, columnspan=1)

        But.place(relx=0.4,rely=0,relwidth=0.2)
        but2=ttk.Button(frame, text="Сохранить", command=lambda: self.master.refrash(newWindow)) #.grid(row=1, column=5, padx=10, pady=10, columnspan=1)
        but2.place(relx=0.6,rely=0,relwidth=0.2)
        pass

    #вывод топа спортсмена
    def TopSpotrsmens(self):

        newWindow = Tk()
        newWindow.title("5 лучших спортсменов")
        newWindow.geometry('1200x300+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)

        table1 = Table(frame, headings=("Имя", "Возраст", "Вес","Рост","Тренер","Побед"),rows=TheBestSportsmen())
        table1.grid()
        #but2=ttk.Button(frame, text="Закрыть", command=lambda: newWindow.destroy())#.grid(row=1, column=5, padx=10, pady=10, columnspan=1)
        #but2.place(relx=0.6,rely=0,relwidth=0.2)
        pass

    #вывод топа тренеров
    def TopCoach(self):
        newWindow = Tk()
        newWindow.title("5 лучших тренеров")
        newWindow.geometry('800x300+100+30')
        frame = ttk.Frame(newWindow)
        frame.pack(expand=YES, fill=BOTH)

        table1 = Table(frame, headings=("Имя", "Рейтинг", "Побед воспитанников"), rows=TheBestCoach())
        table1.grid()

        pass

    #прорисовка фреймов
    def PutWidgets(self):
        newSpotrsmanBut = ttk.Button(self, text="Внести нового спортсмена", command=self.NewSpotrsman)
        newSpotrsmanBut.grid(row=1, column=1, padx=10, pady=5, columnspan=1)
        # newSpotrsmanBut.pack(expand=YES,anchor="nw")
        newCoachBut = ttk.Button(self, text="Внести нового тренера", command=self.NewCoach)
        newCoachBut.grid(row=2, column=1, padx=10, pady=5, columnspan=1)
        newTraumaBut = ttk.Button(self, text="Внести информацию о травме", command=self.NewTrauma)
        newTraumaBut.grid(row=4, column=1, padx=10, pady=5, columnspan=1)
        newCompetitionBut = ttk.Button(self, text="Внести результат соревнования", command=self.NewCompetition)
        newCompetitionBut.grid(row=3, column=1, padx=10, pady=10, columnspan=1)

        changeCoachBut = ttk.Button(self, text="Заменить тренера", command=self.ChangeCoach)
        changeCoachBut.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
        infoBut = ttk.Button(self, text="О спортсмене", command=self.Info)
        infoBut.grid(row=1, column=2, padx=10, pady=10, columnspan=1)
        topSportsmensBut = ttk.Button(self, text="Топ спортсменов", command=self.TopSpotrsmens)
        topSportsmensBut.grid(row=1, column=3, padx=10, pady=10, columnspan=1)
        topCoachsBut = ttk.Button(self, text="Топ тренеров", command=self.TopCoach)
        topCoachsBut.grid(row=2, column=3, padx=10, pady=10, columnspan=1)
        #self.pack()#expand=1, fill='both')
        self.place()
        pass



#дочерний класс с таблицами
class TableForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #self['background'] = self.master['background']
        self['borderwidth']=self.master['borderwidth']
        self['relief']=self.master['relief']

    #прорисовка фреймов
    def PutWidgets(self):
        self.tab_control = ttk.Notebook(self)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Sportsmens')
        self.tab_control.add(self.tab2, text='Coachs')
        self.tab_control.add(self.tab3, text='Traumas')
        self.tab_control.add(self.tab4, text='Competitions')

        self.tab_control.pack(anchor=N, fill=X)

        self.table1 = Table(self.tab1, headings=('Имя', 'Возраст', 'Вес', 'Рост', 'Тренер'), rows=dataInputSportsmens)
        self.table2 = Table(self.tab2, headings=('Имя', 'Рейтинг'), rows=dataInputCoachs)
        self.table3 = Table(self.tab3, headings=('Описание', 'Дата получения', 'Тип травмы', 'Реабилитация'),
                       rows=dataInputTraums)
        self.table4 = Table(self.tab4, headings=('Название', 'Дата', '1й участник', '2й участник', 'Победитель'),
                       rows=dataInputCompetitions)
        self.table1.pack(expand=YES, anchor="nw", fill=BOTH)
        self.table2.pack(expand=YES, anchor="nw", fill=BOTH)
        self.table3.pack(expand=YES, anchor="nw", fill=BOTH)
        self.table4.pack(expand=YES, anchor="nw", fill=BOTH)

        self.place()
        pass




{"""window = Tk()

window.title("Добро пожаловать в приложение PythonRu")

window.geometry('1375x844+10+10')

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Sportsmens')
tab_control.add(tab2, text='Coachs')
tab_control.add(tab3, text='Traumas')
tab_control.add(tab4, text='Competitions')

tab_control.pack(anchor=N, fill=X)

table1 = Table(tab1, headings=('Имя','Возраст','Вес','Рост','Тренер'), rows=dataInputSportsmens)
table2 = Table(tab2, headings=('Имя','Рейтинг'), rows=dataInputCoachs)
table3 = Table(tab3, headings=('Описание','Дата получения','Тип травмы','Реабилитация'), rows=dataInputTraums)
table4 = Table(tab4, headings=('Название','Дата','1й участник','2й участник','Победитель'), rows=dataInputCompetitions)
table1.pack(expand=YES,anchor="nw",fill=X)
table2.pack(expand=YES,anchor="nw", fill=X)
table3.pack(expand=YES,anchor="nw", fill=X)
table4.pack(expand=YES,anchor="nw", fill=X)


setting =  ttk.Frame(window)#Window(window)

for c in range(10): setting.columnconfigure(index=c, weight=1)
for r in range(10): setting.rowconfigure(index=r, weight=1)

newSpotrsmanBut=ttk.Button(setting,text="Внести нового спортсмена",command=NewSpotrsman)
newSpotrsmanBut.grid(row=1,column=1,padx=10,pady=10,columnspan=1)
#newSpotrsmanBut.pack(expand=YES,anchor="nw")
newCoachBut=ttk.Button(setting,text="Внести нового тренера",command=NewCoach)
newCoachBut.grid(row=2,column=1,padx=10,pady=10,columnspan=1)
newTraumaBut=ttk.Button(setting,text="Внести информацию о травме",command=NewTrauma)
newTraumaBut.grid(row=4,column=1,padx=10,pady=10,columnspan=1)
newCompetitionBut=ttk.Button(setting,text="Внести результат соревнования",command=NewCompetition)
newCompetitionBut.grid(row=3,column=1,padx=10,pady=10,columnspan=1)

changeCoachBut=ttk.Button(setting,text="Заменить тренера",command=ChangeCoach)
changeCoachBut.grid(row=2,column=3,padx=10,pady=10,columnspan=1)
infoBut=ttk.Button(setting,text="О спортсмене",command=Info)
infoBut.grid(row=1,column=3,padx=10,pady=10,columnspan=1)
topSportsmensBut=ttk.Button(setting,text="Топ спортсменов",command=TopSpotrsmens)
topSportsmensBut.grid(row=1,column=5,padx=10,pady=10,columnspan=1)
topCoachsBut=ttk.Button(setting,text="Топ тренеров",command=TopCoach)
topCoachsBut.grid(row=2,column=5,padx=10,pady=10,columnspan=1)
setting.pack(expand=1, fill='both')


window.mainloop()"""}