import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import colorchooser

global open_status
open_status = False

global selected_text
selected_text=None


root = tk.Tk()
root.title("TEXT EDITOR")
root.geometry("1360x740")


# New File
def newFile():
    global open_status
    open_status = False

    text.delete("1.0", tk.END)
    root.title("New file - TEXT EDITOR")
    status_bar.config(text= "New File         ")

# Open File
def openFile():
    text.delete("1.0", tk.END)
    text_file = filedialog.askopenfilename(initialdir="D:/",title="Open File", filetypes= (("Text Fileas","*.txt"),("HTML Files","*.html"),("Python Files","*.py"),("All Files","*.*")))
    name = text_file
    if name=='':
        return None
    
    global open_status
    open_status = text_file

    status_bar.config(text=name+"         ")
    name = name.replace("D:/",'')
    root.title(name+" - TEXT EDITOR")

    text_file = open(text_file,'r')
    content = text_file.read()
    text.insert(tk.END,content)

    text_file.close()

# Save As File
def saveAs():
    text_file = filedialog.asksaveasfilename(initialdir="D:/",title= "Save As", defaultextension="*.txt",filetypes= (("Text Fileas","*.txt"),("HTML Files","*.html"),("Python Files","*.py"),("All Files","*.*")))
    if text_file:
        name=text_file
        status_bar.config(text=name+"         ")
        name = name.replace("D:/",'')
        root.title(name+" - TEXT EDITOR")

        text_file = open(text_file,'w')
        content = text.get("1.0", tk.END)
        text_file.write(content)

        text_file.close()

# SAve File
def saveFile():
    if open_status:
        text_file = open(open_status,'w')
        content = text.get("1.0", tk.END)
        text_file.write(content)

        text_file.close()

        status_bar.config(text=f'Saved {open_status}         ')
    else:
        saveAs()

# Cut Text
def cut(e):
    global selected_text

    if e:
        selected_text = root.clipboard_get()
        text.delete("sel.first","sel.last")

    elif text.selection_get():
        selected_text = text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected_text)
        text.delete("sel.first","sel.last")

# Copy Text
def copy(e):
    global selected_text

    if e:
        selected_text = root.clipboard_get()

    elif text.selection_get():
        selected_text = text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected_text)

# Paste Text
def paste(e):
    global selected_text

    if e:
        selected_text = root.clipboard_get()


    elif selected_text:
        position = text.index(tk.INSERT)
        text.insert(position,selected_text)

# Bold Text
def bold():
    bold_font = font.Font(text,text.cget('font'))
    bold_font.configure(weight='bold')
    
    text.tag_configure('bold', font= bold_font)
    if text.tag_ranges("sel"):
        current_tags = text.tag_names("sel.first")

    if 'bold' in current_tags:
        text.tag_remove('bold',"sel.first","sel.last")
    else:
        text.tag_add('bold',"sel.first","sel.last")

# Italic Text
def italics():
    italics_font = font.Font(text,text.cget('font'))
    italics_font.configure(slant='italic')
    
    text.tag_configure('italics', font= italics_font)
    if text.tag_ranges("sel"):
        current_tags = text.tag_names("sel.first")

    if 'italics' in current_tags:
        text.tag_remove('italics',"sel.first","sel.last")
    else:
        text.tag_add('italics',"sel.first","sel.last")

# Color Text
def text_color():
    selected_color = colorchooser.askcolor()[1]

    if selected_color:
        color_font = font.Font(text,text.cget('font'))
    
        text.tag_configure('colored', font= color_font,foreground=selected_color)
        if text.tag_ranges("sel"):
            current_tags = text.tag_names("sel.first")

        if 'colored' in current_tags:
            text.tag_remove('colored',"sel.first","sel.last")
        else:
            text.tag_add('colored',"sel.first","sel.last")

# Color All Text
def all_text_color():
    selected_color = colorchooser.askcolor()[1]

    if selected_color:
        text.config(foreground=selected_color)


# Background color
def bg_color():
    selected_color = colorchooser.askcolor()[1]

    if selected_color:
        text.config(background=selected_color)


# Main Frame
main_frame = tk.Frame()
main_frame.pack(pady=8)

# Toolbar
toolbar=tk.Frame(main_frame)
toolbar.pack(fill='x',pady=3)

bold_button=tk.Button(toolbar, text="Bold", command=bold)
bold_button.grid(row=0, column=0, sticky=tk.W)

italics_button=tk.Button(toolbar, text="Italics", command=italics)
italics_button.grid(row=0, column=1,padx=5)

color_button=tk.Button(toolbar, text="Color", command=text_color)
color_button.grid(row=0, column=2)

# Scroll Bar
text_scroll_up = tk.Scrollbar(main_frame)
text_scroll_up.pack(side="right",fill='y')

text_scroll_side = tk.Scrollbar(main_frame,orient= "horizontal")
text_scroll_side.pack(side="bottom",fill='x')

# Text Editor
text=tk.Text(main_frame,width=110, font= ("Times", 18), selectbackground="blue", selectforeground="white",xscrollcommand=text_scroll_side.set, undo=True, yscrollcommand=text_scroll_up.set,wrap="none")
text.pack(fill='both')

text_scroll_up.config(command=text.yview)
text_scroll_side.config(command=text.xview)


# Menu Bar
menuBar = tk.Menu(root)
root.config(menu=menuBar)

file_menu=tk.Menu(menuBar, tearoff=False)
menuBar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=newFile)
file_menu.add_command(label="Open", command=openFile)
file_menu.add_command(label="Save",command=saveFile)
file_menu.add_command(label="Save As",command=saveAs)
file_menu.add_separator()
file_menu.add_command(label="Close", command=root.quit)

edit_menu=tk.Menu(menuBar, tearoff=False)
menuBar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut   ",command= lambda: cut(False), accelerator="Ctrl+X")
edit_menu.add_command(label="Copy   ",command= lambda: copy(False), accelerator="Ctrl+C")
edit_menu.add_command(label="Paste   ",command= lambda: paste(False), accelerator="Ctrl+V")
edit_menu.add_command(label="Undo   ",command= text.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo   ",command= text.edit_redo, accelerator="Ctrl+R")

color_menu=tk.Menu(menuBar,tearoff=False)
menuBar.add_cascade(label="Colors",menu=color_menu)
color_menu.add_command(label="Selected Text",command=text_color)
color_menu.add_command(label="All Text",command=all_text_color)
color_menu.add_command(label="Background",command=bg_color)


# Status Bar
status_bar=tk.Label(root, text="Ready         ", anchor=tk.E)
status_bar.pack(fill=tk.X,side=tk.BOTTOM,ipady=20)

# Edit Key Bindings
root.bind('<Control-c>', copy)
root.bind('<Control-x>', cut)
root.bind('<Control-v>', paste)



root.mainloop()
