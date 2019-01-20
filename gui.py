import os
import sys
import time

from tkinter import *
from tkinter import filedialog

from scraper import Scraper


class StdRedirector():
	def __init__(self, text_widget):
		self.text_space = text_widget

	def write(self, string):
		self.text_space.config(state=NORMAL)
		self.text_space.insert(END, string)
		self.text_space.see(END)
		self.text_space.config(state=DISABLED)


class Window(Tk):
	def __init__(self):
		Tk.__init__(self)

		self.title("long-live")

		f0 = Frame(self)
		f1 = Frame(self)
		f2 = Frame(self)
		f3 = Frame(self)
		f4 = Frame(self)
		f5 = Frame(self)
		f0.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
		f1.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
		f2.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
		f3.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
		f4.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
		f5.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

		self.option_add("*Font", ("TkDefaultFont", 12))

		self.default = StringVar(self, os.path.abspath(os.path.dirname(__file__)))

		self.entry_save = Entry(f1, textvariable=self.default, width=50)
		self.entry_save.pack(side=LEFT, ipadx=4, ipady=4, padx=4, pady=4)
		button_save = Button(f1, text="Browse...", width=9, command=self.browse)
		button_save.pack(side=LEFT, padx=4, pady=4)

		label_base = Label(f2, text="base_url", anchor=W, width=7)
		label_base.pack(side=LEFT, padx=4, pady=4)
		self.entry_base = Entry(f2, width=50)
		self.entry_base.pack(side=LEFT, ipadx=4, ipady=4, padx=4, pady=4)

		label_start = Label(f3, text="start_url", anchor=W, width=7)
		label_start.pack(side=LEFT, padx=4, pady=4)
		self.entry_start = Entry(f3, width=50)
		self.entry_start.pack(side=LEFT, ipadx=4, ipady=4, padx=4, pady=4)
		self.ps_value = BooleanVar()
		check_ps = Checkbutton(f3, text="ps", variable=self.ps_value)
		check_ps.pack(side=LEFT, padx=4, pady=4)

		# self.option_add("*Font", "TkFixedFont")

		# output = Text(f4, state=DISABLED)
		# output.pack()
		# sys.stdout = StdRedirector(output)
		# sys.stderr = StdRedirector(output)

		# self.option_add("*Font", ("TkDefaultFont", 12))

		button_start = Button(f5, text="Start", width=5, command=self.start)
		button_start.pack(side=LEFT, padx=4, pady=4)
		button_close = Button(f5, text="Close", width=5, command=self.quit)
		button_close.pack(side=LEFT, padx=4, pady=4)

	def browse(self):
		path = filedialog.askdirectory()
		self.default.set(path)

	def start(self):
		save_location = self.entry_save.get()
		base_url = self.entry_base.get()
		start_url = self.entry_start.get()
		ps = self.ps_value.get()

		# print(save_location, base_url, start_url, ps)

		self.destroy()

		scraper = Scraper(save_location, base_url)

		start = time.time()
		scraper.scrape(start_url, ps=ps)
		end = time.time() - start

		print(round(end), "seconds")
		print(scraper.total, "images")


def main():
	Window().mainloop()


if __name__ == '__main__':
	main()
