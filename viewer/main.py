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
import shutil

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
from kivy.uix.dropdown import DropDown
from random import randint
from kivy.cache import Cache

from PIL import Image as pilimage

global is_retina_screen
is_retina_screen=False


class rimgv(FloatLayout):
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

class meshv(FloatLayout):

    def __init__(self, **kwargs):

        #self.canvas=InstructionGroup()
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        self.scene = ObjFile(resource_find(sys.argv[1]))
        #print self.scene.mtl
        super(meshv, self).__init__(**kwargs)
 
        #self.add_widget(Sprite(
        #    size=(200,200),
        #    center=(1000,200)
        #))
        global texture_id_
        texture_id_ = {}
        global global_texture_filename
        global_texture_filename = 'checkerboard.jpg'
        global global_uv_filename
        global_uv_filename = 'checkerboard.jpg'

        for id in range(0,len(self.scene.objects)):
            shutil.copyfile(os.path.split(sys.argv[1])[0]+'/texture/'+self.scene.material.values()[id]+'.png',os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[id]+'.png')

        self.checkerboard_statue = 0

        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            #Color(0, 1, 1, 0.6) 
            #self.rect = Rectangle(size=self.size,pos=self.pos)            
            self.cb = Callback(self.reset_gl_context)

        self.camera_loc = [0,1,0]
        self.camera_up = [0,0,1]
        self.camera_r = 2
        Clock.schedule_once(self.update_glsl, 1 / 60.)    


        self._touches = []
        self.texture_id = 0
        #self.btn_next_texture()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        #self.canvas.add(tmpview)

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
        proj = proj.view_clip(-asp*0.5,asp*0.5, -0.5, 0.5, 1, 10, 50)
        
        self.canvas['projection_mat'] = proj
        self.canvas['modelview_mat'] = mat

    def setup_scene(self):
        #texture = Image('./model/orion.png').texture
        texture_ = Image('checkerboard.jpg')#.texture

        Color(1, 1, 1, 1)
        global texture_id_
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
                texture_id = Image(os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[id]+'.png')#.texture
                texture_id_[id] = texture_id
                #texture_id.nocache = True
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
                texture=texture.texture,
            )
            PopMatrix()

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx/self.width)*360
        y_angle = -1*(touch.dy/self.height)*360
        return x_angle, y_angle
    
    def on_touch_down(self, touch):
        #super(Viewer, self).on_touch_down(touch)
        touch.grab(self)
        if touch.x>=1010 and touch.x<=1490 and touch.y>=60 and touch.y<=540:
            #Cache.remove(os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[self.texture_id]+'.png')
            
            timg = pilimage.open(os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[self.texture_id]+'.png')
            tpx = timg.load()
            ranr = randint(0,256)
            rang = randint(0,256)
            ranb = randint(0,256)
            for i in range(int((touch.x-1010)/480*timg.size[0])-9,int((touch.x-1010)/480*timg.size[0])+10):
                for j in range(int((touch.y-60)/480*timg.size[1])-9,int((touch.y-60)/480*timg.size[1])+10):
                    if i>=0 and i<timg.size[0] and j>=0 and j<timg.size[1]:
                        tpx[i,timg.size[1]-j-1] = (ranr,rang,ranb)
            timg.save(os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[self.texture_id]+'.png')
            #print self.scene.material.values()[self.texture_id]
            global texture_id_
            texture_id_[self.texture_id].remove_from_cache()
            self.draw_mark()

        else: 
            self._touches.append(touch)
        
    def draw_mark(self):
        self.redraw()
        global mytext
        textv.texture_update(mytext)   
    
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
        if keycode[1] == 't':
            print 'keycode disable'

    def btn_rotate(self):
        self._keyboard ='r'
        print 'rotate_mode'
    def btn_scale(self):
        self._keyboard ='s'
        print 'rotate_mode'
    def btn_checkerboard(self):
        #self._keyboard ='c'
        self.checkerboard_statue = 1 - self.checkerboard_statue
        self.redraw() 
        print 'checkerboard on/off'
    def btn_prev_texture(self):
        self.texture_id -= 1
        if self.texture_id == -1:
            self.texture_id = len(self.scene.objects)-1
        global global_texture_filename
        global_texture_filename = os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[self.texture_id]+'.png'
        global global_uv_filename
        global_uv_filename = os.path.split(sys.argv[1])[0]+'/uv_layout/uv'+self.scene.material.values()[self.texture_id][7:]+'.png'
        print 'texture prev',global_texture_filename,global_uv_filename
        #print global_texture_filename
        global mytext
        textv.texture_update(mytext)
    def btn_next_texture(self):
        self.texture_id += 1
        if self.texture_id == len(self.scene.objects):
            self.texture_id = 0
        global global_texture_filename
        global_texture_filename = os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[self.texture_id]+'.png'
        global global_uv_filename
        global_uv_filename = os.path.split(sys.argv[1])[0]+'/uv_layout/uv'+self.scene.material.values()[self.texture_id][7:]+'.png'
        print 'texture next',global_texture_filename,global_uv_filename
        #print global_texture_filename
        global mytext
        textv.texture_update(mytext)
    def btn_update_texture(self):
        global texture_id_   
        for id in range(0,len(self.scene.objects)):
            #Cache.remove(os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[id]+'.png')
            shutil.copyfile(os.path.split(sys.argv[1])[0]+'/texture/'+self.scene.material.values()[id]+'.png',os.path.split(sys.argv[1])[0]+'/texture/tmp_'+self.scene.material.values()[id]+'.png')
            texture_id_[id].remove_from_cache()
        self.redraw() 
        global mytext
        textv.texture_update(mytext)        
        print 'texture reset'

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

class textv(FloatLayout):
    def __init__(self, **kwargs):

        super(textv, self).__init__(**kwargs)

    def texture_update(self):
        self.redraw() 

    def redraw(self):
        global global_texture_filename
        global global_uv_filename

        rx=randint(0,1000000)
        shutil.copyfile(global_texture_filename,os.path.split(sys.argv[1])[0]+'/texture/'+'%07d'%rx+'.png')

        self.canvas.clear()

        with self.canvas:
            if os.path.isfile(global_texture_filename):
                Color(1,1,1,1)
                self.rect = Rectangle(source=os.path.split(sys.argv[1])[0]+'/texture/'+'%07d'%rx+'.png',size=[480,480],pos=[1010,60])
                #print global_texture_filename
            Color(0,0,0,1)
            self.rect = Rectangle(source=global_uv_filename,size=[480,480],pos=[1010,60])
        os.remove(os.path.split(sys.argv[1])[0]+'/texture/'+'%07d'%rx+'.png')



class ViewerApp(App):

    def build(self):

        global is_retina_screen
        if is_retina_screen: #retina screen?
            rtscreen = 2
        else:
            rtscreen = 1
        Window.size=(1500/rtscreen,600/rtscreen)
      
        parentlayout = FloatLayout()
        
        imgwidget = FloatLayout(size = (500,550), pos = (0,0))
        viewerwidget = FloatLayout(size = (500,550), pos = (500,0))
        texturewidget = FloatLayout(size = (500,550), pos = (1000,0))

        myimg = rimgv()
        imgwidget.add_widget(myimg)

        global myviewer
        myviewer = meshv()
        viewerwidget.add_widget(myviewer)

        global mytext
        mytext = textv()
        texturewidget.add_widget(mytext)

        with imgwidget.canvas.before:
            Color(1, 0, 0, 0.6) 
            self.rect = Rectangle(size=imgwidget.size,pos=imgwidget.pos)

        with viewerwidget.canvas.before:
            Color(0, 0, 1, 0.6) 
            self.rect = Rectangle(size=viewerwidget.size,pos=viewerwidget.pos)

        with texturewidget.canvas.before:
            Color(0, 1, 0, 0.6) 
            self.rect = Rectangle(size=texturewidget.size,pos=texturewidget.pos)

        textwidget = FloatLayout(size = (1500,50), pos = (0,0))

        with textwidget.canvas.before:
            Color(1,1,1,1)
            self.text = Label(text='Reference Image',pos=(200,-10),bold='True',font_size='20sp')
            self.text = Label(text='3D View',pos=(700,-10),bold='True',font_size='20sp')
            self.text = Label(text='Texture Image',pos=(1200,-10),bold='True',font_size='20sp')
        

        btnwidget = BoxLayout(orientation='horizontal',size = (1500,50), pos = (0,550))
        with btnwidget.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=btnwidget.size,pos=btnwidget.pos)
            Color(1,1,1,1)
            self.text = Label(text='Reference Image',pos=(200,-10),bold='True',font_size='20sp')
            self.text = Label(text='3D View',pos=(700,-10),bold='True',font_size='20sp')
            self.text = Label(text='Texture Image',pos=(1200,-10),bold='True',font_size='20sp')
        


        def btn1_callback(instance):
            myviewer.btn_rotate()
        def btn2_callback(instance):
            myviewer.btn_scale()
        def btn3_callback(instance):
            myviewer.btn_checkerboard()
        def btn4_callback(instance):
            idle = 0
        def btn5_callback(instance):
            myviewer.btn_update_texture()
        def btn6_callback(instance):
            myviewer.btn_prev_texture()
        def btn7_callback(instance):
            myviewer.btn_next_texture()


        btn1 = Button(text='rotate',size=(100,50),pos=(0,550),size_hint=(None,None))#heckerboard')
        btn1.bind(on_press=btn1_callback)
        btn2 = Button(text='scale',size=(100,50),pos=(101,550),size_hint=(None,None))
        btn2.bind(on_press=btn2_callback)
        btn3 = Button(text='checkerboard on/off',size=(200,50),pos=(201,550),size_hint=(None,None))
        btn3.bind(on_press=btn3_callback)
        btn4 = Button(text='texture project',size=(200,50),pos=(401,550),size_hint=(None,None))
        btn4.bind(on_press=btn4_callback)
        btn5 = Button(text='texture reset',size=(200,50),pos=(601,550),size_hint=(None,None))
        btn5.bind(on_press=btn5_callback)
        btn6 = Button(text='<<',size=(30,50),pos=(801,550),size_hint=(None,None))
        btn6.bind(on_press=btn6_callback)
        btn7 = Button(text='>>',size=(30,50),pos=(831,550),size_hint=(None,None))
        btn7.bind(on_press=btn7_callback)


        btnwidget.add_widget(btn1)
        btnwidget.add_widget(btn2)
        btnwidget.add_widget(btn3)
        btnwidget.add_widget(btn4)
        btnwidget.add_widget(btn5)
        btnwidget.add_widget(btn6)
        btnwidget.add_widget(btn7)


        parentlayout.add_widget(imgwidget, index=1)
        parentlayout.add_widget(viewerwidget, index=0)
        parentlayout.add_widget(texturewidget, index=2)
        parentlayout.add_widget(btnwidget)

        return parentlayout

    def on_stop(self):
        global myviewer
        for id in range(0,len(myviewer.scene.objects)):
            os.remove(os.path.split(sys.argv[1])[0]+'/texture/tmp_'+myviewer.scene.material.values()[id]+'.png')


if __name__ == "__main__":
    ViewerApp().run()
