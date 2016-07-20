import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle, Line, Ellipse

from kivy.core.window import Window

import random

Window.clearcolor = (0.85, 0.85, 0.85, 0.5)
Window.borderless = True

class Point:
    def __init__(self, net, x, y):
        self.net = net
        self.x = x
        self.y = y
        self.slots = []
        self.r = [0, 0, 0]
        self.s = 0

    def is_valid_scp(self, d):
        x = self.x - 7
        y = self.y - 7
    # 0 - vert, 1 - horiz, 2 - up, 3 - down
        if d == 0 and y > -6 and y < 6:
            return True
        if d == 1 and x > -6 and x < 6:
            return True
        if d == 2 and (x > -6 and y < 6) and (x < 6 and y > -6):
            return True
        if d == 3 and (x > -6 and y > -6) and (x < 6 and y < 6):
            return True
        return False

    def add_slot(self, s):
        self.slots.append(s)
        self.r[s.s] += 1

    def to_string(self):
        return "x:{0},y:{1};".format(self.x, self.y)

class Slot:
    def __init__(self, net, scp, d):
        self.net = net
        self.scp = scp
        self.d = d
        self.points = [None] * 5
        self.r = 0
        self.s = 0

    def init(self):
        #print "Init Slot: d: {0}, scp: {1}".format(self.d, self.scp.to_string())
        self.points[2] = self.net.get_point(self.scp.x, self.scp.y)

        if self.d == 0:
            self.points[0] = self.net.get_point(self.scp.x, self.scp.y - 2)
            self.points[1] = self.net.get_point(self.scp.x, self.scp.y - 1)
            self.points[3] = self.net.get_point(self.scp.x, self.scp.y + 1)
            self.points[4] = self.net.get_point(self.scp.x, self.scp.y + 2)
        elif self.d == 1:
            self.points[0] = self.net.get_point(self.scp.x - 2, self.scp.y)
            self.points[1] = self.net.get_point(self.scp.x - 1, self.scp.y)
            self.points[3] = self.net.get_point(self.scp.x + 1, self.scp.y)
            self.points[4] = self.net.get_point(self.scp.x + 2, self.scp.y)
        elif self.d == 2:
            self.points[0] = self.net.get_point(self.scp.x - 2, self.scp.y - 2)
            self.points[1] = self.net.get_point(self.scp.x - 1, self.scp.y - 1)
            self.points[3] = self.net.get_point(self.scp.x + 1, self.scp.y + 1)
            self.points[4] = self.net.get_point(self.scp.x + 2, self.scp.y + 2)
        elif self.d == 3:
            self.points[0] = self.net.get_point(self.scp.x - 2, self.scp.y + 2)
            self.points[1] = self.net.get_point(self.scp.x - 1, self.scp.y + 1)
            self.points[3] = self.net.get_point(self.scp.x + 1, self.scp.y - 1)
            self.points[4] = self.net.get_point(self.scp.x + 2, self.scp.y - 2)

        for i in range(0, 5):
            self.points[i].add_slot(self)

class Net:
    def __init__(self):
        pass

    def init(self):
        self.all_slots = []
        self.active_slots = [[], [], []]  # free, black, white

        self.all_points = [Point(self, int(i / 15), i % 15 ) for i in range(0, 225)]
        self.empty_points = self.all_points[:]

        for p in self.all_points:
            for d in range(0, 4):
                if p.is_valid_scp(d):
                    s = Slot(self, p, d)
                    self.all_slots.append(s)

        self.active_slots[0] = self.all_slots[:]
        for s in self.all_slots:
            s.init()

    def step(self, x, y, c):
        p = self.get_point(x, y)
        p.s = c
        self.empty_points.remove(p)

        for s in p.slots:
            if s.s == 0:
                p.r[0] -= 1
                p.r[c] += 1
                s.s = c
                s.r = 1
                self.active_slots[0].remove(s)
                self.active_slots[c].append(s)
            elif s.s == c:
                p.r[c] += 1
                s.r += 1
            elif s.s != 3:
                p.r[c] -= 1
                self.active_slots[s.s].remove(s)
                s.s = 3

    def get_point(self, x, y):
        #print (x, y)
        return self.all_points[x * 15 + y]


class Game:
    def __init__(self, app):
        self.is_play = False
        self.is_run = False
        self.is_busy = False

        self.n_step = 0
        self.mes = ""

        self.app = app
        self.name_c = ["", "Black", "White"]

    def play(self):
        self.app.desk.draw_init()
        self.app.desk.draw_grid()

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

        self.app.net.init()

        self.app.qsteps = 0
        self.add_step(7, 7, 0, "Start")

        self.mes = "Start"
        self.n_step = 1
        self.app.net.step(7, 7, 1)
        self.app.status.text = "New game"

        if self.app.mode() == 1:
            self.run(False)

    def run(self, r):
        if self.is_play:
            self.app.status.text = "Thinking..."
            self.is_busy = True
            self.is_run = r
            self.go(True, 0, 0)
            self.is_busy = False

    def back(self):
        self.is_play = True
        self.is_busy = True

        self.replay(1)

        self.is_busy = False

        self.app.action_run.disabled = False
        self.app.action_step.disabled = False

    def replay(self, k):
        n = self.n_step - k

        if n > 0:
            self.app.net.init()
            self.app.desk.draw_init()
            self.app.desk.draw_grid()
            #self.app.desk_init()
            self.n_step = 1
            self.app.net.step(7, 7, 1)
            self.app.qsteps = 0
            self.add_step(7, 7, 0, "")
            self.is_busy = False
            self.is_play = True
            self.is_run = False

            self.app.status.text = "Start"

        if n > 1:
            for i in range(1, n):
                st = self.app.steps[i]
                #self.app.steps[i] = None
                self.replay_step(st["x"], st["y"], st["mes"])

            self.app.status.text = "Step {0} -> {1}".format(self.n_step, st["mes"])

    def replay_step(self, x, y, mes):
        self.n_step += 1

        self.app.net.step(x, y, 2 - self.n_step % 2)
        self.add_step(x, y, 1 - self.n_step % 2, mes)
        return self.n_step

    def go(self, auto, x, y):
        ret = 0
        if auto:
            ret = self.next_step()
        else:
            ret = self.manual_step(x, y)

        self.app.status.text = "Finish! -> {0}".format(self.mes) if ret < 0 else "Step {0} -> {1}".format(ret, self.mes)

        if self.app.mode() == 0:
            self.app.action_back.disabled = False

        if ret < 0 or ret > 224:
            self.app.action_run.disabled = True
            self.app.action_step.disabled = True
            self.app.action_mode.disabled = False

            self.is_run = False
            self.is_play = False

        elif not auto and self.app.mode() > 0:
            self.go(True, 7, 7)
        elif self.is_run:
            self.go(True, 7, 7)

    def next_step(self):
        self.n_step += 1

        if self.check_win(3 - (2 - self.n_step % 2)) or self.check_draw():
            return -1
        else:
            p = self.calc_point(2 - self.n_step % 2)
            self.app.net.step(p.x, p.y, 2 - self.n_step % 2)
            self.add_step(p.x, p.y, 1 - self.n_step % 2, self.mes)
            return self.n_step

    def manual_step(self, x, y):
        self.n_step += 1
        if self.check_win(3 - (2 - self.n_step % 2)) or self.check_draw():
            return -1
        else:
            self.app.net.step(x, y, 2 - self.n_step % 2)
            self.mes = "{0}  :: manual ({1},{2})".format(self.name_c[2 - self.n_step % 2], x, y )
            self.add_step(x, y, 1 - self.n_step % 2, self.mes)
            return self.n_step

    def check_win(self, c):
        for s in self.app.net.active_slots[c]:
            if s.r == 5:
                self.mes = self.name_c[c] + " :: win!!!"
                return True
        return False

    def check_draw(self):
        if len(self.app.net.active_slots[0]) == 0 and \
                len(self.app.net.active_slots[1]) == 0 and \
                len(self.app.net.active_slots[2]) == 0:
            self.mes = " draw :("
            return True
        else:
            return False

    def calc_point(self, c):

        self.mes = self.name_c[c] + " :: auto :: "

        ret = self.find_slot_4(c)
        if len(ret) == 0:
            ret = self.find_slot_4(3 - c)
        if len(ret) == 0:
            ret = self.find_point_x(c, 2, 1)

        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 2, 1)
        if len(ret) == 0:

            ret = self.find_point_x(c, 1, 5)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 1, 5)
        if len(ret) == 0:

            ret = self.find_point_x(c, 1, 4)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 1, 4)

        if len(ret) == 0:
            ret = self.find_point_x(c, 1, 3)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 1, 3)

        if len(ret) == 0:
            ret = self.find_point_x(c, 1, 2)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 1, 2)

        if len(ret) == 0:
            ret = self.find_point_x(c, 1, 1)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 1, 1)

        if len(ret) == 0:
            ret = self.find_point_x(c, 0, 10)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 0, 10)

        if len(ret) == 0:
            ret = self.find_point_x(c, 0, 9)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 0, 9)

        if len(ret) == 0:
            ret = self.find_point_x(c, 0, 8)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 0, 8)

        if len(ret) == 0:
            ret = self.find_point_x(c, 0, 7)
        if len(ret) == 0:
            ret = self.find_point_x(3 - c, 0, 7)

        if len(ret) == 0:
            ret = self.calc_point_max_rate(c)

        #mes = ret[0].m;
		#return ret[0].p;
		#i = int(Math.random() * ret.length)
        o = random.choice(ret)
        self.mes = o["m"]
        return o["p"]

    def find_slot_4(self, c):
        ret = []
        m = 0
        for s in self.app.net.active_slots[c]:
            if s.r == 4:
                for p in s.points:
                    if p.s == 0:
                        m = "{0} {1} :: find_slot_4 -> -> ({2},{3})".format(self.mes, self.name_c[c], p.x, p.y)
                        ret.append({"p": p, "m": m})
        return ret

    def find_point_x(self, c, r, b):
        ret = []
        m = ""
        for p in self.app.net.empty_points:
            i = 0
            for s in p.slots:
                if s.s == c and s.r > r:
                    i += 1
            if i > b:
                m = "{0} {1} :: point_max_rate({2},{3}) -> ({4},{5})".format(self.mes, self.name_c[c], r, b, p.x, p.y)
                ret.append({"p": p, "m": m})

        return ret

    def calc_point_max_rate(self, c):
        ret = []
        m = ""
        r = -1
        d = 0
        i = 0

        for p in self.app.net.empty_points:
            d = 0
            for s in p.slots:
                if s.s == 0:
                    d += 1
                elif s.s == c:
                    d += (1 + s.r) * (1 + s.r)
                elif s.s != 3:
                    d += (1 + s.r) * (1 + s.r)

            if d > r:
                i = 1
                r = d
                ret = []
                m = "{0} {1} :: point_max_rate({2},{3}) -> ({4},{5})".format(self.mes, self.name_c[c], i, r, p.x, p.y)
                ret.append({"p": p, "m": m})
            elif d == r:
                i += 1
                m = "{0} {1} :: point_max_rate({2},{3}) -> ({4},{5})".format(self.mes, self.name_c[c], i, r, p.x, p.y)
                ret.append({"p": p, "m": m})

        return ret

    def add_step(self, x, y, c, mes):
        self.app.steps[self.app.qsteps] = {"x": x, "y": y, "mes": mes}
        self.app.qsteps += 1
        self.app.desk.draw_step(x, y, self.app.colors[c])

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

    def draw_step(self, x, y, c):
        self.canvas.add(Color(c[0], c[1], c[2]))
        self.canvas.add(Ellipse(pos = [self.cx[x] - self.d/2, self.cy[y] - self.d/2], size = [self.d, self.d]))
        self.canvas.add(Color(0., 0., 0.))
        self.canvas.add(Line(circle = (self.cx[x], self.cy[y], self.d/2)))

    def on_touch_up(self, touch):
        print "Touch Up: {0}, {1}".format(touch.pos[0], touch.pos[1])
        if self.app.game.is_play and not self.app.game.is_run and not self.app.game.is_busy:
            x, y = self.get_dc(touch.pos[0], touch.pos[1])
            if not x is None and not y is None and self.app.net.get_point(x, y).s == 0:
                print "Manual step: {0}, {1}".format(x, y)
                self.app.game.go(False, x, y)

    def get_dc(self, px, py):
        x = None
        for i in range(0, 15):
            if px < self.cx[i] + self.d / 2 and px > self.cx[i] - self.d / 2:
                x = i
                break

        y = None
        for j in range(0, 15):
            if py < self.cy[j] + self.d / 2 and py > self.cy[j] - self.d / 2:
                y = j
                break

        return x, y


class Gomoku(App):

    def build(self):
        self.game = Game(self)
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

        self.action_step = Button(text = "Step",
                            pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None),
                            on_press = lambda x: self.game.run(False))

        self.action_back = Button(text = "Back",
                            pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None),
                            on_press=lambda x: self.game.back())

        self.action_run = Button(text = "Run",
                            pos_hint = {'top': 1}, size = (70, 30), size_hint = (None, None),
                            on_press=lambda x: self.game.run(True))
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
        self.desk.app = self

        self.status = Label(text = "Ready", pos_hint = {'bottom': 1}, size = (500, 30), size_hint = (None, None), text_size=(500, None))

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

        self.colors = ([0, 0, 0, 0.5], [1, 1, 1, 0.5])
        self.qsteps = 0
        self.steps = [None] * 225
        self.mode = lambda : {"Mode:Manual":0, "Mode:Black":1, "Mode:White":2}[self.action_mode.text]

        print self.mode()

        self.net = Net()
        self.status.text = "Press 'New'"
        return main






if __name__ == '__main__':
    Gomoku().run()


