#Importing Dependencies
import tkinter as tk
from tkinter import ttk
import re
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter import messagebox as msg
import os.path,subprocess
from subprocess import STDOUT,PIPE
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


#Global Variables
input_data = []
output_data = [["","Total Time","Minimum Time","Maximum Time","Average Time","Makespan","Cost"]]



def compile_java(java_file,path,jar):
    command = "javac -classpath jars\\"+jar+"; examples\\org\\cloudbus\\cloudsim\\examples\\"+java_file
    subprocess.run(command,cwd=path)
def execute_java(java_file,stdin,path,jar,tab,algo):
	global output_data
	java_class,ext = os.path.splitext(java_file)
	cmd = "java -classpath jars\\"+jar+";examples org.cloudbus.cloudsim.examples."+java_class
	proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT,cwd=path)
	stdout,stderr = proc.communicate(stdin)
	output = stdout.decode("utf-8")
	totalTime = round(float(re.search("Total Time : ([0-9]*\.)?[0-9]+", output).group().split(":")[1].lstrip()),3)
	minTime = round(float(re.search("Minimum Time : ([0-9]*\.)?[0-9]+", output).group().split(":")[1].lstrip()),3)
	maxTime = round(float(re.search("Maximum Time : ([0-9]*\.)?[0-9]+", output).group().split(":")[1].lstrip()),3)
	avgTime = round(float(re.search("Average Time : ([0-9]*\.)?[0-9]+", output).group().split(":")[1].lstrip()),3)
	makespan = round(float(re.search("Makespan : ([0-9]*\.)?[0-9]+", output).group().split(":")[1].lstrip()),3)
	cost = round(float(re.search("Cost : ([0-9]*\.)?[0-9]+", output).group().split(":")[1].lstrip()),3)
	l = [algo,totalTime,minTime,maxTime,avgTime,makespan,cost]
	output_data.append(l)
	T = tk.Text(tab, height=100, width=200)
	T.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
	T.insert(tk.END, stdout)

nameEntered0 = 1
nameEntered1 = 1
win= None

#functionalities
def entryDataManualy():
	global input_data
	global nameEntered0
	global nameEntered1
	global win
	win = tk.Tk()

	win.title("Entry Data")
	labelsFrame=ttk.LabelFrame(win,text='Main function')
	labelsFrame.grid(column=0,row=0,padx=5,pady=5)
	aLabel0=ttk.Label(labelsFrame,text="Number of Cloudlets: ")
	aLabel0.grid(column=0,row=2,pady=10)
	nameEntered0=ttk.Entry(labelsFrame,width=60)
	nameEntered0.grid(column=1,row=2)
	nameEntered0.focus()
	aLabel1=ttk.Label(labelsFrame,text="Number of Virtual Machines: ")
	aLabel1.grid(column=0,row=4)
	nameEntered1=ttk.Entry(labelsFrame,width=60)
	nameEntered1.grid(column=1,row=4,pady=10)
	action=ttk.Button(labelsFrame, text="Entry",command=entry)
	action.grid(column=0,row=5,pady=5)
	# action=ttk.Button(labelsFrame, text="Upload Data",command=open_file)
	# action.grid(column=1,row=5,pady=5)


def entry():
	global nameEntered0
	global nameEntered1
	global win

	cloudlet=nameEntered0.get()
	vm=nameEntered1.get()

	with open("input.txt","w+") as file:
		file.write(str(cloudlet) + "\n")
		file.write(vm + "\n")
		for i in range(int(cloudlet)):
			num = random.randint(1000,3000)
			file.write(str(num)+"\n")
	win.destroy()
	
def open_file():
    """Open a file for editing."""
    global input_data
	# global win 
    filepath = askopenfilename(initialdir="c:",title="Select File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if filepath:
    	with open(filepath,'rb') as reader:
    		input_data = reader.read()
			# win.destroy()
	

def run():
	clear()
	global input_data
	if(input_data):
		#SJF
		file_name = 'ShortestJobFirst.java'
		compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
		execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab1,"Shortest Job First")
		#FCFS
		file_name = 'FCFS.java'
		compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
		execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab2,"FCFS")
		#MaxMin
		file_name = 'MaxMin.java'
		compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
		execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab3,"MaxMin")
		#ACO
		# file_name = 'ACO.java'
		# compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
		# execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab4,"ACO")
		# #PSO
		# file_name = 'MaxMin.java'
		# compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
		# execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab5,"PSO")
		
		drawTable(output_data,len(output_data),len(output_data[0]),tab6)
		input_data = []
	else:
		msg_ans = tk.messagebox.askyesnocancel(title="Input", message="Do you want to proceed without custom input?")
		if(msg_ans):
			#SJF
			file_name = 'ShortestJobFirst.java'
			compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
			execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab1,"Shortest Job First")
			#FCFS
			file_name = 'FCFS.java'
			compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
			execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab2,"FCFS")
			#MaxMin
			file_name = 'MaxMin.java'
			compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
			execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab3,"MaxMin")
			# #ACO
			# file_name = 'ACO.java'
			# compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
			# execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab4,"ACO")
			# #PSO
			# file_name = 'PSO_Scheduler.java'
			# compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
			# execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab5,"PSO")
			drawTable(output_data,len(output_data),len(output_data[0]),tab6)
			input_data = []		
		else:
			if(input_data):
				#SJF
				file_name = 'ShortestJobFirst.java'
				compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
				execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab1,"Shortest Job First")
				#FCFS
				file_name = 'FCFS.java'
				compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
				execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab2,"FCFS")
				#MaxMin
				file_name = 'MaxMin.java'
				compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
				execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab3,"MaxMin")
				#ACO
				# file_name = 'ACO.java'
				# compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
				# execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab4,"ACO")
				# #PSO
				# file_name = 'PSO_Scheduler.java'
				# compile_java(file_name,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar")
				# execute_java(file_name,input_data,"C:\\Users\Youssef\eclipse-workspace1\cloudsim-3.0.3","cloudsim-3.0.3.jar",tab5,"PSO")
				drawTable(output_data,len(output_data),len(output_data[0]),tab6)
				input_data = []
			else:
				tk.messagebox.showerror(title="Input Data Not Selected", message="Input Data Not Selected!!!\nPlease Select it from Open Option")

def clear():
	global output_data
	output_data = output_data[0:1]
	for tab in (tab1,tab2,tab3,tab6):#,tab4,tab5
		for widget in tab.winfo_children():
			widget.destroy()
		tab.pack_forget()

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return

#Comparaison Table
def drawTable(data,height,width,tab):
	fr_table = tk.Frame(master=tab)
	fr_table.pack(pady=50)
	for i in range(height): #Rows
		for j in range(width): #Column
			text = data[i][j]
			if(i==0 or j==0):
				b = tk.Label(fr_table, text=text,relief=tk.GROOVE,padx=40, pady=10,borderwidth=2)
				b.grid(row=i, column=j,sticky='NSEW')
			else:
				b = tk.Label(fr_table, text=text,relief=tk.SUNKEN,padx=40, pady=10,borderwidth=2,bg='#FFF')
				b.grid(row=i, column=j,sticky='NSEW')

def exit():
	answer = msg.askyesno("Exit","Are you sure to exit?")
	if(answer):
		window.destroy()


window = tk.Tk()
window.title(" CloudSim Project ")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
fr_display = tk.Frame(master=window,relief=tk.SUNKEN,borderwidth=2)
fr_buttons = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=4)
btn_data = tk.Button(fr_buttons, text="Manual Data", command=entryDataManualy)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_run = tk.Button(fr_buttons,text="Run",command=run)
btn_clr = tk.Button(fr_buttons,text="Clear",command=clear)
btn_save = tk.Button(fr_buttons, text="Save", command=save_file)
btn_exit = tk.Button(fr_buttons, text="Exit",command=exit)
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
btn_data.grid(row=0, column=0, sticky="ew", ipadx=15,ipady=5,padx=20, pady=10)
btn_open.grid(row=1, column=0, sticky="ew", ipadx=15,ipady=5,padx=20, pady=10)
btn_run.grid(row=2,column=0,sticky="ew", ipadx=15,ipady=5,padx=20, pady=10)
btn_clr.grid(row=3,column=0,sticky="ew", ipadx=15,ipady=5,padx=20, pady=10)
btn_save.grid(row=4, column=0, sticky="ew", ipadx=15,ipady=5,padx=20, pady=10)
btn_exit.grid(row=5,column=0,sticky="ew",ipadx=15,ipady=5,padx=20,pady=10)
fr_buttons.grid(row=0, column=0, sticky="ns")
fr_display.grid(row=0, column=1, sticky="nsew")
tabControl = ttk.Notebook(master=fr_display)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
# tab4 = ttk.Frame(tabControl)
# tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='SJF') 
tabControl.add(tab2, text ='FCFS') 
tabControl.add(tab3, text ='MaxMin')
# tabControl.add(tab4, text ='ACO')
# tabControl.add(tab5, text ='PSO')
tabControl.add(tab6, text ='Comparison Table')
tabControl.pack(expand = 1, fill ="both")
window.mainloop()
