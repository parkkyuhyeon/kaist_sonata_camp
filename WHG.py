from bs4 import BeautifulSoup
import requests
from tkinter import *
import tkinter.font
from PIL import ImageTk,Image


selection_en = ['breakfast', 'lunch', 'dinner']
menu = []
Date = []


def resetarray(arr):
	length = len(arr)
	for _ in range(length):
		arr.pop()


def getDate(num1, num2):
	if(int(num1) < 10):
		num1 = '0'+num1
	Date.append(num1)
	Date.append(num2)


def getMenu():
	fullUrl = 'http://daeseong.hs.kr/?act=lunch.main&month={0}/01/2018&mcode=1217'.format(Date[0])
	try:
		response = requests.get(fullUrl)
	except:
		print('인터넷 연결을 확인해주세요')
		return
	response.encoding = 'euc-kr'
	response_html = response.text
	soup = BeautifulSoup(response_html, 'html.parser')
	for i in range(3):
		text_url = soup.select('#dayBoxContent_{0}_{1} > span > a'.format(selection_en[i], Date[1]))
		try:
			food = str(text_url[0])
			text_url.pop()
			food = food.replace('<a href="/?act=lunch.main2&amp;month=2018.{0}.{1}&amp;mcode=1217">'.format(Date[0], Date[1]), '')
			food = food.replace('<br/>', '')
			food = food.replace('</a>', '')
			food = food.replace('\r\n', '\n')
			menu.append(food)
		except IndexError:
			menu.append('')


class MainWindow:
	def __init__(self):
		root = Tk()
		root.title('급식')
		fonts=tkinter.font.Font(family = "맑은 고딕", size=30)
		font1=tkinter.font.Font(family = "맑은 고딕", size=20)
		self.canvas = Canvas(root)
		self.board=ImageTk.PhotoImage(file='./칠판.gif')
		self.image_on_canvas=self.canvas.create_image(0,0,anchor=NW,image=self.board)

		self.canvas.config(width=1300, height=660)
		self.canvas.config(highlightthickness=0)
		self.canvas.create_text(215, 100, text='아침', font=fonts, anchor=N, fill='pink')
		self.canvas.create_line(130,150,300,150,fill='blue',width=3)
		self.canvas.create_text(615, 100, text='점심', font=fonts, anchor=N, fill='pink')
		self.canvas.create_line(530,150,700,150,fill='blue',width=3)
		self.canvas.create_text(1015, 100, text='저녁', font=fonts, anchor=N, fill='pink')
		self.canvas.create_line(930,150,1100,150,fill='blue',width=3)
		self.breakfast = self.canvas.create_text(215, 200, text='', font=fonts, anchor=N, fill='white', justify=CENTER)
		self.lunch = self.canvas.create_text(615, 200, text='', font=fonts, anchor=N, fill='white', justify=CENTER)
		self.dinner = self.canvas.create_text(1015, 200, text='', font=fonts, anchor=N, fill='white', justify=CENTER)
		root.bind('<Key>',self.key_input)
		self.canvas.pack(expand=YES)
		self.inputButton = Button(root, text='확인', command=self.onButton)
		self.inputButton.place(x=700,y=10,anchor=NW)
		self.month_value=StringVar()
		self.month_value.set(1)
		self.month_box=OptionMenu(root, self.month_value, 1,2,3,4,5,6,7,8,9,10,11,12)
		self.month_box.place(x=500,y=10, anchor=NW)
		self.day_value=StringVar()
		self.day_value.set(1)
		self.canvas.create_text(560,10,text='월',font=font1, anchor=NW, fill='white')
		self.day_box=OptionMenu(root, self.day_value, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
		self.day_box.place(x=600,y=10, anchor=NW)
		self.canvas.create_text(660,10,text='일',font=font1, anchor=NW, fill='white')

	def onButton(self):
		resetarray(Date)
		resetarray(menu)
		string = [self.month_value.get(), self.day_value.get()]
		getDate(string[0], string[1])
		getMenu()
		for i in range(3):
			try:
				self.canvas.itemconfig(eval('self.'+selection_en[i]), text=menu[i])
			except IndexError:
				pass

	def key_input(self,value):
		if(value.keysym=='Return'):
			self.onButton()


MainWindow()
mainloop()
