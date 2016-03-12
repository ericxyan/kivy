Assignment #1 Part B
CSC320 Spring 2016
Kyros Kutulakos

Notes on the starter code for the matting GUI application 

---------------
GENERAL REMARKS
---------------

A. REFERENCE SOLUTION BINARY EXECUTABLE

  I am supplying a fully-functional version of the python code in 
  compiled form (ie. a binary, statically-linked executable), so you 
  have a reference solution. Currently I only have this available for
  Mac OS X but I am trying to get a CDF-compatible executable
  binary as well. I will let you know when it becomes available.

     viscomp-gui.osx    					    available now
     /u/csc320h/winter/pub/A1/viscomp-gui.cdf   available shortly

B. STARTER EXECUTABLE

  The top-level python executable is

     viscomp-gui.py

C. RUNNING THE EXECUTABLE

  To run, use
     viscomp-gui.py -- --usegui

  The executables operate in two modes:

D. GETTING FAMILIAR WITH THE INTERFACE

  1. The GUI has two modes: Matting and Compositing.
  2. You can switch between those modes by clicking the "Switch Modes" button
  3. The lower-right button shows the GUI's "current image". Clicking
     on that button will open a dialog box to load that image from a file
     (if it is an input image) or to save to a file (if the image is an
     output image of the algorithm).
  4. To run the triangulation matting algorithm, you need to load its four
     input images. To do that, click the lower-right button and choose an
     image with the dialog box, the click the 'Switch Image' button to load
     the second image, etc. Once all four input images are loaded, you can 
     press the 'Run' button to run the algorithm. Switching images again
     will now also show you the two output images of the algorithm: the 
     matte and the object color. Those can be saved by clicking the 
     lower-right button again. 
  5. Pressing the escape key closes the GUI and terminates the program
  6. Clicking with the left mouse button on the image being displayed
     shows a pair of red axes centered on the point being clicked, along
     with the point's coordinates. These axes disappear after the mouse
     button is released.
  7. Dragging the mouse button drags the image. The image can be moved 
     back to its original position by double-clicking/double-tapping on
     the image.
  8. To run compositing, click the 'Switch mode' button and load appropriate
     input images.

---------------------
STRUCTURE OF THE CODE
---------------------

1. GENERAL NOTES

  * partB/viscomp-gui
       top-level routine that does nothing other than call the
       code's main function, located in partB/mattingui/run.py

2. IMPORTANT: 

  We will be running scripts to test your code automatically. To 
  ensure proper handling and marking, observe the following:

  * All your widget specs should go in file partB/kv/viscomp.kv 
  * All your python code should go in the files partB/mattingui/widgets.py
    and partB/mattingui/viewer.py 
  * Do not modify any files other than those three
  * Do not modify any parts of these files except where specified
  * Do not add any extra files or directories under partB/mattingui/
  * Do not create any extra directories in partB/
  * The code expects the files for Part A to be located at their original
    locations under partA of the code

3. GENERAL STRUCTURE & HOW TO NAVIGATE THE CODE

  The GUI is defined in the file kv/viscomp.kv. This defines the entire
  set of widgets used by the GUI and controls which methods are called
  in response to various GUI events (button presses, mouse clicks, etc).
  You need to start by reading this file. It is heavily commented, to 
  guide you through its structure, etc. ** you will need to add a few specs
  to this file in order to implement the functionalities requested in A1-PartB

  Each Kivy widget is an instance of a Kivy widget class. The most important
  class in the code is RootWidget. This class is defined in file mattingui/widgets.py. 
  Read this file next and try to understand it well. You will need to write
  one of its methods.

  To load/save images in the Matting object you used in PartA, the code uses
  a class called MattingControl. This 'sits' in between the RootWidget class
  and the Matting class. The RootWidget class you need to write will have to
  call one of the methods in this file.

  The last file you should look at is viewer.py. This file defines a widget
  called ImageViewer that controls how images are displayed and how a user
  can interact with those images. You will need to implement a method in this
  class as part of the assignment, so read this code carefully. This code
  does **not** depend on triangulation matting.

4. FILES UNDER THE DIRECTORY partB/

   kv/viscomp.py	
			Specifications written in the kivy widget specification language.
			The comments in this file should be sufficient to understand its
			basic structure. The assignment does NOT depend on learning much
			about this language beyond what is in this file already.

   mattingui/widgets.py
			The only relevant part of this file are the methods of the 
			RootWidget class. 
			
   mattingui/control.py
		    The only relevant functions are those labelled "Top-level methods when
		    interacting with the GUI". You can ignore the rest, at least initially.
		
   mattingui/viewer.py
			A widget class for displaying images. This is completely
			independent of the matting algorithm. You will need to add 
			(at least) one method to this class for partB of the assignment. 
			
   run.py	This has the same structure and functionality as the run.py 
            script in PartA/matting. No need to look at it.

