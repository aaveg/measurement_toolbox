import tkinter as tk
import math

click_origin = [0,0]

def click(event):
    global click_origin
    click_origin = [event.x,event.y]

def drag(event,prot):
    global click_origin

    x, y = event.x, event.y
    x0, y0 = click_origin
    click_origin = [x, y]
    dx, dy = x-x0, y-y0
    prot.move(dx,dy)

def scale(event,prot):
    global click_origin
    x, y = event.x, event.y
    x0, y0 = click_origin
    x, y = x - x0, y - y0
    prot.scale(x)

def adj_a1(event,prot):
    global click_origin
    x, y = event.x, event.y
    prot.adj_a1(x,y)

def adj_a2(event,prot):
    global click_origin
    x, y = event.x, event.y
    prot.adj_a2(x,y)


def fullscreen(event):
    global root
    if event.char == 'q':
        root.attributes('-fullscreen', 0)

class protractor():
    def __init__(self,canvas):
        self.coord = [50, 50, 200, 200]
        a, b, c, d = self.coord
        self.text_coord = [(a+c)//2, (b+d)//2-10]
        self.h1_coord = [(a+c)//2, (b+d)//2, c+20, (b+d)//2]
        self.h2_coord = [(a+c)//2, (b+d)//2, (a+c)//2, b-20]

        self.canvas = canvas
        self.a0 = 0
        self.a = 90
        self.arc = canvas.create_arc(self.coord, start=self.a0, extent=self.a, fill="red")
        self.disp = canvas.create_text(self.text_coord, text=str(self.a - self.a0))
        self.hand1 = canvas.create_line(self.h1_coord, fill="blue")
        self.hand2 = canvas.create_line(self.h2_coord, fill="blue")

        self.cir1 = canvas.create_oval([c+20-5, (b+d)//2-5, c+20+5, (b+d)//2+5], fill ='yellow')
        self.cir2 = canvas.create_oval([(a+c)//2-5, b-20-5, (a+c)//2+5, b-20+5], fill='yellow')
        self.init_keybinds()

    def init_keybinds(self):
        self.canvas.tag_bind(self.arc,'<Button-1>',click)
        self.canvas.tag_bind(self.arc,'<B1-Motion>', lambda event: drag(event, self))
        self.canvas.tag_bind(self.cir1,'<B1-Motion>', lambda event: adj_a1(event, self))
        self.canvas.tag_bind(self.cir2,'<B1-Motion>', lambda event: adj_a2(event, self))

    def adj_a1(self,x,y):
        self.canvas.coords(self.cir1, [x - 5, y - 5, x + 5, y + 5])
        self.canvas.coords(self.hand1, self.h1_coord[0:2]+[x, y])
        a1 = -math.degrees(math.atan2(y - self.h1_coord[1], x - self.h1_coord[0]))
        a2 = -math.degrees(math.atan2(self.h2_coord[3] - self.h2_coord[1], self.h2_coord[2] - self.h2_coord[0]))
        self.canvas.itemconfig(self.arc, start=a1, extent=a2 - a1)
        self.canvas.itemconfig(self.disp, text=str(abs(round(a2 - a1,3))))
        self.h1_coord = self.canvas.coords(self.hand1)

    def adj_a2(self,x,y):
        self.canvas.coords(self.cir2, [x - 5, y - 5, x + 5, y + 5])
        self.canvas.coords(self.hand2, self.h2_coord[0:2]+[x, y])
        a1 = -math.degrees(math.atan2(self.h1_coord[3]-self.h1_coord[1], self.h1_coord[2]-self.h1_coord[0]))
        a2 = -math.degrees(math.atan2(y-self.h2_coord[1], x-self.h2_coord[0]))
        self.canvas.itemconfig(self.arc, start = a1, extent= a2-a1)
        self.canvas.itemconfig(self.disp, text=str(abs(round(a2 - a1,3))))
        self.h2_coord = self.canvas.coords(self.hand2)

    def move(self, x, y):
        self.canvas.move(self.arc, x, y)
        self.canvas.move(self.disp, x, y)
        self.canvas.move(self.hand1, x, y)
        self.canvas.move(self.cir1, x, y)
        self.canvas.move(self.hand2, x, y)
        self.canvas.move(self.cir2, x, y)

        self.coord = self.canvas.coords(self.arc)
        self.text_coord = self.canvas.coords(self.disp)
        self.h1_coord = self.canvas.coords(self.hand1)
        self.h2_coord = self.canvas.coords(self.hand2)


    def scale(self, frac):
        a,b,c,d = self.coord
        coord = [a-frac,b-frac,c+frac,d+frac]
        self.canvas.coords(self.arc,coord)


class measure_app():
    def __init__(self,master):
        self.master = master
        self.create_protractor()

    def create_protractor(self):
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-transparentcolor", "white")
        self.master.attributes('-fullscreen',1)
        self.master.wm_attributes("-alpha", 0.7)

        WIDTH = self.master.winfo_width()
        HEIGHT = self.master.winfo_height()
        print(self.master.winfo_width(),self.master.winfo_height())
        canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        prot = protractor(canvas)
        canvas.pack()
        self.master.bind('<Key>',fullscreen)

    def run(self):
        self.master.mainloop()


root = tk.Tk()
app = measure_app(root)
app.run()
