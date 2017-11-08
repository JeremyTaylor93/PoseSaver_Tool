### Pose Saver UI ###

# creates a window and adds buttons that contain the pose information,
# these poses are exported to a folder under the character name and reLoaded on creation

# add character to a menu list 

import maya.cmds as cmds
import os
from functools import partial
import maya.mel as mel
from sys import argv

workspaceFilepath = cmds.workspace(q = True, fullName = True)
scriptsFilePath = workspaceFilepath + "/" + "scripts/PoseSaver"
blankFilePath = scriptsFilePath + "/" + "poseLibrary.txt"
print blankFilePath

rigFilePaths = {}
class PoseSaver():

	def __init__(self):
	
		# class vars
		self.widgets = {}
		
		self.rigList = {}
		
		# call on the build UI method
		self.buildUI()
		
	def buildUI(self):
	
		if cmds.window("PoseSaver_UI", exists = True):
			cmds.deleteUI("PoseSaver_UI")
		
		self.widgets["window"] = cmds.window("PoseSaver_UI",mnb = False, menuBar = True, mxb = False, t="PoseSaver_UI", w = 600, h = 600, sizeable = False, bgc = [0.15,0.15,0.15])
		
		cmds.menu( label='File', tearOff=True )
		cmds.menuItem( label='Quit', c = partial(self.quit, "PoseSaver_UI"))
		cmds.menu( label='Help', helpMenu=True )
		cmds.menuItem( 'Application..."', label='About Creator', c = self.about )
		
		
		# panel layout 
		self.widgets["mainLayout"] = cmds.paneLayout(configuration='vertical2' )
		# column layout inside first panel
		self.widgets["panel_1_Layout"] = cmds.columnLayout( w = 125, p = self.widgets["mainLayout"], bgc = [0.2,0.2,0.2])
		
		# first panel content
		
		#instructions on how to use poseSaver
		cmds.text(l='Instructions:',align='center',fn='boldLabelFont')
		cmds.separator(h=5, style = 'none')
		cmds.text(l=' add rigs to list before saving poses, \n you can load rigs and poses from \n the load rig button',align='left')
		cmds.separator(h=20, style = 'none')
		# character rig menu
		cmds.text(l='Choose a rig :',align='center')
		self.widgets["characterOptionMenu"] = cmds.optionMenu( w=125, bgc = [0.3,0.3,0.3])
		cmds.separator(h=20, style = 'none')
		# buttons to load rigs, add rigs and save poses
		cmds.separator(h=5, style = 'none')
		self.widgets["loadRigsButton"] = cmds.button(l='load rig', bgc = [0.15,0.15,0.15] )
		cmds.separator(h=5, style = 'none')
		self.widgets["addRigsButton"] = cmds.button(l='add rig', c=self.addRig, bgc = [0.15,0.15,0.15])
		cmds.separator(h=5, style = 'none')
		self.widgets["savePoseButton"] = cmds.button(l='save pose', c=self.savePose, bgc = [0.15,0.15,0.15])
		
		# set parent back up to panel layout
		cmds.setParent(u=True)
		
		# column layout inside second panel
		self.widgets["posesFormLayout"] = cmds.formLayout(bgc = [0.15,0.15,0.17])
		self.widgets["tabsLayout"] = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
		self.widgets["tabFormLayout"] = cmds.formLayout( self.widgets["posesFormLayout"], edit=True, attachForm=((self.widgets["tabsLayout"], 'top', 0), (self.widgets["tabsLayout"], 'left', 0), (self.widgets["tabsLayout"], 'bottom', 0), (self.widgets["tabsLayout"], 'right', 0)) )

		# second panel content
		

		#cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'One'), (child2, 'Two')) )
		
		# create window
		cmds.showWindow(self.widgets["window"])
		
		# edit window size
		self.widgets["window"] = cmds.window("PoseSaver_UI", edit=True, w = 600, h = 600, sizeable = False)
	
	def quit(self, window, *args):
		cmds.deleteUI(window)

	def loadRigs(self,*args):

		# get file directory for pose libraries

		poseSaverFP = scriptsFilePath + '/PoseSaver'

		# list files

		Libraries = os.listdir(poseSaverFP)

		for file in Libraries :


			rigName = file.rpartition('_')[0]

			print rigName

			poseLibrary = open(file,'r+')

			poseLibraryStr = poseLibrary.read()

	def loadRig(self, *args):

		# load RIG directories within project folder
		rigLibraries = os.listdir(scriptsFilePath)

		for rigFolder in rigLibraries:

			# read the file that holds the selecion command for all the rigscontrols and add it to the rigList dictionary
			rigLibPath = scriptsFilePath + '/' + rigFolder

			rigName = rigFolder.rpartition('_Pose')[0]
			rigCTRLS = rigLibPath+'/'+rigName+'_CTRLS_LIB.txt'

			rigFile = open(rigCTRLS,'r')

			rigList['rigName'] = rigFile.read()

			# create tab for loaded rig

			self.widgets[rigName] = cmds.menuItem(l=text, p=self.widgets["characterOptionMenu"])
			print self.widgets[rigName]

			self.widgets[rigName + "_tab"] = cmds.gridLayout(p=self.widgets["tabsLayout"])
			tabName = self.widgets[rigName + "_tab"]

			cmds.tabLayout(self.widgets["tabsLayout"], edit=True, tabLabel=((tabName, rigName)))
			print self.widgets["tabsLayout"]

			rigPoses = os.listdir(rigLibPath)

			for pose in rigPoses:

				# loop through POSE_LIB files and add them to window as buttons
				if pose == rigName+'_CTRLS_LIB.txt' :

					pass

				else:
					poseFilePath = rigLibPath + '/' + pose
					poseFile = open(poseFilePath, r)
					poseName = pose.rpartition('_POSE')[0]
					poseData = poseFile.read()
					cmds.button(l=poseName, p=self.widgets[rigName + "_tab"], c=poseData)









	
	def addRig(self,*args):
		
		# collect selection 
		controlsList = cmds.ls(sl=True)
		
		selectionCommand = []
		
		for control in controlsList :

			selectionCommand.append(control)
		
		result = cmds.promptDialog(
			title='Rename Object',
			message='Enter Name:',
			button=['OK', 'Cancel'],
			defaultButton='OK',
			cancelButton='Cancel',
			dismissString='Cancel')

		if result == 'OK':
			text = cmds.promptDialog(query=True, text=True)
			
		print text
		print self.widgets["characterOptionMenu"]
		print self.widgets["tabsLayout"]
		
		self.widgets[text] = cmds.menuItem(l=text, p = self.widgets["characterOptionMenu"])
		print self.widgets[text]
		
		self.widgets[text + "_tab"] = cmds.gridLayout(p=self.widgets["tabsLayout"])
		tabName = self.widgets[text + "_tab"]
		
		cmds.tabLayout(self.widgets["tabsLayout"], edit=True, tabLabel=((tabName, text)))
		print self.widgets["tabsLayout"]
		
		self.rigList[text] = selectionCommand

		# create LIB file for selecting rig controls
		rigFilePaths[text] = scriptsFilePath + "/PoseSaver/" + text + "_CTRLS_LIB.txt"

		rigFile = open(rigFilePaths[text], 'w+')

		rigFile.write(selectionCommand)

		rigFile.close()

	def savePose(self,*args):
		
		currentMenuItem = cmds.optionMenu(self.widgets["characterOptionMenu"], q=True, v = True)
		
		print currentMenuItem
		
		cmds.select(clear=True)

		filePath = rigFilePaths[currentMenuItem]
		
		for control in self.rigList[currentMenuItem] :
			cmds.select(control, add=True)
		
		rigControls = cmds.ls(sl=True)
		
		safeShelfCommand = ''
		
		for control in rigControls :
		
			controlAttrs = cmds.listAttr(control, r=True, w=True, k=True, u=True, v=True, m=True, s=True, )
			
			for attr in controlAttrs :
				
				value =  cmds.getAttr((control+"."+attr))
				safeShelfCommand = ("cmds.setAttr('"+str(control) + "." + str(attr)+"'," + str(value)+") \n") + safeShelfCommand
		
		result = cmds.promptDialog(
			title='Rename Object',
			message='Enter Name:',
			button=['OK', 'Cancel'],
			defaultButton='OK',
			cancelButton='Cancel',
			dismissString='Cancel')

		if result == 'OK':
			text = cmds.promptDialog(query=True, text=True)

		ifp = scriptsFilePath + "/PoseSaver"

		# Prepare unique image name for snapshot
		imageSnapshot = ifp + "/" + currentMenuItem + '_' + text +"_Snapshot.jpg"

		# Take a snapshot of the viewport and save to file
		cmds.refresh(cv=True, fe="jpg", fn=imageSnapshot)


		cmds.button( l= text, p = self.widgets[currentMenuItem + "_tab"], c = safeShelfCommand)

		# save pose to file

		rigFile = open(filePath, 'r')

		fileStr = rigFile.read()

		rigFile.close()

		rigFileWrite = open(filePath, 'w+')

		addedLine = '\n' + text + '_Pose:'

		rigFileWrite.write(fileStr)

		rigFileWrite.write(addedLine)

		rigFileWrite.write(safeShelfCommand)

		rigFileWrite.write(':End. \n')

		rigFileWrite.close()
	
	def about(self, *args):
	
		if cmds.window("AboutWindow", q=True, exists = True):
			cmds.deleteUI("AboutWindow")
			
		aboutWindow = cmds.window("AboutWindow",t="About",w=200,h=200,bgc=[0.15,0.15,0.15], sizeable=False)
		cmds.columnLayout(parent = "AboutWindow",adj=True)
		
		cmds.text(l='About AutoRig', fn='boldLabelFont', align='center' )
		cmds.separator(h=10, style = 'none')
		cmds.rowColumnLayout(nc=2, cw=[(1,100),(2,190)])
		cmds.text(l='Created by:', align='center' )
		cmds.text(l='Jeremy Taylor', align='left' )
		cmds.separator(h=5, style = 'none')
		cmds.separator(h=5, style = 'none')
		cmds.text(l='Email:', align='center' )
		cmds.text(l='jeremytaylortd@gmail.com', align='left' )
		cmds.separator(h=5, style = 'none')
		cmds.separator(h=5, style = 'none')
		cmds.text(l='Vimeo Page :', align='center' )
		vimeoLink = cmds.text(hl=True, l="https://vimeo.com/spiritforger101", align='left' )
		print vimeoLink
		cmds.separator(h=10, style = 'none')
		cmds.separator(h=10, style = 'none')
		cmds.text(l='Report Bugs:', align='center' )
		cmds.text(l='No Link', align='left' )
		
		cmds.setParent(u=True)
		
		cmds.separator(h=10,style='none')
		
		cmds.button(l='Exit',c=partial(self.quit, "AboutWindow"),bgc=[0.2,0.2,0.2])
		
		cmds.showWindow(aboutWindow)
		
		cmds.window("AboutWindow", e=True,w=290,h=140)
			
		
	
