import tkinter
import util as ut
from tkinter import *
from tkinter import ttk
import sys
import search


class ProcessId(Frame):
    """docstring for getProcess"""
    def __init__(self, master):
        super().__init__(master)
        self.lable = Label(self, width=20, relief=RIDGE, text="选择进程:", padx = 5)
        self.lable.pack(side = LEFT)

        self.var = tkinter.StringVar()
        self.comboxlist = ttk.Combobox(self, textvariable=self.var, width=30)
        self.comboxlist["value"] = ut.getPidList()
        self.comboxlist.current(0)
        self.comboxlist.bind("<<ComboboxSelected>>", self.getSelectedPid)
        self.comboxlist.pack()
        self.config(padx=10)

        self.pid = self.getSelectedPid()

    def getSelectedPid(self, *args):
        pid = self.comboxlist.get()
        sum = 0
        for i in range(1, len(pid)):
            if pid[i] in "1234567890":
                sum *= 10
                sum += int(pid[i])
            else:
                break
        self.pid = sum
        return self.pid
        

class LE(Frame):

    def __init__(self, master, txt):
        super().__init__(master)
        self.label = Label(self, width = 15, relief=RIDGE, text=txt+':')
        self.label.pack(side = LEFT,  padx = 10)
        self.var = StringVar()
        self.entry = Entry(self, textvariable=self.var)
        self.entry.pack(side = LEFT)

        self.config(padx= 10, pady =10)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)

    def changeState(self, enable):
        if enable:
            self.entry.config(state = NORMAL)
        else:
            self.entry.config(state = DISABLED)

class InputMemory(Frame):
    """docstring for LEFT"""
    def __init__(self, master, mas):
        super().__init__(master)
        self.v = IntVar()
        self.rd1 = Radiobutton(self, text="直接输入地址",width = 14, variable=self.v, value=1, command=self.update)
        self.rd1.pack(side=LEFT, padx=3)
        self.rd1.select()
        self.rd2 = Radiobutton(self,text="自动查找地址", variable=self.v, value=2, command=self.update)
        self.rd2.pack(side=LEFT)
        self.mas = mas

    def update(self):
        self.mas.changeState(self.v.get())

    def get(self):
        return self.v.get()


class  GUI(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.pi = ProcessId(self)
        self.pi.config(pady=5)
        self.pi.pack(fill=X)

        #*********************内存

        self.f0 = Frame(self)
        self.f = Frame(self.f0)
        self.v = StringVar()
        self.showAddr = Listbox(self.f, selectmode = BROWSE, listvariable=self.v)
        #self.showAddr.bind('<Button-1>', self.updateAddrValue)
        self.s = Scrollbar(self.f)
        self.s.pack(side=RIGHT, fill = Y)
        self.showAddr.pack(side=LEFT)
        self.s.config(command = self.showAddr.yview)
        self.showAddr.config(yscrollcommand=self.s.set)
        self.f.pack(side=LEFT, padx=6)


        self.f2 = Frame(self.f0)
        self.im = InputMemory(self.f2, self)
        self.im.pack(fill=X)
        self.tagAddr = LE(self.f2, "目标地址")
        self.tagAddr.pack(fill=X)

        self.tagValue = LE(self.f2, "目标值")
        self.tagValue.pack(fill=X)
        self.tagValue.changeState(False)
        self.escValue = LE(self.f2, "期望值")
        self.escValue.entry.config(width=13)
        self.modify = Button(self.escValue,width=20, text="修改", command=self.change)
        self.modify.pack(side=LEFT, padx=3)
        self.escValue.pack(fill=X)
        self.f2.pack(side=RIGHT)
        self.f0.pack(pady=5)

        self.group = LabelFrame(self, text="操作", padx=5, pady=5)
        self.group.pack(padx=5, pady=10, ipady=5)
        self.firSearch = Button(self.group, width = 16, height=2, text = "首次查找", command = self.search)
        self.firSearch.pack(side=LEFT, padx = 10)
        self.secSearch = Button(self.group,width = 16, height=2, text = "累计查找", command = self.reSearch)
        self.secSearch.pack(side=LEFT, padx = 10)
        self.ext = Button(self.group,width = 16, height=2, text = "退出", command = self.closeWindow)
        self.ext.pack(side=LEFT, padx = 10)


    def closeWindow(self):
        sys.exit()

    def changeState(self, v):
        if v == 1:#直接输入地址
            self.tagAddr.changeState(True)
            self.tagValue.changeState(False)
        else:
            self.tagAddr.changeState(False)
            self.tagValue.changeState(True)

    def search(self):
        self.showAddr.delete(0, END)
        se.getPh(self.pi.pid)
        val = self.tagValue.get()
        if val == '':
            return
        li = se.firstSearch(val)
        #li = [x for x in range(10,30)]
        for i in li:
            self.showAddr.insert(END, i)

    def reSearch(self):
        self.showAddr.delete(0, END)
        val = self.tagValue.get()
        if val == '':
            return
        li2 = se.reSearch(val)
        for i in li2:
            self.showAddr.insert(END, li2)

    def change(self):
        if self.im.get() == 1:
            se.getPh(self.pi.pid)
            se.change(self.escValue.get(), 1, self.tagAddr.get())
        else:
            se.change(self.escValue.get(), 2)

root = Tk()
root.title("一组项目-----内存修改器")
root.geometry("410x280+200+200")
se = search.Search()
gui = GUI(root)
gui.pack()
root.mainloop()