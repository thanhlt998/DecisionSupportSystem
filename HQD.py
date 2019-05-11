import tkinter as tk
import tkinter.messagebox
from settings import GAME_TAGS


class CheckbuttonList(tk.LabelFrame):
    def __init__(self, master, text=None, list_of_cb=None):
        super().__init__(master)

        self['text'] = text
        self.list_of_cb = list_of_cb
        self.cb_values = dict()
        self.check_buttons = dict()

        if self.list_of_cb:
            col = 0
            row = 1
            for item in list_of_cb:
                col += 1
                self.cb_values[item] = tk.BooleanVar()
                self.check_buttons[item] = tk.Checkbutton(self, text=item)
                self.check_buttons[item].config(onvalue=True, offvalue=False,
                                                variable=self.cb_values[item])
                self.check_buttons[item].grid(row=row, column=1 + col)
                if (col > 7):
                    row += 1
                    col = 0


def find(_range, _type, platform):
    a = _range.get()
    type_list = _type.cb_values
    res_types= []
    for k, v in type_list.items():
        if v.get():
            res_types.append(k)

    return get_search_link(res_types)

    # tkinter.messagebox.showinfo("Result", f"{res}{a}")


# root = tk.Tk()
#
# root.geometry('550x250')
# root.title("Game Picker")
#
# Type = GAME_TAGS.keys()
# Platform = ["PC", "XBox", "PS"]
#
# _type = CheckbuttonList(root, "Type", Type)
# _type.place(x=10, y=10)
#
# platform = CheckbuttonList(root, "Platform", Platform)
# platform.place(x=10, y=100)
#
# price = tk.Label(root, text="max price($)")
# price.place(x=10, y=150)
# _range = tk.Scale(root, from_=0, to=1000, orient=tk.HORIZONTAL, length=500)
# _range.place(x=10, y=170)
#
# submit = tk.Button(root, text="Find", command=find)
# submit.place(x=10, y=220)
#
# root.mainloop()


def get_search_link(tag_list):
    tag_id_list = [GAME_TAGS[tag] for tag in tag_list]
    link = f"https://store.steampowered.com/search?tags={','.join(tag_id_list)}&category1=998"
    return link


# if __name__ == '__main__':
#     ui()
