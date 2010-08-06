#encoding: utf-8

import appuifw
import graphics
import e32

IMGS_DIR = "E:\\Marmota\\images\\interface\\"

class Connection(object):

    def __init__(self):
        pass
     
    def listDevices(self):
        pass
   
    def connect(self, device):
        pass

    def disconnect(self):
        pass
        
    def goAhead(self):
        pass
        
    def turnLeft(self):
        pass
        
    def turnRight(self):
        pass
        
    def stop(self):
        pass

class Display(object):

    def __init__(self):
        
        self.left_image = graphics.Image.open(IMGS_DIR + "left.jpg")
        self.right_image = graphics.Image.open(IMGS_DIR + "right.jpg")
        self.front_image = graphics.Image.open(IMGS_DIR + "ahead.jpg")
        self.stop_image = graphics.Image.open(IMGS_DIR + "index.jpg")

        self.image_buffer = graphics.Image.new((640, 360))
        
        self.stop()
        self.canvas = appuifw.Canvas(redraw_callback=self.handleRedraw)
        
        appuifw.app.screen          = 'full'
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
