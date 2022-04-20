from distutils import extension
from re import I
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from functools import partial

root = Tk()

frm = ttk.Frame(root, padding=10)
frm.pack()

entry = ttk.Frame(root, padding=10)


class FileComp:
    # object used to hold file name, extension and binary data

    def __init__(self, name, extension, data):
        self.name = name
        self.extention = extension
        self.data = data


def select_a_file():
    # select a file and return a object with the name, extension and binary data as values

    file = fd.askopenfilename(
        title='Select a file',
        initialdir='/',)

    if not file:
        return None
    try:
        with open(file, 'rb') as tf:
            data = tf.read()

        extension = file.split(".")[-1]
        name = file.split("/")[-1].split(".")[0]
        return FileComp(name, extension, data)
    except:
        showinfo(
            title="Error!",
            message="Something went wrong"
        )
        return None


def hide_secret(secret, container, start, increment):
    # where the message hiding happens

    stop = start
    inner_stop = 0
    # holds new byte array
    output = b""+start.to_bytes(1, "big")+increment.to_bytes(1, "big")
    # count will keep track of how many we have skipped
    count = 0
    iteration = 0
    for container_block in container:
        count += 1

        # we will only be replacing bits of the start byte of the container
        # and every bit that is increment distance away
        if((count == start) | ((count > stop) & (count == (stop + increment)))):

            # stop keeps track of where we stopped in container byte steam
            stop = count

            # inner_count keeps track of where we are in secret message byte steam
            inner_count = 0

            # holds new byte data
            for secret_block in secret:
                inner_count += 1
                # this ensures we only read 1 block at a time
                if(inner_count > inner_stop):
                    inner_stop = inner_count
                    output += secret_block.to_bytes(1, "big")
                    iteration += 1
                    break
        else:
            output += container_block.to_bytes(1, "big")
            # keeps track of where we stopped in secret message
    output += iteration.to_bytes(1, "big")
    return output


start_label = Label(
    entry, 
    text="Enter starting index", 
    font=('Calibri 10')
    )
start_box = Entry(
    entry, 
    width=35
    )

increment_label = Label(
    entry, 
    text="Enter increment value", 
    font=('Calibri 10')
    )
increment_box = Entry(
    entry, 
    width=35
    )

def hide_a_message(start, increment):
    # choose the  file you want to hide and the container file

    first = select_a_file()

    if first == None:
        return
    else:
        showinfo(
            title="File to hide",
            message="Secret file : " + first.name + "." + first.extention
        )

    second = select_a_file()

    if second == None:
        return

    try:
        hidden_data = hide_secret(
            secret=first.data, 
            container=second.data, 
            start=int(start),
            increment=int(increment)
        )
    except:
        return showinfo(
            title="Error",
            message="Failed to hide, values too large"
        )
    
    save_file = fd.asksaveasfile(mode='wb')

    if save_file == None:
        return
    else:
        save_file.write(hidden_data)
        showinfo(
            title="Success",
            message="Message hidden!"
        )
    start_label.pack_forget()
    start_box.pack_forget()
    increment_label.pack_forget()
    increment_box.pack_forget()
    entry.pack_forget()
    increment_box.pack
    return frm.pack()


def get_start_increment():
    frm.pack_forget()
    entry.pack()
    start_label.pack()
    start_box.pack()
    increment_label.pack()
    increment_box.pack()
    hide_me = ttk.Button(
        entry,
        text='Select file to hide',
        command=lambda: [hide_a_message(
            start=start_box.get(), 
            increment=increment_box.get()
            )]
    ).pack()



create_secret = ttk.Button(
    frm,
    text='Hide secret in file',
    command=lambda: [get_start_increment()]
).pack()


def get_secret(message):
    start = 0
    increment = 0
    output = b""

    # count will keep track of how many we have skipped
    count = 0

    for message_block in message:
        if(count == 0):
            start = message_block
        if(count == 1):
            increment = message_block
        count += 1
    end = message[-1]
    count = 0
    iteration = 0
    start += 2
    stop = start
    for message_black in message:
        count += 1
        if((count == start) | ((count > stop) & (count == (stop + increment))) & (iteration < end)):
            iteration += 1
            stop = count
            output += message_black.to_bytes(1, "big")
    return output

def get_that_secret():
    message = select_a_file()
    if(message == None):
        return
    try:
        hidden_data = get_secret(message.data)
    except:
        showinfo(
            title="Error",
            message="Failed to hide"
        )
    save_file = fd.asksaveasfile(mode='wb')

    if save_file == None:
        return
    else:
        save_file.write(hidden_data)
        showinfo(
            title="Success",
            message="Message hidden!"
        )


def print_byte_data():
    message = select_a_file()


print_byte = ttk.Button(
    frm,
    text='Print byte data',
    command=lambda: [print_byte_data()]
).pack()        

extract_secret = ttk.Button(
    frm,
    text='Select file with a secret',
    command=lambda: [get_that_secret()]
).pack()

# all the home screen buttons
root.mainloop()
