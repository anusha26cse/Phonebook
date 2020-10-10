import tkinter as tk
import re
import pymysql
db=pymysql.connect("localhost","root","password","demo")
print(db)
cursor=db.cursor()

def about():
    l1.delete(0,l1.size())
    l1.insert(0,"This app is an address book and it maintains contacts and email addresses.")

def insert():
    l1.delete(0,l1.size())
    s=e4.get()
    s1=(e3.get())
    y=re.search("^\d{10}$",s1)
    x=re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",s)
    if x is None or y is None:
        l1.insert(0,"Invalid Email or phone number")
    else:
        sql="insert into contact values('%s','%s',%d,'%s')" %(e1.get(),e2.get(),int(e3.get()),e4.get())
        cursor.execute(sql)
        db.commit()
        l1.insert(0,"inserted:")
        l1.insert(1,e1.get())
   
        

def update():
    l1.delete(0,l1.size())
    global db,cursor
    s=e4.get()
    s1=(e3.get())
    y=re.search("^\d{10}$",s1)
    x=re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",s)
    if x and y:       
        sql="update contact set phno=%d,email='%s' where fname='%s' and lname='%s'" %(int(e3.get()),e4.get(),e1.get(),e2.get())
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        l1.insert(0,"Updated:")
        l1.insert(1,e1.get())
        
    else:
        l1.insert(0,"Invalid Email or phone number")
    
        
def delete():
    l1.delete(0,l1.size())
    global db,cursor
    sql="delete from contact where fname='%s'"%(e1.get())
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    l1.insert(0,"Deleted:",e1.get())
    

def clear():
    e1.delete(0,len(e1.get()))
    e2.delete(0,len(e2.get()))
    e3.delete(0,len(e3.get()))
    e4.delete(0,len(e4.get()))
    e5.delete(0,len(e5.get()))
    l1.delete(0,l1.size())
   
def List():
    global db,cursor,l1
    l1.delete(0,l1.size())
    j=0

    sql="select * from contact"
    cursor.execute(sql)
    for i in cursor.fetchall():
        l1.insert(j,i[0])
        j+=1
        l1.insert(j,i[1])
        j+=1
        l1.insert(j,i[2])
        j+=1
        l1.insert(j,i[3])
        j+=1
        l1.insert(j,"--------------------")
        j+=1

def search():
    l1.delete(0,l1.size())
    j=0
    global db,cursor,e5
    exp="%"+"%s"%(e5.get())+"%"
    sql="select * from contact where fname like " + "'" + exp + "'"
    cursor.execute(sql)
    for i in cursor.fetchall():
        l1.insert(j,i[0])
        j+=1
        l1.insert(j,i[1])
        j+=1
        l1.insert(j,i[2])
        j+=1
        l1.insert(j,i[3])
        j+=1
        l1.insert(j,"--------------------")
        j+=1

master =tk.Tk()
master.title('Address book')
tk.Label(master,text="ADDRESS BOOK", font='Helvetica 18 bold',fg="green").grid(row=0,column=1)
menu = tk.Menu(master)
master.config(menu=menu) 
filemenu = tk.Menu(menu) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_command(label='About',command=about) 
filemenu.add_separator() 
filemenu.add_command(label='Exit', command=master.destroy) 


e5=tk.Entry(master)
e5.grid(row=1,column=1)
tk.Button(master,text="Search",command=search,width=10, font='Helvetica 12').grid(row=1,column=3)
tk.Label(master,text="First name", font='Helvetica 12').grid(row=2)
tk.Label(master,text="Last name", font='Helvetica 12').grid(row=3)
tk.Label(master,text="Phone no", font='Helvetica 12').grid(row=4)
tk.Label(master,text="E-mail", font='Helvetica 12').grid(row=5)
e1=tk.Entry(master)
e1.grid(row=2,column=1)
e2=tk.Entry(master)
e2.grid(row=3,column=1)
e3=tk.Entry(master)
e3.grid(row=4,column=1)
e4=tk.Entry(master)
e4.grid(row=5,column=1)
l1=tk.Listbox(master,width=35,height=10)
l1.grid(row=9,column=1)
tk.Button(master,text="Insert",command=insert,width=10, font='Helvetica 12').grid(row=2,column=3)
tk.Button(master,text="Update",command=update,width=10, font='Helvetica 12').grid(row=3,column=3)
tk.Button(master,text="Delete",command=delete,width=10, font='Helvetica 12').grid(row=4,column=3)
tk.Button(master,text="Clear",command=clear,width=10, font='Helvetica 12').grid(row=5,column=3)
tk.Button(master,text="List",command=List,width=10, font='Helvetica 12').grid(row=9,column=3)
tk.Label(master,text="Results", font='Helvetica 12').grid(row=9,column=0)
tk.Label(master,text="").grid(row=10)
tk.mainloop()
