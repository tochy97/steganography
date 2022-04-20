from distutils import extension
from re import I
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from functools import partial

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()


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



def hide_secret(secret, container, start, inbetween):
    # where the message hiding happens

    stop = start
    inner_stop = 0
    # holds new byte array
    output = b""+start.to_bytes(1, "big")+inbetween.to_bytes(1, "big")
    # count will keep track of how many we have skipped
    count = 0
    iteration = 0
    for container_block in container:
        count += 1

        # we will only be replacing bits of the start byte of the container
        # and every bit that is inbetween distance away
        if((count == start) | ((count > stop) & (count == (stop + inbetween)))):

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


def hide_a_message():
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

    hidden_data = hide_secret(secret=first.data, container=second.data, start=10, inbetween=5)

    save_file = fd.asksaveasfile(mode='wb')

    if save_file == None:
        return
    else:
        save_file.write(hidden_data)


create_secret = ttk.Button(
    frm,
    text='Select file to hide',
    command=lambda: [hide_a_message()]
)


def get_secret(message):
    print("before ", message)
    start = 0
    inbetween = 0
    output = b""

    # count will keep track of how many we have skipped
    count = 0

    for message_block in message:
        if(count == 0):
            start = message_block
        if(count == 1):
            inbetween = message_block
        count += 1
    end = message[-1]
    count = 0
    iteration = 0
    start += 2
    stop = start
    print(start, inbetween, end," hello")
    for message_black in message:
        count += 1
        if((count == start) | ((count > stop) & (count == (stop + inbetween))) & (iteration < end)):
            iteration += 1
            stop = count
            output += message_black.to_bytes(1, "big")
    print(iteration,end, "after ",output)
    return output

def get_that_secret():
    message = select_a_file()
    if(message == None):
        return
    get_secret(message.data)


def print_byte_data():
    message = select_a_file()
    print(message.data)
    


print_byte = ttk.Button(
    frm,
    text='Print byte data',
    command=lambda: [print_byte_data()]
)        

extract_secret = ttk.Button(
    frm,
    text='Select file with a secret',
    command=lambda: [get_that_secret()]
)

# all the home screen buttons
create_secret.pack()
extract_secret.pack()
print_byte.pack()
root.mainloop()
