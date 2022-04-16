# import packages, modules and dependencies
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# create main window
compiler = Tk()
compiler.title('PyLeaf IDE')
file_path = ''

# set file path


def set_file_path(path):
    global file_path
    file_path = path


def redo():
    editor.edit_redo()


def undo():
    editor.edit_undo()


def copy():
    editor.clipboard_clear()
    editor.clipboard_append(editor.selection_get())


def cut():
    editor.clipboard_clear()
    editor.clipboard_append(editor.selection_get())
    editor.delete(SEL_FIRST, SEL_LAST)


def paste():
    editor.insert(INSERT, editor.clipboard_get())


def select_all():
    editor.tag_add(SEL, '1.0', END)


# define open_file function
def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

# define save_as function


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

# define run function


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code!')
        text.pack()
        return
    command = f'python {file_path}'
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)


# create menu bar
menu_bar = Menu(compiler)

# add command to the File menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

# add command to the Edit menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Undo', command=undo)
file_menu.add_command(label='Redo', command=redo)
file_menu.add_separator()
file_menu.add_command(label='Cut', command=cut)
file_menu.add_command(label='Copy', command=copy)
file_menu.add_command(label='Paste', command=paste)
file_menu.add_command(label='Select All', command=select_all)
file_menu.add_separator()
file_menu.add_command(label='Find', command=find)
file_menu.add_command(label='Replace', command=exit)
menu_bar.add_cascade(label='Edit', menu=file_menu)

# add command to the Run menu
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

# set the menu bar to the config bar in tkinter
compiler.config(menu=menu_bar)

# create text part
editor = Text(width=1079, undo=True)
editor.pack()

# create output part
code_output = Text(height=10, width=1079)
code_output.pack()

# run the window
compiler.mainloop()
