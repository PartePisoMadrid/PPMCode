import tkinter as tk

def writeFile(fileToWritePath, buttonText, isBigWindow=False):
	"""
    get input and write it in a file with the text received from tkinter box
    """
	ff = open(fileToWritePath, "w")
	root = tk.Tk()
	canvas1 = tk.Canvas(root, width = 800, height = 500)
	canvas1.pack()
	#entry1 = tk.Entry(root)
	t = tk.Text(root, height=15, width=50, font=("Courier", 14))
	t.pack()
	canvas1.create_window(400, 150, window=t)
	def getSquareRoot():
		inputText = t.get("1.0", "end-1c")
		ff.write(inputText)
		ff.close()
		root.destroy()
	button1 = tk.Button(text=buttonText, command=getSquareRoot)
	canvas1.create_window(410, 310, window=button1)
	root.mainloop()
	ff = open(fileToWritePath, "r")
	inputText = ff.read()
	print("inputText", inputText)
	ff.close()
	return inputText

