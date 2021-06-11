import tkinter as tk

def writeWithTKinter(fileToWrite, buttonText):
	"""
    Write file with the text received as input from tkinter box
    """
    root= tk.Tk()
	canvas1 = tk.Canvas(root, width = 400, height = 300)
	canvas1.pack()
	entry1 = tk.Entry(root)
	canvas1.create_window(200, 140, window=entry1)
	def getSquareRoot():  
		inputText = entry1.get()
		fileToWrite.write(inputText)
		cc = ff.close()
		root.destroy()
	button1 = tk.Button(text=buttonText, command=getSquareRoot)
	canvas1.create_window(200, 180, window=button1)
	root.mainloop()