from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import csv

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by จ๊ะ')
GUI.geometry('750x800+500+50')


################Menu#################

menubar=Menu(GUI)
GUI.config(menu=menubar)

#### File Menu
filemenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='import CSV')
filemenu.add_command(label='Export to Googlesheet')
#### Help Menu
def About():
  messagebox.showinfo('About','สวัสดีค่ะนี่คือโปรแกรมบันทึกข้อมูล\n สนใจบริจารด้วยหัวใจไหมคะ')

helpmenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
#### Donate Menu
donatemenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
#######################################


Tab = ttk.Notebook(GUI)
Tab1 = ttk.Frame(Tab)
Tab2 = ttk.Frame(Tab)
Tab.pack(fill='both', expand=1)

#Tab1.pack(fill='both', expand=1)
#Tab2.pack(fill='both', expand=1)

expenseicon = PhotoImage(file='expensepig.png').subsample(10)
listicon = PhotoImage(file='expensepig1.png').subsample(10)

Tab.add(Tab1, text='Add Expense',image=expenseicon,compound='top')
Tab.add(Tab2, text='Expense List',image=listicon,compound='top')

F1=Frame(Tab1)
F1.place(x=250,y=50)
F2=Frame(Tab2)
F2.pack()
#background
bgimage1=PhotoImage(file='bg.png').subsample(2)
bgimage=ttk.Label(F1,image=bgimage1)
bgimage.pack()



days={'Mon':'จันทร์',
      'Tue':'อังคาร',
      'Wed':'พุธ',
      'Thu':'พฤหัสบดี',
      'Fri':'ศุกร์',
      'Sat':'เสาร์',
      'Sun':'อาทิตย์'}

def Save(event=None):
    
    expense=v_expense.get()
    price=v_price.get()
    qty=v_qty.get()


    #if expense=='' or price=='' or qty=='':
        #print('No Data')
        #messagebox.showwarning('Error','กรุณากรอกข้อมูลให้ครบทุกช่อง')
        #return
    if expense == '':
        messagebox.showwarning('Error','กรุณากรอกข้อมูลรายการสินค้า')
        return

    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกข้อมูลราคา')
        return

    elif qty == '':
        messagebox.showwarning('Error','กรุณากรอกจำนวน')
        return

    try:
      pricetotal=int(price)*int(qty)

      now = datetime.now()
      today=now.strftime('%a') #days['Mon'] ='จันทร์'
      dt = now.strftime('%Y-%m-%d-%H:%M:%S') 
      dt = days[today]+'-'+dt

      print( 'รายการ: {} ราคา: {} จำนวน: {} ราคารวมทั้งหมด {} บาท วัน {}'.format(expense,price,qty,pricetotal,dt))
      text = 'รายการ: {} ราคา: {} จำนวน: {} ราคารวมทั้งหมด {} บาท'.format(expense,price,qty,pricetotal)
      v_result.set(text)

      v_expense.set('')
      v_price.set('')
      v_qty.set('')


      with open('savedatatotal.csv','a',encoding='utf-8',newline='') as f:
          fw = csv.writer(f)
          data=[dt,expense,price,qty,pricetotal]
          fw.writerow(data)


      E1.focus()
      update_table()
    except Exception as e: #Show error detail
      print('ERROR:',e)
      messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่')
      v_expense.set('')
      v_price.set('')
      v_qty.set('')
      #messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่')
      #messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่')




#ทำให้สามารถกด Enter ได้      
GUI.bind('<Return>',Save)     
Font1 =('TH SarabunPSK',20)
#-------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=Font1).pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=Font1)
E1.pack()
#--------------------
#-------text2--------
L = ttk.Label(F1,text='ราคา(บาท)',font=Font1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=Font1)
E2.pack()
#--------------------
#-------text3--------
L = ttk.Label(F1,text='จำนวน(ชิ้น)',font=Font1).pack()
v_qty = StringVar()
E2 = ttk.Entry(F1,textvariable=v_qty,font=Font1)
E2.pack()
#--------------------
savepic=PhotoImage(file='save.png').subsample(8)
B2=ttk.Button(F1,text='Save',image=savepic,compound='left',command=Save)
B2.pack(ipadx=40,ipady=20,pady=10)

v_result = StringVar()
v_result.set('------ผลลัพธ์------')
result = ttk.Label(F1,textvariable=v_result,font=Font1,foreground='green')
result.pack(pady=20)

###########ZONETAB2############
def read_csv():
  with open('savedatatotal.csv',newline='',encoding='utf-8') as f:
    fr=csv.reader(f)
    data=list(fr)
  return data

#Table

L = ttk.Label(Tab2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=Font1).pack(pady=20)

header=['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable=ttk.Treeview(Tab2,column=header,show='headings',height=10)
resulttable.pack()

#for i in range(len(header)):
  #resulttable.heading(header[i],text=header[i])
#column header
for h in header:
  resulttable.heading(h,text=h)
#Modify width in each column
headerwith=[150,170,80,80,80]
for h,w in zip(header,headerwith):
  resulttable.column(h,width=w)

def update_table():
  resulttable.delete(*resulttable.get_children())
  data=read_csv()
  for d in data:
    resulttable.insert('',0,value=d)

update_table()
    #print(data)
    #print(data[0][0])
    #for a,b,c,d,e in data:
      #print(e)
    #for d in data:
      #print()
#rs=read_csv()
#print(rs)
#header=['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']

GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()