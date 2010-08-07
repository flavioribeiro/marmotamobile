#encoding: utf-8

import appuifw
import graphics
import e32
import lightblue

IMGS_DIR = "E:\\Marmota\\images\\interface\\"

class Connection(object):

    def __init__(self):
        self.my_socket = lightblue.socket()
        self.connected = False

    def listDevices(self):
        self.devices_available = lightblue.finddevices()
        return self.devices_available

    def connect(self, device):
        try: 
            self.my_socket.connect((device[0], 1))
            appuifw.note(u"Connecting to " + unicode(device[1]))
            self.connected = True
            return True

        except:
            self.connected = False
            return False

    def disconnect(self):
        self.connected = False
        self.my_socket.close()

    def goAhead(self):
        if self.connected: self.my_socket.send("g")

    def turnLeft(self):
        if self.connected: self.my_socket.send("l")

    def turnRight(self):
        if self.connected: self.my_socket.send("r")

    def stop(self):
        if self.connected: self.my_socket.send("s")

class Display(object):

    def __init__(self):
        
        self.left_image = graphics.Image.open(IMGS_DIR + "left.jpg")
        self.right_image = graphics.Image.open(IMGS_DIR + "right.jpg")
        self.front_image = graphics.Image.open(IMGS_DIR + "ahead.jpg")
        self.stop_image = graphics.Image.open(IMGS_DIR + "index.jpg")

        self.image_buffer = graphics.Image.new((640, 360))
        
        self.stop()
        self.canvas = appuifw.Canvas(redraw_callback=self.handleRedraw)
        
        appuifw.app.screen          = 'large'
        appuifw.app.directional_pad = False
        appuifw.app.orientation     = 'landscape'
        appuifw.app.body            = self.canvas

    def handleRedraw(self, rect):
        if self.image_buffer:
            self.canvas.blit(self.image_buffer)
        
    def goAhead(self):
        self.image_buffer.blit(self.front_image)

    def turnLeft(self):
        self.image_buffer.blit(self.left_image)

    def turnRight(self):
        self.image_buffer.blit(self.right_image)

    def stop(self):
        self.image_buffer.blit(self.stop_image)

    def about(self):
        appuifw.note(u"Marmota - Car Controlled by Phone. More info: http://marmota.mobi", "conf")


class Main(object):
    def __init__(self):
        self.app_lock = e32.Ao_lock()
        self.display = Display()
        self.is_running = True
        appuifw.app.exit_key_handler = self.quit
        
    def quit(self):
        appuifw.note(u"Exiting...", "info")
        self.app_lock.signal()
        self.is_running = False

    def startApp(self):
        self.display.stop()
        self.app_lock.wait()

if __name__ == "__main__": 
    main = Main()
    main.startApp()
