#usage: kivy main.py model.obj ref_img

#layout: reference image; 3d viewer; texture viewer

'''
operation: 
    r-rotation;
    s-scale;
    c-checkerboard on/off

'''

import math
import sys
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from objloader import ObjFile
from kivy.logger import Logger
from kivy.vector import Vector
from kivy.core.image import Image
from kivy.uix.label import Label
from kivy.config import Config

from PIL import Image as pilimage

class rimgv(Widget):
    def __init__(self, **kwargs):

        super(rimgv, self).__init__(**kwargs)
        refimg = pilimage.open(sys.argv[2])
        if refimg.size[0]>refimg.size[1]:
            newsize=[450,int(450.0/float(refimg.size[0])*float(refimg.size[1]))]
        else:
            newsize=[int(450.0/float(refimg.size[1])*float(refimg.size[0])),450]
        
        with self.canvas:
            Color(1,1,1,1)
            self.rect = Rectangle(source=sys.argv[2],size=newsize,pos=[250-int(newsize[0]/2),300-int(newsize[1]/2)])

    def on_touch_down(self, touch):
        idle = 0


class meshv(Widget):

    def __init__(self, **kwargs):

        #self.reset_gl_context = True
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        self.scene = ObjFile(resource_find(sys.argv[1]))
        #print self.scene.mtl
        super(meshv, self).__init__(**kwargs)
 
        self.checkerboard_statue = 0

        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)

        self.camera_loc = [0,1,0]
        self.camera_up = [0,0,1]
        self.camera_r = 2
        Clock.schedule_once(self.update_glsl, 1 / 60.)    
        
 
        self._touches = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        asp = 15/5.5
        proj = Matrix()
        mat = Matrix()
        mat = mat.look_at(self.camera_loc[0]*self.camera_r, self.camera_loc[1]*self.camera_r, self.camera_loc[2]*self.camera_r, 0,0,0, self.camera_up[0],self.camera_up[1],self.camera_up[2])
        proj = proj.view_clip(-asp*0.5,asp*0.5, -0.5, 0.5, 1, 5, 50)
        
        self.canvas['projection_mat'] = proj
        self.canvas['modelview_mat'] = mat

    def setup_scene(self):
        #texture = Image('./model/orion.png').texture
        texture_ = Image('checkerboard.jpg').texture

        Color(1, 1, 1, 1)
        for id in range(0,len(self.scene.objects)):
            PushMatrix()
            #Translate(0, 0, -4)
            self.rotx = Rotate(0, 0, 1, 0)
            self.roty = Rotate(0, 1, 0, 0)
            self.scale = Scale(2)
            m = self.scene.objects.values()[id]
            #print self.scene.mtl
            #print m.vertex_format
            UpdateNormalMatrix() 
            if os.path.isfile(os.path.split(sys.argv[1])[0]+'/texture/'+self.scene.material.values()[id]+'.png'):
                texture_id = Image(os.path.split(sys.argv[1])[0]+'/texture/'+self.scene.material.values()[id]+'.png').texture
            else:
                texture_id = texture_

            if self.checkerboard_statue == 0: 
                texture = texture_id
            else:
                texture = texture_

            self.mesh = Mesh(
                vertices=m.vertices,
                indices=m.indices,
                fmt=m.vertex_format,
                mode='triangles',
                texture=texture,
            )
            PopMatrix()

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx/self.width)*360
        y_angle = -1*(touch.dy/self.height)*360
        return x_angle, y_angle
    
    def on_touch_down(self, touch):
        #super(Viewer, self).on_touch_down(touch)
        touch.grab(self)
        #print touch.x,touch.y
        self._touches.append(touch)
        
    def on_touch_up(self, touch):
        touch.ungrab(self)
        if len(self._touches)>0:
            self._touches.remove(touch)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 's':
            self._keyboard = 's'
            print 'scale_mode'
        if keycode[1] == 'r':
            self._keyboard = 'r'
            print 'rotate_mode'
        if keycode[1] == 'c':
            self.checkerboard_statue = 1 - self.checkerboard_statue
            self.redraw() 
            print 'checkerboard on/off'

    def redraw(self):
        self.canvas.clear()
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)         

    def on_touch_move(self, touch): 
        #Logger.debug("dx: %s, dy: %s. Widget: (%s, %s)" % (touch.dx, touch.dy, self.width, self.height))
        #self.update_glsl()
        #print self._touches
        if touch in self._touches and touch.grab_current == self:
            
            tup=[self.camera_up[0],self.camera_up[1],self.camera_up[2]]
            tfo=[-self.camera_loc[0],-self.camera_loc[1],-self.camera_loc[2]]
            tri=[tup[1]*tfo[2]-tup[2]*tfo[1],tup[2]*tfo[0]-tup[0]*tfo[2],tup[0]*tfo[1]-tup[1]*tfo[0]]

            if self._keyboard == 'r':
                # here do just rotation
                ay, ax = self.define_rotate_angle(touch)
                
                #self.rotx.angle += ax
                #self.roty.angle += ay
                self.camera_loc[0] += tup[0]*ax+tri[0]*ay 
                self.camera_loc[1] += tup[1]*ax+tri[1]*ay
                self.camera_loc[2] += tup[2]*ax+tri[2]*ay
                nl = pow(self.camera_loc[0]*self.camera_loc[0]+self.camera_loc[1]*self.camera_loc[1]+self.camera_loc[2]*self.camera_loc[2],0.5)
                self.camera_loc[0] = self.camera_loc[0]/nl
                self.camera_loc[1] = self.camera_loc[1]/nl
                self.camera_loc[2] = self.camera_loc[2]/nl
                tfo=[-self.camera_loc[0],-self.camera_loc[1],-self.camera_loc[2]]
                lm=-(tup[0]*tfo[0]+tup[1]*tfo[1]+tup[2]*tfo[2])/pow(tfo[0]*tfo[0]+tfo[1]*tfo[1]+tfo[2]*tfo[2],0.5)
                self.camera_up[0]=tup[0]+lm*tfo[0]
                self.camera_up[1]=tup[1]+lm*tfo[1]
                self.camera_up[2]=tup[2]+lm*tfo[2]


            elif self._keyboard == 's': # scaling here
                #use two touches to determine do we need scal

                SCALE_FACTOR = 0.2
                
                if touch.dx > 0:
                    scale = -1*SCALE_FACTOR
                    Logger.debug('Scale up')
                elif touch.dx == 0:
                    scale = 0
                else:
                    scale = SCALE_FACTOR
                    Logger.debug('Scale down')
                
                if scale:
                    self.camera_r += scale*self.camera_r/5
                    #print scale,self.camera_r
            self.update_glsl()


class ViewerApp(App):
    def build(self):

        if True: #retina screen?
            rtscreen = 2
        else:
            rtscreen = 1
        Window.size=(1500/rtscreen,550/rtscreen)
      
        parentlayout = BoxLayout()
        
        imgwidget = FloatLayout(size = (500,550), pos = (0,0))
        viewerwidget = FloatLayout(size = (500,550), pos = (500,0))
        texturewidget = FloatLayout(size = (500,550), pos = (1000,0))

        myviewer = meshv()
        viewerwidget.add_widget(myviewer)

        myimg = rimgv()
        imgwidget.add_widget(myimg)

        with imgwidget.canvas.before:
            Color(1, 0, 0, 0.6) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=imgwidget.size,pos=imgwidget.pos)
            Color(1,1,1,1)
            self.text = Label(text='Reference Image',pos=(200,-10),bold='True',font_size='20sp')

        with viewerwidget.canvas.before:
            Color(0, 1, 0, 0.6) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=viewerwidget.size,pos=viewerwidget.pos)
            Color(1,1,1,1)
            self.text = Label(text='3D View',pos=(700,-10),bold='True',font_size='20sp')

        with texturewidget.canvas.before:
            Color(0, 0, 1, 0.6) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=texturewidget.size,pos=texturewidget.pos)
            Color(1,1,1,1)
            self.text = Label(text='Texture Iamge',pos=(1200,-10),bold='True',font_size='20sp')

        parentlayout.add_widget(imgwidget, index=1)
        parentlayout.add_widget(viewerwidget, index=0)
        parentlayout.add_widget(texturewidget, index=2)

        '''
        def btn1_callback(instance):
            myviewer.convert_checkerboard()

        btn1 = Button(text='Checkerboard',size=(100,200))
        btn1.bind(on_press=btn1_callback)
        parentlayout.add_widget(btn1)
        '''
        return parentlayout


if __name__ == "__main__":
    ViewerApp().run()
