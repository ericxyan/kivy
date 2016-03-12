## CSCN Winter 2016 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
from matplotlib import pyplot as plt
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################
def haveNone(mat, mdict):
	"""
	mdict: A dictionary
	Return True if any element in mdict is None.
	Return False if all element are valid.
	"""
	for key in mdict.keys():
		if mat._images[key] is None:
			return True
	return False   

def ein_inv_solver(A, B):
	M, N, R, C = A.shape
	D = M * N
	
	AT = A.transpose((0,1,3,2))
	B = B.reshape(M,N,6, 1)

	A2 = np.einsum('...ij,...jk->...ik', AT, A).reshape(-1, C, C)
	B2 = np.einsum('...ij,...jk->...ik', AT, B).reshape(-1, C)

	sol = np.linalg.solve(A2, B2).reshape(M,N,C)
	return sol
#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
	#
	# The class constructor
	#
	# When called, it creates a private dictionary object that acts as a container
	# for all input and all output images of the triangulation matting and compositing 
	# algorithms. These images are initialized to None and populated/accessed by 
	# calling the the readImage(), writeImage(), useTriangulationResults() methods.
	# See function run() in run.py for examples of their usage.
	#
	def __init__(self):
		self._images = { 
			'backA': None, 
			'backB': None, 
			'compA': None, 
			'compB': None, 
			'colOut': None,
			'alphaOut': None, 
			'backIn': None, 
			'colIn': None, 
			'alphaIn': None, 
			'compOut': None, 
		}

	# Return a dictionary containing the input arguments of the
	# triangulation matting algorithm, along with a brief explanation
	# and a default filename (or None)
	# This dictionary is used to create the command-line arguments
	# required by the algorithm. See the parseArguments() function
	# run.py for examples of its usage
	def mattingInput(self): 
		return {
			'backA':{'msg':'Image filename for Background A Color','default':None},
			'backB':{'msg':'Image filename for Background B Color','default':None},
			'compA':{'msg':'Image filename for Composite A Color','default':None},
			'compB':{'msg':'Image filename for Composite B Color','default':None},
		}
	# Same as above, but for the output arguments
	def mattingOutput(self): 
		return {
			'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
			'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
		}
	def compositingInput(self):
		return {
			'colIn':{'msg':'Image filename for Object Color','default':None},
			'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
			'backIn':{'msg':'Image filename for Background Color','default':None},
		}
	def compositingOutput(self):
		return {
			'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
		}
	
	# Copy the output of the triangulation matting algorithm (i.e., the 
	# object Color and object Alpha images) to the images holding the input
	# to the compositing algorithm. This way we can do compositing right after
	# triangulation matting without having to save the object Color and object
	# Alpha images to disk. This routine is NOT used for partA of the assignment.
	def useTriangulationResults(self):
		if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
			self._images['colIn'] = self._images['colOut'].copy()
			self._images['alphaIn'] = self._images['alphaOut'].copy()

		# If you wish to create additional methods for the 
		# Matting class, include them here

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################

		#########################################
			
	# Use OpenCV to read an image from a file and copy its contents to the 
	# matting instance's private dictionary object. The key 
	# specifies the image variable and should be one of the
	# strings in lines 82-91. See run() in run.py for examples
	#
	# The routine should return True if it succeeded. If it did not, it should
	# leave the matting instance's dictionary entry unaffected and return
	# False, along with an error message
	def readImage(self, fileName, key):
		success = False
		msg = 'Placeholder'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		try:
			self._images[key] = cv.imread(fileName, -1)
			if self._images[key] is not None:
				success = True
			else:
				msg = 'Wrong file ' + fileName
		except IOError:
			msg = "can\'t read file: " + fileName
		
		#########################################
		return success, msg

	# Use OpenCV to write to a file an image that is contained in the 
	# instance's private dictionary. The key specifies the which image
	# should be written and should be one of the strings in lines 82-91. 
	# See run() in run.py for usage examples
	#
	# The routine should return True if it succeeded. If it did not, it should
	# return False, along with an error message
	def writeImage(self, fileName, key):
		success = False
		msg = 'Placeholder'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		try:
			cv.imwrite(fileName, self._images[key])
			success = True
		except IOError:
			msg = "can\'t write file: " + fileName

		#########################################
		return success, msg

	# Method implementing the triangulation matting algorithm. The
	# method takes its inputs/outputs from the method's private dictionary 
	# ojbect. 
	def triangulationMatting(self):
		"""
success, errorMessage = triangulationMatting(self)
		
		Perform triangulation matting. Returns True if successful (ie.
		all inputs and outputs are valid) and False if not. When success=False
		an explanatory error message should be returned.
		"""

		success = False
		msg = 'Placeholder'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		# Validate inputs
		if not haveNone(self, self.mattingInput()):        
			# Convert to 0.0 - 1.0 scale
			backA = np.divide(self._images['backA'], 255.)
			backB = np.divide(self._images['backB'], 255.)
			compA = np.divide(self._images['compA'], 255.)
			compB = np.divide(self._images['compB'], 255.)
			M = backA.shape[0]
			N = backA.shape[1]
			C = backA.shape[2]
			# Construct matrix B
			BA = np.subtract(compA, backA)
			BB = np.subtract(compB, backB)
			B = np.dstack((BA,BB))
			# Construct matrix A
			E = np.tile(np.eye(3), (M,N,1,1))
			aa = np.multiply(backA.reshape(M,N,3,1), -1)
			ab = np.multiply(backB.reshape(M,N,3,1), -1)
			aa = np.concatenate((E, aa), axis=3)
			ab = np.concatenate((E, ab), axis=3)
			A = np.concatenate((aa,ab), axis=2)
			# Solve equation Ax=B
			sol = ein_inv_solver(A, B)
			# Clip to 0.0-1.0
			c0 = np.clip(sol, 0.0, 1.0)
			# Rescale to 0-255
			c0 = np.uint8(c0 * 255)
			# Store outputs
			self._images['colOut'] = c0[:,:,:-1]
			self._images['alphaOut'] = c0[:,:,-1]
			
			if not haveNone(self, self.mattingOutput()):
				success = True
			else:
				msg = 'Wrong matting outputs.'
		else:
			msg = 'Wrong matting inputs.'
		#########################################

		return success, msg
	
	def createComposite(self):
		"""
success, errorMessage = createComposite(self)
		
		Perform compositing. Returns True if successful (ie.
		all inputs and outputs are valid) and False if not. When success=False
		an explanatory error message should be returned.
"""

		success = False
		msg = 'Placeholder'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		if not haveNone(self, self.compositingInput()):
			colIn = self._images['colIn']
			alphaIn = self._images['alphaIn'] / 255.0         
			M, N, C = colIn.shape
			
			compOut = colIn + (1 - alphaIn.reshape(M, N, -1)) * self._images['backIn']
			self._images['compOut']  = np.uint8(compOut)
			
			if not haveNone(self, self.compositingOutput()):
				success = True
			else:
				msg = 'Wrong compositing outputs.'
		else:
			msg = 'Wrong compositing inputs.'
		#########################################

		return success, msg