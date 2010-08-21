#encoding: utf-8
#
# Marmota v1.1 - Making Arduino and Mobile Devices Talk
# WebSite: http://www.marmota.mobi
#
# Small Description:
#   This version is dedicated to mobile devices with Symbian S60v5. 
#   Only tested on Nokia 5800 XM device.
#
#   More details may be found on docs/ path.
# 
# Created on: August 05, 2010.
# 
# Main Developer:
#   Artur Santos         (ar7hur.santos@gmail.com)
#   Roberto Teixeira    (rtcf85@gmail.com)
#   Rafael Trindade        (rafaeltscs@gmail.com)
#   Rubean Santos        (rubeansite@gmail.com)
#

import appuifw
import graphics
import e32
import lightblue
import key_codes
import globalui

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
            self.my_socket.connect((device[0], 11))
            appuifw.note(u"Connecting to " + unicode(device[1]))
            self.connected = True
            return True

        except:
            self.connected = False
            return False

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.my_socket.close()

    def goAhead(self):
        if self.connected: self.my_socket.send("G")

    def turnLeft(self):
        if self.connected: self.my_socket.send("L")

    def turnRight(self):
        if self.connected: self.my_socket.send("R")

    def stop(self):
        if self.connected: self.my_socket.send("S")

class Display(object):

    def __init__(self,connection):
        
        self.connection = connection
        
        self.left_image  = graphics.Image.open(IMGS_DIR + "left.jpg")
        self.right_image = graphics.Image.open(IMGS_DIR + "right.jpg")
        self.front_image = graphics.Image.open(IMGS_DIR + "ahead.jpg")
        self.stop_image  = graphics.Image.open(IMGS_DIR + "index.jpg")
        self.bt_image    = graphics.Image.open(IMGS_DIR + "bt.png")

        self.image_buffer = graphics.Image.new((640, 360))
        
        self.canvas = appuifw.Canvas(redraw_callback=self.handleRedraw)
        self.stop()
        
        appuifw.app.screen          = 'full'
        appuifw.app.directional_pad = False
        appuifw.app.orientation     = 'landscape'
        appuifw.app.body            = self.canvas

    def handleRedraw(self, rect):
        if self.image_buffer:
            self.canvas.blit(self.image_buffer)
        
    def goAhead(self):
        if self.connection.connected:
            self.front_image.blit(self.bt_image,target=(60,8), source=((0,0),(20,28)))
        else:
            self.front_image.blit(self.bt_image,target=(60,8), source=((20,0),(40,28)))
        self.image_buffer.blit(self.front_image)
        self.handleRedraw(self.image_buffer)

    def turnLeft(self):
        if self.connection.connected:
            self.left_image.blit(self.bt_image,target=(60,8), source=((0,0),(20,28)))
        else:
            self.left_image.blit(self.bt_image,target=(60,8), source=((20,0),(40,28)))
        self.image_buffer.blit(self.left_image)
        self.handleRedraw(self.image_buffer)

    def turnRight(self):
        if self.connection.connected:
            self.right_image.blit(self.bt_image,target=(60,8), source=((0,0),(20,28)))
        else:
            self.right_image.blit(self.bt_image,target=(60,8), source=((20,0),(40,28)))    
        self.image_buffer.blit(self.right_image)
        self.handleRedraw(self.image_buffer)

    def stop(self):
        if self.connection.connected:
            self.stop_image.blit(self.bt_image,target=(60,8), source=((0,0),(20,28)))
        else:
            self.stop_image.blit(self.bt_image,target=(60,8), source=((20,0),(40,28)))
        self.image_buffer.blit(self.stop_image)
        self.handleRedraw(self.image_buffer)

    def about(self):
        appuifw.note(u"Marmota - Car Controlled by Phone. More info: http://marmota.mobi", "conf")


class Main(object):
    
    def __init__(self):
        self.app_lock                = e32.Ao_lock()
        self.connection              = Connection()
        self.display                 = Display(self.connection)
        appuifw.app.exit_key_handler = self.quit
        self.startConnection()
        self.initBinds()
    
    def initBinds(self):
        total_x, total_y = self.display.canvas.size
        y1 = total_y/3
        y2 = y1 * 2
        y3 = y1 * 3
        
        x1 = total_x/3
        x2 = x1 * 2
        x3 = x1 * 3
        
        largura_menu = 50
        
        self.display.canvas.bind(key_codes.EButton1Down, self.turnLeft, ((0,largura_menu), (x1,total_y)))
        self.display.canvas.bind(key_codes.EButton1Down, self.goAhead, ((x1,largura_menu), (x2,total_y)))
        self.display.canvas.bind(key_codes.EButton1Down, self.turnRight, ((x2,largura_menu), (x3,total_y)))
        self.display.canvas.bind(key_codes.EButton1Up,   self.stop)
        self.display.canvas.bind(key_codes.EButton1Down, self.quit, ((total_x - largura_menu, 0), (total_x,largura_menu)))
        self.display.canvas.bind(key_codes.EButton1Down, self.about, ((0, 0), (largura_menu,largura_menu)))
        self.display.canvas.bind(key_codes.EButton1Down, self.reconnect, ((50,0),(90,44)))
        
            
    def quit(self,event):
        if globalui.global_query(u"Are you sure?") == 1:
            self.connection.disconnect()
            self.app_lock.signal()

    def startApp(self):
        self.display.stop()
        self.app_lock.wait()
        
    def goAhead(self,event):
        self.display.goAhead()
        self.connection.goAhead()
        
    def turnLeft(self,event):
        self.display.turnLeft()
        self.connection.turnLeft()

    def turnRight(self,event):
        self.display.turnRight()
        self.connection.turnRight()

    def stop(self,event):
        self.display.stop()
        self.connection.stop()
        
    def about(self,event):
        self.display.about()
        
    def startConnection(self):
        appuifw.note(u"Please wait, scanning bluetooth devices..", "info")

        self.devices_list = self.connection.listDevices()
        
        if self.devices_list:
            self.device_names = [device[1] for device in self.devices_list]
            
            self.choice = appuifw.popup_menu( self.device_names )
    
            if self.choice != None:
                try:
                    if self.connection.connect( self.devices_list[self.choice] ): 
                        appuifw.note(u"Connected!", "conf")
                except: 
                    appuifw.note(u"Connection Error!", "error")
        else:
            appuifw.note(u"No bluetooth devices found!", "error")
     
    def reconnect(self,event):
        self.startConnection()
   
if __name__ == "__main__": 
    main = Main()
    main.startApp()