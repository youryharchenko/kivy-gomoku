import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle, Line

from kivy.core.window import Window

Window.clearcolor = (0.85, 0.85, 0.85, 0.5)
Window.borderless = True

class Net:
    def __init__(self):
        pass

    def init(self):
        self.active_slots = [[], [], []]  # free, black, white
    '''
        active_slots[0] = new
        Vector. < Slot > (); // free
        active_slots[1] = new
        Vector. < Slot > (); // black
        active_slots[2] = new
        Vector. < Slot > (); // white

        empty_points = new
        Vector. < Point > ();
        all_slots = new
        Vector. < Slot > ();

        for (var i: int = 0; i < 225; i + +) {
            var
        p:Point = new
        Point(this, Math.floor(i / 15) - 7, i % 15 - 7);
        // trace(i, p.x, p.y);
        all_points[i] = p;
        empty_points.push(p);

        for (var j: int = 0; j < 4; j + +) {
        if (p.is_valid_scp(j))
        {
            var
        s: Slot = new
        Slot(this, p, j);
        all_slots.push(s);
        active_slots[0].push(s);
        }
        }
        }

        for each(var item: Slot in all_slots) {
            item.init();
        }
        '''

class Game:
    def __init__(self, app):
        self.is_play = False
        self.is_run = False
        self.is_busy = False

        self.n_step = 0
        self.mes = ""

        self.app = app
        self.app.status.text = "Press 'New'"

    def play(self):
        self.is_play = True
        self.is_run = False
        self.is_busy = False

        if self.app.mode() == 0:
            self.app.action_step.disabled = False
        else:
            self.app.action_step.disabled = True
            self.app.action_back.disabled = True

        self.app.action_run.disabled = False
        self.app.action_mode.disabled = True

        self.app.desk.draw_init()
        self.app.desk.draw_grid()

        self.app.net.init()

        self.mes = "Start"
        self.n_step = 1
        self.app.net.step(0, 0, 1)
        self.app.status.text = "New game"

        if self.app.mode() == 1:
            self.run(False)

class Desk(Widget):
    def draw_init(self):
        self.canvas.clear()

        self.h = 31
        self.s = 16 * self.h
        self.pady = (Window.height - self.s - self.h * 2) / 2
        self.padx = (Window.width - self.s) / 2
        self.size = (self.s, self.s)
        self.pos = (self.padx, self.h + self.pady)
        self.d = self.h
        self.cx = [self.pos[0] + self.d + i * self.d for i in range(0, 15)]
        self.cy = [self.pos[1] + self.d + i * self.d for i in range(0, 15)]

    def draw_grid(self):

        self.canvas.add(Color(1., 1., 1.))
        self.canvas.add(Rectangle(size=self.size, pos=self.pos))
        self.canvas.add(Color(0., 0., 0.))
        for c in self.cx:
            self.canvas.add(Line(points = [c, self.pos[1] + self.d, c, self.pos[1] + self.size[1] - self.d]))
        for c in self.cy:
            self.canvas.add(Line(points=[self.pos[0] + self.d, c, self.pos[0] + self.size[0] - self.d, c]))



class Gomoku(App):

    def build(self):
        main = GridLayout(cols = 1, rows = 1)

        actions = BoxLayout(orientation='horizontal', pos_hint = {'x': 0}, size_hint_x = 1)
        self.action_new = Button(text = "New",
                            pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None),
                            on_press = lambda x: self.game.play())

        self.action_mode = Button(text="Mode:Black",
                            pos_hint = {'top': 1}, size = (100, 30), size_hint = (None, None),
                            on_release = lambda x: drop_mode.open(x))
        drop_mode = DropDown()
        drop_mode.bind(on_select=lambda instance, x: setattr(self.action_mode, 'text', x))
        mode_on_release = lambda btn: drop_mode.select("Mode:" + btn.text)

        black_mode = Button(text = "Black", size = (100, 30), size_hint = (None, None), on_release=mode_on_release)
        white_mode = Button(text = "White", size=(100, 30), size_hint=(None, None), on_release=mode_on_release)
        manual_mode = Button(text = "Manual", size=(100, 30), size_hint=(None, None), on_release=mode_on_release)
        drop_mode.add_widget(black_mode)
        drop_mode.add_widget(white_mode)
        drop_mode.add_widget(manual_mode)

        self.action_step = Button(text = "Step", pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None))
        self.action_back = Button(text = "Back", pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None))
        self.action_run = Button(text = "Run", pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None))
        self.action_close = Button(text="Close",
                            pos_hint={'top': 1}, size=(70, 30), size_hint=(None, None),
                            on_press = lambda x: Window.close())

        actions.add_widget(self.action_new)
        actions.add_widget(self.action_mode)
        actions.add_widget(self.action_step)
        actions.add_widget(self.action_back)
        actions.add_widget(self.action_run)
        actions.add_widget(self.action_close)

        self.desk = Desk()

        self.status = Label(text = "Ready", pos_hint = {'bottom': 1}, size = (200, 30), size_hint = (None, None), text_size=(180, None))

        vbox = BoxLayout(orientation='vertical', size = main.size, pos_hint = {'x': 0, 'y': 0}, size_hint_x = 1, size_hint_y = 1)
        vbox.add_widget(actions)
        vbox.add_widget(self.desk)
        vbox.add_widget(self.status)
        main.add_widget(vbox)

        self.action_step.disabled = True
        self.action_back.disabled = True
        self.action_run.disabled = True

        self.desk.draw_init()
        self.desk.draw_grid()

        self.game = Game(self)
        self.colors = ([0, 0, 0, 0.5], [1, 1, 1, 0.5])
        self.qsteps = 0
        self.steps = [None] * 225
        self.mode = lambda : {"Mode:Manual":0, "Mode:Black":1, "Mode:White":2}[self.action_mode.text]

        print self.mode()

        self.net = Net()

        return main

if __name__ == '__main__':
    Gomoku().run()


