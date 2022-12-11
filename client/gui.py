from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import json
import hashlib
from user import AuthorizedUser
from communicator import Communicator

class Gui:

	class ScreenType:
		entry = 0
		invalid_card = 1
		pin_code = 2
		invalid_pin = 3
		options = 4
		options_with_label = 5

	def __init__(
		self, title, win_size, bg_img=None, is_resizableX=False, is_resizeableY=False
	):
		# setting up window
		self.window = Tk()
		self.window.title(title)
		self.window.geometry(f"{win_size}x{win_size}")
		self.window.resizable(is_resizableX, is_resizeableY)
		self.win_size = win_size
		#
		# user inputs
		self.pin_input = ""
		self.amount_input = None
		self.receiver_card_input = None
		#
		# elements (btns/lables/etc), that are drawn on window
		self.elems_to_draw = {}
		#
		# inserted by user card. dict object. contains info about user card.
		self.user_card = None
		#
		# AuthorizedUser object, which is created after user inserts card and enters correct pin.
		# Is used for making queries to server in order to make operations [send_money/get_cash/check_balance]
		self.auth_user = None
		#
		# background image
		self.bg_img = bg_img
		self.set_background(bg_img)


	def __clear_screen(self):
		# empties elems_to_draw, so no elements are drawn.
		self.elems_to_draw = {}

	def __add_label(self, x=0, y=0, text="", fg="black", bg="white", font_size=25):
		lbl = Label(self.window, text=text, fg=fg, bg=bg, font=("Helvetica", font_size))
		self.elems_to_draw[lbl] = {"x": x, "y": y}
		return lbl

	def __add_button(self, x, y, text, h, w, callback):
		btn = Button(self.window,text=text,height=h,width=w,command=callback)
		self.elems_to_draw[btn] = {"x": x, "y": y}
		return btn

	def set_background(self, img_path=None):
		if img_path:
			self.bg_img = ImageTk.PhotoImage(Image.open(img_path))

	def __render_background_img(self, x=0, y=0):
		bg = Label(self.window, image=self.bg_img)
		self.elems_to_draw[bg] = {"x": x,"y": y}
		return self.elems_to_draw

	def __insert_card_callback(self):
		"""
		# is called, when user press button "insert card".
		# invoke user to insert card(attach file, that represents card)
		"""
		try:
			file_path = filedialog.askopenfilename(initialdir="../card_simulation", title="Select a File")
			with open(file_path, "r") as fd:
				fdata = json.loads(fd.read())
				# checks signature in order to check, taht card is valid.
				if fdata["signature"] != hashlib.md5(b'goodbankofindia').hexdigest():
					raise Exception("Signature is wrong")
				self.user_card = fdata 
			self.__clear_screen()
			self.render_pincode_enter_screen()
		except Exception as e:
			print(e)
			self.__clear_screen()
			self.render_invalid_card_screen();

	def render_entry_screen(self):
		self.set_background(img_path="./resources/bg.png")
		self.__render_background_img(x=-10, y=-10)
		self.__add_label(x=120, y=92, text="Hello guys,\nWelcome to Good Bank Of India", font_size=20)
		self.__add_button(x=139, y=230, text="<insert card>", h=1, w=28, callback=self.__insert_card_callback)
		return self.elems_to_draw

	def render_invalid_card_screen(self):
		self.render_entry_screen()
		self.__add_label(x=204, y=170, text="invalid card...", fg="red", font_size=20)
		return self.elems_to_draw

	def pincode_btn_press_callback(self, btn_text):
		if btn_text == "BACK":
			self.__exit()
		elif btn_text == "cancel" and len(self.pin_input)>0:
			self.pin_input = self.pin_input[0:-1]
			self.__clear_screen()
			display_pin = "*" * len(self.pin_input)
			self.render_pincode_enter_screen(pincode_lbl_text=display_pin)
		elif btn_text == "ENTER":
			if self.user_card["pincode"] == hashlib.md5(self.pin_input.encode()).hexdigest():
				if len(sys.argv) < 2:
					print("Invalid syntax: python3 gui.py <port:int>")
					self.__exit()
					exit(1)
				com = Communicator(ip="127.0.0.1", port=sys.argv[1])
				self.auth_user = AuthorizedUser(com, self.user_card["number"], self.user_card["cvv"], self.user_card["date"])
				self.__clear_screen()
				self.render_options_screen()
			else:
				# inserted card is invalid => signature is incorrect.
				self.render_invalid_pin_screen()
		elif btn_text in "#*0123456789" and len(self.pin_input) < 4:
			self.pin_input += btn_text
			self.__clear_screen()
			display_pin = "*" * len(self.pin_input)
			self.render_pincode_enter_screen(pincode_lbl_text=display_pin)


	def add_pincode_button(self, ch, x, y, h, w):
		button_explore = Button(
					self.window,
					text=ch,
					height=h,
					width=w,
					command=lambda: self.pincode_btn_press_callback(ch),
				)
		self.elems_to_draw[button_explore] = {"x": x,"y": y}

	def render_pincode_enter_screen(self, pincode_lbl_text="____",pinlabel_bg_color="white"):
		self.set_background(img_path="./resources/bg.png")
		self.__render_background_img(x=-10, y=-10)
		if len(pincode_lbl_text) < 4:
			pincode_lbl_text += "_" * ((len(pincode_lbl_text)-4) * -1)
		self.__add_label(x=147, y=76, text=f"  {pincode_lbl_text[0]}  {pincode_lbl_text[1]}  {pincode_lbl_text[2]}  {pincode_lbl_text[3]}  ", fg="black", bg=pinlabel_bg_color, font_size=40)
		template = [
			["#", "*", "cancel"],
			["1", "2", "3"],
			["4", "5", "6"],
			["7", "8", "9"],
			["BACK", "0", "ENTER"],
		]
		x_pos = 167
		y_pos = 150
		y_offset = 0
		for row in range(len(template)):
			x_offset=0
			for column in range(len(template[row])):
				self.add_pincode_button(template[row][column],x_pos+x_offset,y_pos+y_offset,2,5)
				x_offset += 60
			y_offset += 50
		return self.elems_to_draw

	def render_invalid_pin_screen(self):
		display_pin = "*" * len(self.pin_input)
		self.render_pincode_enter_screen(pinlabel_bg_color="red", pincode_lbl_text=display_pin)
		return self.elems_to_draw

	def __check_balance(self):
		response = self.auth_user.get_balance()
		response = json.loads(response)
		balance = str(float(response["data"]["balance"]))
		self.render_options_with_label_screen(label_msg=f"<Balance>\n{balance}", x=225, y=100)

	def __get_cash_callback(self):
		try:
			amount = float(self.amount_input.get())
		except:
			self.__clear_screen()
			self.render_options_with_label_screen(label_msg=f"incorrect amount", x=225, y=100, font_size=25)
			return
		response = json.loads(self.auth_user.get_cash(amount))
		if response["data"]["retcode"] == 1:
			self.__clear_screen()
			self.render_options_with_label_screen(label_msg=response["data"]["msg"], x=225, y=100, font_size=20)
		else:
			self.__clear_screen()
			self.render_options_with_label_screen(label_msg=f"take your cash", x=225, y=100, font_size=25)	

	def __get_cash(self):
		self.__clear_screen()
		self.render_options_screen()
		self.__add_label(x=250, y=60, text="Enter amount:", fg="black", bg="white", font_size=20)
		self.amount_input = Entry(self.window, width=20)
		self.amount_input.focus_set()
		self.elems_to_draw[self.amount_input] = {"x": 250,"y": 100}
		self.__add_button(250, 150, "get", 2, 10, self.__get_cash_callback)


	def __send_money_callback(self):
		receiver_card_num = self.receiver_card_input.get()
		if len(receiver_card_num) != 16:
			self.__clear_screen()
			self.render_options_with_label_screen(label_msg=f"incorrect receiver card", x=225, y=100, font_size=20)
			return
		for ch in receiver_card_num:
			if ch.isdigit() == False:
				self.__clear_screen()
				self.render_options_with_label_screen(label_msg=f"incorrect receiver card", x=225, y=100, font_size=20)
				return
		receiver = receiver_card_num[0:4]+"."+receiver_card_num[4:8]+"."+receiver_card_num[8:12]+"."+receiver_card_num[12:16]
		try:
			amount_to_send = float(self.amount_input.get())
		except:
			self.__clear_screen()
			self.render_options_with_label_screen(label_msg=f"incorrect amount", x=225, y=100, font_size=25)
			return
		response = self.auth_user.get_balance()
		response = json.loads(response)
		balance = float(response["data"]["balance"])
		if balance < amount_to_send:
			self.render_options_with_label_screen(label_msg=f"not enough money", x=225, y=100, font_size=25)
			return;
		response = json.loads(self.auth_user.send_money(receiver=receiver, amount=amount_to_send))
		if response["data"]["retcode"] == 1:
			self.render_options_with_label_screen(label_msg=response["data"]["msg"], x=225, y=100, font_size=25)
			return;
		elif response["data"]["retcode"] == 0:
			self.render_options_with_label_screen(label_msg="Money Sent", x=225, y=100, font_size=25)
			return;

	def __send_money(self):
		self.__clear_screen()
		self.render_options_screen()
		self.__add_label(x=250, y=0, text="Card to send money:", fg="black", font_size=20)
		self.receiver_card_input = Entry(self.window, width=20)
		self.receiver_card_input.focus_set()
		self.elems_to_draw[self.receiver_card_input] = {"x": 250,"y": 40}
		self.__add_label(x=250, y=80, text="Enter amount:", fg="black", font_size=20)
		self.amount_input = Entry(self.window, width=20)
		self.amount_input.focus_set()
		self.elems_to_draw[self.amount_input] = {"x": 250,"y": 120}
		self.__add_button(250, 180, "send", 2, 10, self.__send_money_callback)

	def __exit(self):
		self.pin_input = ""
		self.amount_input = None
		self.receiver_card_input = None
		self.user_card = None
		self.auth_user = None
		self.__clear_screen()
		self.render_entry_screen()

	def render_options_screen(self):
		self.set_background(img_path="./resources/wxp.jpeg")
		self.__render_background_img(x=-5, y=-5)
		options = {
			"check balance": self.__check_balance,
			"get cash": self.__get_cash,
			"send money": self.__send_money,
			"exit": self.__exit,
		}
		y = 0
		for option, callback in options.items():
			self.__add_button(0, y, option, 3, 15, callback)
			y += 70
		return self.elems_to_draw

	def render_options_with_label_screen(self, label_msg="", x=225, y=100, font_size=40):
		self.render_options_screen()
		self.__add_label(x=x, y=y, text=label_msg, fg="black", font_size=font_size)
		return self.elems_to_draw

	def set_screen(self, screen_type):
		self.__clear_screen()
		if screen_type == self.ScreenType.entry:
			gui.render_entry_screen()
		elif screen_type == self.ScreenType.invalid_card:
			gui.render_invalid_card_screen()
		elif screen_type == self.ScreenType.pin_code:
			gui.render_pincode_enter_screen()
		elif screen_type == self.ScreenType.invalid_pin:
			gui.render_invalid_pin_screen()
		elif screen_type == self.ScreenType.options:
			gui.render_options_screen()
		elif screen_type == self.ScreenType.options_with_label:
			gui.render_options_with_label_screen()
		else:
			raise Exception("Wrong screen")
		return self.elems_to_draw

	def update(self):
		for elem in self.elems_to_draw:
			elem.place(x=self.elems_to_draw[elem]["x"], y=self.elems_to_draw[elem]["y"])
		self.window.update()


if __name__ == "__main__":
	gui = Gui(title="ATM simulator", win_size=510, bg_img="./resources/bg.png")
	gui.set_screen(Gui.ScreenType.entry)
	while True:
		gui.update()


