## CSC320 Winter 2016 
## Assignment 1 - Part B
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

##
## This file defines a single class called RootWidget that
## controls the behavior of the RootWidget defined in the
## file viscomp.kv. 
##
## It's purpose is two-fold:
##    (a) It isolates all functions called by the widgets viscomp.kv
##        from all other code
##    (b) It defines all the routines required for the GUI to operate
##        correctly
##

import kivy
kivy.require('1.9.1')

from kivy import Config
# disable fullscreen mode
Config.set('graphics','fullscreen','0')
# do not allow window resizing
Config.set('graphics','resizable','0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.graphics import *
from kivy.input.postproc.doubletap import *
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger

from control import MattingControl

# 
# The class that defines the whole GUI application. 
# This class is created immediately when the program
# is run. Then control is passed to the program's 
# main() function which must ultimately call
# its run() method to display all windows and enter
# the GUI's main loop.
#
class VisCompApp(App):
    def build(self):
        '''This method loads the VisComp.kv file automatically

        :rtype: none
        '''

        # This tells Kivy's window- and widget-building
        # routine where to find the .kv file that specifies
        # all the widgets to be created
        try:
            filename = 'kv/viscomp.kv'
            # loading the content of viscomp.kv and building its widgets
            self.root = Builder.load_file(filename)
        except Exception as e:
            Logger.exception('VisComp: Unable to load <%s>' % filename)
            
    def on_pause(self):
        return True

#
# Class definitions for the two dialog box widgets
# used by the GUI, for opening and saving files, respectively
# These are taken from Kivy's RST_Editor tutorial example
#

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
#
# Class that controls the complete GUI. It is derived from 
# Kivy's built-in FloadLayout widget class
class RootWidget(FloatLayout):
    # Create an instance of the MattingControl class that will 
    # take care of all functionalities related to matting.
    mattingControl = MattingControl()
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    # 
    # All the methods below are called by widgets of viscomp.kv
    #

    # Switch the GUI's current mode
    def next_mode(self):
        # change the mode of the matting class
        self.mattingControl.nextMode()
        # update the variable holding the current mode's descriptive text
        self.modeText = self.currentModeMsg()
        # update the variable holding the current image's descriptive text
        self.imageText = self.currentImageMsg()
        # display the current image in the imview widget
        self.display_current_image()
                
    # Switch the GUI's current image
    def next_image(self):
        # change the current image of the matting class
        self.mattingControl.nextImage()        
        # update the variable holding the current mode's descriptive text
        self.imageText = self.currentImageMsg()        
        # display the current image in the imview widget
        self.display_current_image()        
        
    # Run the algorithm associate with the GUI's current mode
    def run_algorithm(self):
        
#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################
        success, text = self.mattingControl.runAlgorithm()
        if not success:
            popup = Popup(title='Failed', content=Label(text='Run algorithm failed!'), size_hint=(0.4, 0.4))
            popup.open()

#########################################
        return

    # These methods simply call the associated routine of the 
    # mattingControl class to get the descriptive strings to be
    # displayed by the GUI's various buttons
    def currentModeMsg(self):
        return self.mattingControl.currentModeMsg()
    def currentImageMsg(self):
        return self.mattingControl.currentImageMsg()
    def currentFileActionMsg(self):
        return self.mattingControl.currentFileActionMsg()

    # Method to update the image displayed by the imviewer widget
    def display_current_image(self):
        # first we get the OpenCV image associated with the GUI's 
        # current image
        currentOpenCVImage = self.mattingControl.imageData()
        # then we call the imviewer's display routine to display it
        self.ids.imviewer.display_opencv_image(currentOpenCVImage)

    # Method to display a small popup window showing an error message
    # The method expects a title for the popup as well as a message
    def show_error_popup(self, title, message):
        try:
            content = Label(text=message)
            self._popup = Popup(title=title, content=content,
                                size_hint=(0.9, None))
            self._popup.open()
        except Exception as e:
            Logger.exception('VisComp: Error %s' %message)

    # Method to close a popup that is currently shown on screen
    def dismiss_error_popup(self):
        self._popup.dismiss()
    
    # Routine to display the dialog box for selecting an image file for
    # opening/writing
    def show_dialog(self):
        if self.mattingControl.isInputImage():
            content = LoadDialog(load=self.load, cancel=self.dismiss_error_popup)
            self._popup = Popup(title="Open Image", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        elif self.mattingControl.isOutputImage():
            content = SaveDialog(save=self.save, cancel=self.dismiss_error_popup)
            self._popup = Popup(title="Save Image", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()

    # Lower-level routines for loading and saving an image
    def _loadsave(self, filename, func, s):
        if len(filename)<=0:
            return
        
        ok, msg = func(filename)
        if not ok:
            title = 'Error %s Image'%s
            self.show_error_popup(title, msg)
        else:
            self.display_current_image()
        self.dismiss_error_popup()
    def load(self, path, filenameList):
        s = 'Opening'
        self._loadsave(filenameList[0], self.mattingControl.load, s)

    def save(self, path, filename):
        s = 'Saving'
        self._loadsave(filename, self.mattingControl.save, s)

        
        

