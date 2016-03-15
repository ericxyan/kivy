## CSC320 Winter 2016 
## Assignment 1 - Part B
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY


##
## DO NOT MODIFY THIS FILE 
##


##
## This file defines a single class called MattingControl that
## is derived from the Matting class of Assignment 1 Part A.
## It's purpose is three-fold:
##    (a) It isolates all matting-related functions and internal variables
##        from the GUI code
##    (b) It maintains two state variables that can be changed
##        through the GUI: the 'current mode' and the 'current image'
##        The 'current mode' controls which algorithm is run when we
##        press the Run button on the GUI. The 'current image' controls
##        (1) which image variable in the Matting class is changed when
##        we press the 'Image Open' button or (2) which image of the 
##        matting class is saved to a file when we press the 'Image Save'
##        button
##    (c) It stores the various strings to be displayed by the GUI 
##        for various modes, input/output images, etc.
##


import kivy
kivy.require('1.9.1')

from itertools import cycle
import sys

## import the Matting class and its methods
from matting.algorithm import Matting

class MattingControl(Matting):

    def __init__(self):
        Matting.__init__(self)
        # Specify the set of images relevant to each algorithm
        self._modes = {
            'Matting':dict(self.mattingInput().items() + self.mattingOutput().items()), 
            'Compositing':dict(self.compositingInput().items() + self.compositingOutput().items())
        }
        # Specify the set of input images expected by all algorithms
        self._inout = {
            'Input':dict(self.mattingInput().items() + self.compositingInput().items()), 
            'Output':dict(self.mattingOutput().items() + self.compositingOutput().items())
        }
        # Specify which method of Matting should be run in each mode
        self._algorithm = {
            'Matting':self.triangulationMatting,
            'Compositing':self.createComposite
        }
        
        # Define an iterator that allows us to switch between
        # the two modes of the GUI
        self._modeOrder = ['Matting', 'Compositing']
        self._modeIter = cycle(self._modeOrder)
        self.nextMode()

    #
    # Top-level methods called when interacting with the GUI. These methods
    # are NOT called directly by the GUI, they are called by methods of 
    # the class RootWidget. 
    #
    
    # Run the algorithm associated with the current mode of the GUI
    def runAlgorithm(self):
        return (self._algorithm[self._currentMode])()

    # Cycle through the modes
    def nextMode(self):
        self._currentMode = self._modeIter.next()
        self._imageIter = cycle(self._sortByMsg(self._modes[self._currentMode]))
        self.nextImage()

    # Cycle through the images relevant to each mode
    def nextImage(self):
        self._currentImage = self._imageIter.next()

    # Load into the current image the file given by filename
    def load(self,filename):
        if self.isInputImage():
            return self.readImage(filename, self._currentImage)
        else:
            return False, 'MattingInterface: %s is not an input image'%self._currentImage

    # Save the current image to the file given by filename
    def save(self,filename):
        if self.isOutputImage():
            return self.writeImage(filename, self._currentImage)
        else:
            return False, 'MattingInterface: %s is not an input image'%self._currentImage

    # Return the OpenCV image data structure for the current image
    def imageData(self):
        if self._images.has_key(self._currentImage):
            return self._images[self._currentImage]
        else:
            return None

    #
    # Utility methods called by methods of the RootWidget class
    #

    # Return a string that describes the current mode
    def currentModeMsg(self):
        return self._currentMode
    # Return a string that describes the current image
    def currentImageMsg(self):
        return self._modes[self._currentMode][self._currentImage]['msg']
    # Return 'Open' if the current image is an input image and 'Save' otherwise
    def currentFileActionMsg(self):
        if self.isInputImage():
            return 'Open'
        else:
            return 'Save'
    # Return True if the current image is an input image
    def isInputImage(self):
        return self._currentImage in self._inout['Input'].keys()
    # Return True if the current image is an output image
    def isOutputImage(self):
        return self._currentImage in self._inout['Output'].keys()
    
    
    def _sortByMsg(self,modeDict):
        return map(lambda x: x[0], sorted(modeDict.items(),key=lambda x:x[1]['msg']))
    
    #
    # Define the descriptive text to be displayed for the various
    # input and output images 
    #
        
    def mattingInput(self): 
        return {
            'backA':{'msg':'Input Background A Color','default':None},
            'backB':{'msg':'Input Background B Color','default':None},
            'compA':{'msg':'Input Composite A Color','default':None},
            'compB':{'msg':'Input Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self): 
        return {
            'colOut':{'msg':'Output Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Output Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Input Object Color','default':None},
            'alphaIn':{'msg':'Input Object Alpha','default':None},
            'backIn':{'msg':'Input Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Output Composite Color','default':['comp.tif']},
        }
