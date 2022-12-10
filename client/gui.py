from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import json
import hashlib
from user import AuthorizedUser, Communicator

class ScreenType:
	entry = 0
	invalid_card = 1
	pin_code = 2
	invalid_pin = 3
	options = 4
	options_with_label = 5


class Gui:
	def __init__(
		self, title, win_size, bg_img=None, is_resizableX=False, is_resizeableY=False
	):
		self.window = Tk()
		self.title = title
		self.is_resizableX = is_resizableX
		self.is_resizeableY = is_resizeableY
		self.win_size = win_size
		self.elements_to_draw = {}
		self.pin_code_input = ""
		self.user_card = None
		self.auth_user = None
		self.amount_input = None
		self.send_card_input = None
		self.set_background_image(bg_img)
		self.__apply_settings()

	def __apply_settings(self):
		self.window.title(self.title)
		self.window.geometry(f"{self.win_size}x{self.win_size}")
		self.window.resizable(self.is_resizableX, self.is_resizeableY)

	def __insert_card_callback(self):
		file_path = filedialog.askopenfilename(initialdir="../card_simulation", title="Select a File")
		try:
			with open(file_path, "r") as fd:
				fdata = json.loads(fd.read())
				if fdata["signature"] != hashlib.md5(b'goodbankofindia').hexdigest():
					raise Exception("Signature is wrong")
				self.user_card = fdata 
			self.__clear_screen()
			self.render_pincode_enter_screen()
		except Exception as e:
			print(e)
			self.__clear_screen()
			self.render_invalid_card_screen();

	def __render_background_img(self, x=0, y=0):
		background = Label(self.window, image=self.bg_img)
		self.elements_to_draw[background] = {
			"x": x,
			"y": y,
		}
		return self.elements_to_draw

	def set_background_image(self, img_path=None):
		if img_path:
			self.bg_img = ImageTk.PhotoImage(Image.open(img_path))

	def __clear_screen(self):
		self.elements_to_draw = {}

	def render_entry_screen(self):
		self.set_background_image(img_path="./resources/bg.png")
		self.__render_background_img(x=-10, y=-10)
		# Text labels
		welcome_text = Label(
			self.window, text="Hello guys,\nWelcome to Good Bank Of India", fg="black", font=("Helvetica", 20)
		)
		self.elements_to_draw[welcome_text] = {
			"x": 120,
			"y": int(self.win_size * 0.182),
		}

		# button to insert card
		button_explore = Button(
			self.window,
			text="<insert card>",
			height=1,
			width=28,
			command=self.__insert_card_callback,
		)
		self.elements_to_draw[button_explore] = {
			"x": int(self.win_size * 0.273),
			"y": int(int(self.win_size * 0.182) * 2.5),
		}
		return self.elements_to_draw

	def render_invalid_card_screen(self):
		self.render_entry_screen()
		invalid_card_msg = Label(
			self.window, text="invalid card...", fg="red", font=("Helvetica", 20)
		)
		self.elements_to_draw[invalid_card_msg] = {
			"x": int(self.win_size * 0.40),
			"y": 170,
		}
		return self.elements_to_draw

	def pincode_press(self, btn_text):
		if btn_text == "BACK":
			self.__exit()
		elif btn_text == "cancel" and len(self.pin_code_input)>0:
			self.pin_code_input = self.pin_code_input[0:-1]
			display_pin = "*" * len(self.pin_code_input)
			self.__clear_screen()
			self.render_pincode_enter_screen(pincode_lbl_text=display_pin)
		elif btn_text == "ENTER":
			if self.user_card["pincode"] == hashlib.md5(self.pin_code_input.encode()).hexdigest():
				com = Communicator(ip="127.0.0.1", port=sys.argv[1])
				self.auth_user = AuthorizedUser(com, self.user_card["number"], self.user_card["cvv"], self.user_card["date"])
				self.__clear_screen()
				self.render_options_screen()
			else:
				self.render_invalid_pin_screen()
		elif btn_text in "#*0123456789" and len(self.pin_code_input) < 4:
			self.pin_code_input += btn_text
			display_pin = "*" * len(self.pin_code_input)
			self.__clear_screen()
			self.render_pincode_enter_screen(pincode_lbl_text=display_pin)


	def add_button(self, ch, x, y, h, w):
		button_explore = Button(
					self.window,
					text=ch,
					height=h,
					width=w,
					command=lambda: self.pincode_press(ch),
				)
		self.elements_to_draw[button_explore] = {
			"x": x,
			"y": y,
		}

	def render_pincode_enter_screen(self, pincode_lbl_text="____",pinlabel_bg_color="white"):
		self.set_background_image(img_path="./resources/bg.png")
		self.__render_background_img(x=-10, y=-10)

		if len(pincode_lbl_text) < 4:
			pincode_lbl_text += "_" * ((len(pincode_lbl_text)-4) * -1)
		pincode_text = Label(
			self.window,
			text=f"  {pincode_lbl_text[0]}  {pincode_lbl_text[1]}  {pincode_lbl_text[2]}  {pincode_lbl_text[3]}  ",
			fg="black",
			bg=pinlabel_bg_color,
			font=("Helvetica", 40),
		)
		self.elements_to_draw[pincode_text] = {
			"x": int(self.win_size * 0.29),
			"y": int(self.win_size * 0.15),
		}
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
				self.add_button(template[row][column],x_pos+x_offset,y_pos+y_offset,2,5)
				x_offset += 60
			y_offset += 50
		return self.elements_to_draw

	def render_invalid_pin_screen(self):
		display_pin = "*" * len(self.pin_code_input)
		self.render_pincode_enter_screen(pinlabel_bg_color="red", pincode_lbl_text=display_pin)
		return self.elements_to_draw

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
		
		amount_lbl = Label(
			self.window, text="Enter amount:", fg="black", font=("Helvetica", 20)
		)
		self.elements_to_draw[amount_lbl] = {
			"x": 250,
			"y": 60,
		}
		self.amount_input = Entry(self.window, width=20)
		self.amount_input.focus_set()
		self.elements_to_draw[self.amount_input] = {
			"x": 250,
			"y": 100,
		}
		get_btn = Button(
				self.window,
				text="get",
				height=2,
				width=10,
				command=self.__get_cash_callback,
		)
		self.elements_to_draw[get_btn] = {
			"x": 250,
			"y": 150,
		}


	def __send_money_callback(self):
		receiver_card_num = self.send_card_input.get()
		if len(receiver_card_num) != 16:
			self.__clear_screen()
			self.render_options_with_label_screen(label_msg=f"incorrect receiver card", x=225, y=100, font_size=20)
			return
		for ch in receiver_card_num:
			if ch.isdigit() == False:
				self.__clear_screen()
				self.render_options_with_label_screen(label_msg=f"incorrect receiver card", x=225, y=100, font_size=20)
				return
		receiver = receiver_card_num[0:4] + "." + receiver_card_num[4:8] + "." + receiver_card_num[8:12] + "." + receiver_card_num[12:16]		
		print(receiver)
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
		
		send_card_lbl = Label(
			self.window, text="Card to send money:", fg="black", font=("Helvetica", 20)
		)
		self.elements_to_draw[send_card_lbl] = {
			"x": 250,
			"y": 0,
		}
		self.send_card_input = Entry(self.window, width=20)
		self.send_card_input.focus_set()
		self.elements_to_draw[self.send_card_input] = {
			"x": 250,
			"y": 40,
		}

		amount_lbl = Label(
			self.window, text="Enter amount:", fg="black", font=("Helvetica", 20)
		)
		self.elements_to_draw[amount_lbl] = {
			"x": 250,
			"y": 80,
		}
		self.amount_input = Entry(self.window, width=20)
		self.amount_input.focus_set()
		self.elements_to_draw[self.amount_input] = {
			"x": 250,
			"y": 120,
		}
		send_btn = Button(
				self.window,
				text="send",
				height=2,
				width=10,
				command=self.__send_money_callback,
		)
		self.elements_to_draw[send_btn] = {
			"x": 250,
			"y": 180,
		}

	def __exit(self):
		# goes to enrty screen
		self.pin_code_input = ""
		self.user_card = None
		self.auth_user = None
		self.__clear_screen()
		self.render_entry_screen()

	def render_options_screen(self):
		self.set_background_image(img_path="./resources/wxp.jpeg")
		self.__render_background_img(x=-5, y=-5)
		options = {
			"check balance": self.__check_balance,
			"get cash": self.__get_cash,
			"send money": self.__send_money,
			"exit": self.__exit,
		}

		distance = 0
		for option, callback in options.items():
			button_explore = Button(
				self.window,
				text=option,
				height=3,
				width=15,
				command=callback,
			)
			self.elements_to_draw[button_explore] = {
				"x": 0,
				"y": 0 + distance,
			}
			distance += 70
		return self.elements_to_draw

	def render_options_with_label_screen(self, label_msg="", x=225, y=100, font_size=40):
		self.render_options_screen()
		lbl = Label(
			self.window, text=label_msg, fg="black", font=("Helvetica", font_size)
		)
		self.elements_to_draw[lbl] = {
			"x": x,
			"y": y,
		}
		return self.elements_to_draw

	def set_screen(self, screen_type):
		self.__clear_screen()
		if screen_type == ScreenType.entry:
			gui.render_entry_screen()
		elif screen_type == ScreenType.invalid_card:
			gui.render_invalid_card_screen()
		elif screen_type == ScreenType.pin_code:
			gui.render_pincode_enter_screen()
		elif screen_type == ScreenType.invalid_pin:
			gui.render_invalid_pin_screen()
		elif screen_type == ScreenType.options:
			gui.render_options_screen()
		elif screen_type == ScreenType.options_with_label:
			gui.render_options_with_label_screen()
		else:
			raise Exception("Wrong screen")
		self.update()
		return self.elements_to_draw

	def update(self):
		for elem in self.elements_to_draw:
			elem.place(x=self.elements_to_draw[elem]["x"], y=self.elements_to_draw[elem]["y"])
		self.window.update()





if __name__ == "__main__":
	gui = Gui(title="ATM simulator", win_size=510, bg_img="./resources/bg.png")
	gui.set_screen(ScreenType.entry)

	while True:

		gui.update()
