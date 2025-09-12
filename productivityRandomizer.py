import wx
import random
import json


class taskWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 640))
        
        self.panel = wx.Panel(self)
        self.elememtWrapper = wx.BoxSizer(wx.VERTICAL)
        #self.elememtWrapper = wx.GridSizer(cols=1, rows=2, hgap=0, vgap=30)
        
        taskElements = []

        


        self.taskNameLabel = wx.StaticText(self.panel, label="Task Name:")
        taskElements.append(self.taskNameLabel)
        self.taskNameInput = wx.TextCtrl(self.panel)
        taskElements.append(self.taskNameInput)

        self.methodCheckCompletable = wx.CheckBox(self.panel, label="Completable")
        taskElements.append(self.methodCheckCompletable)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))
        
        self.methodCheckList = wx.CheckBox(self.panel, label="5 Key Sentences")
        taskElements.append(self.methodCheckList)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))

        self.methodCheckWords = wx.CheckBox(self.panel, label="400 words")
        taskElements.append(self.methodCheckWords)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))

        self.methodCheckW3 = wx.CheckBox(self.panel, label="Complete 3+ pages (W3)")
        taskElements.append(self.methodCheckW3)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))

        self.methodCheckProgram = wx.CheckBox(self.panel, label="Make Program")
        taskElements.append(self.methodCheckProgram)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))

        self.methodCheckCustom = wx.CheckBox(self.panel, label="Custom")
        taskElements.append(self.methodCheckCustom)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))

        self.addTaskButton = wx.Button(self.panel, label="Add Task")
        self.Bind(wx.EVT_BUTTON, self.addTaskClick, self.addTaskButton)
        taskElements.append(self.addTaskButton)
        #Null Element
        taskElements.append(wx.StaticText(self.panel, label=""))

        self.taskSizer = wx.GridSizer(cols=2, rows=len(taskElements)//2+1, vgap=3, hgap=3)

        self.taskSizer.AddMany(taskElements)
        self.elememtWrapper.Add(self.taskSizer, proportion=0, flag=wx.ALIGN_LEFT)
        #TODO: Make Display Tasks work properly
        """
        self.randomTaskSizer = wx.GridSizer(cols=2, rows=1, vgap=4, hgap=4)
        self.elememtWrapper.Add(self.randomTaskSizer, proportion=0, flag=wx.ALIGN_LEFT)

        
        self.possibleTaskDisplays = []
        self.taskDeleteButtons = []

        self.displayTasks()"""

        self.panel.SetSizer(self.elememtWrapper)

        
        self.Show(True)
    
    """
    def displayTasks(self):
        for destroyIndex in range (len(self.possibleTaskDisplays)-1, -1, -1):
            self.possibleTaskDisplays[destroyIndex].Destroy()
            self.taskDeleteButtons[destroyIndex].Destroy()

        self.possibleTaskDisplays = []
        self.taskDeleteButtons = []

        for taskIndex in range(0, len(tasks)):
            self.possibleTaskDisplays.append(wx.StaticText(self.panel, label=tasks[taskIndex].taskName))
            self.randomTaskSizer.Add((self.possibleTaskDisplays[taskIndex]), 0, flag=wx.ALIGN_LEFT)

            self.taskDeleteButtons.append(wx.Button(self.panel, label="Delete"))
            self.randomTaskSizer.Add((self.taskDeleteButtons[taskIndex]), 0, flag=wx.ALIGN_LEFT)
        
        self.panel.SetSizer(self.elememtWrapper)
    """
        



        


        



    def addTaskClick(self, event):
        taskNameStr = self.taskNameInput.GetValue()
        
        taskMethodsList = []

        if self.methodCheckCompletable.GetValue():
            taskMethodsList.append("Do: ")
        
        if self.methodCheckList.GetValue():
            taskMethodsList.append("Write 5 key sentences about: ")
        
        if self.methodCheckWords.GetValue():
            taskMethodsList.append("Write 400 words about: ")

        if self.methodCheckW3.GetValue():
            taskMethodsList.append("Complete 3 or more pages (usually on W3) about: ")

        if self.methodCheckProgram.GetValue():
            taskMethodsList.append("Make a program about: ")
        
        if self.methodCheckCustom.GetValue():
            customTaskWindow(task(taskNameStr, taskMethodsList))
        else:
            tasks.append(task(taskNameStr, taskMethodsList))
            #mainWindow.displayTasks()

    

class customTaskWindow(wx.Frame):
    def __init__(self, taskForCustomization):
        wx.Frame.__init__(self, title="Custom Method Task", parent=None, size=(400, 580))
        self.Panel = wx.Panel(self)
        self.taskForCustomization = taskForCustomization

        self.customEntriesAmount = 1

        self.customTaskLabels = [wx.StaticText(self.Panel, label=f"Custom {self.customEntriesAmount}:",
                                               pos=(2, 5 + (self.customEntriesAmount - 1) * 25))]
        self.customMethodsEntries = [wx.TextCtrl(self.Panel, pos=(60, 5 + (self.customEntriesAmount - 1) * 25))]

        self.addTaskButton = wx.Button(self.Panel, label="Add Task", pos=(2, 30 + (self.customEntriesAmount - 1) * 25))
        self.addCustomFieldButton = wx.Button(self.Panel, label="Add Custom Field", pos=(80, 30 + (self.customEntriesAmount - 1) * 25))
        
        self.Bind(wx.EVT_BUTTON, self.addTaskWithCustomMethods, self.addTaskButton)
        self.Bind(wx.EVT_BUTTON, self.addCustomField, self.addCustomFieldButton)

        self.Show(True)


    def addTaskWithCustomMethods(self, event):
        for inMethodEntry in self.customMethodsEntries:
            self.taskForCustomization.taskMethods.append(inMethodEntry.GetValue())
        tasks.append(self.taskForCustomization)

        #mainWindow.displayTasks()

        self.Close(True)
    
    def addCustomField (self, event):
        self.customEntriesAmount += 1
        self.customTaskLabels.append(wx.StaticText(self.Panel, label=f"Custom {self.customEntriesAmount}:",
                                               pos=(2, 5 + (self.customEntriesAmount - 1) * 25)))
        self.customMethodsEntries.append(wx.TextCtrl(self.Panel, pos=(60, 5 + (self.customEntriesAmount - 1) * 25)))

        self.addTaskButton.SetPosition((2, 30 + (self.customEntriesAmount - 1) * 25))
        self.addCustomFieldButton.SetPosition((80, 30 + (self.customEntriesAmount - 1) * 25))

        if self.customEntriesAmount >= 16:
            self.addCustomFieldButton.Disable()
        
        


        




class task():
    def __init__(self, taskName, taskMethods):
        self.taskName = taskName
        self.taskMethods = taskMethods
        
    
    def getTaskWithMethod(self):
        if len(self.taskMethods) > 1:
            methodIndex = random.randint(0, len(self.taskMethods)-1)
            return self.taskMethods[methodIndex]+self.taskName
        elif len(self.taskMethods) == 1:
            return self.taskMethods[0]+self.taskName
        else:
            return "Do: " + self.taskName
    
    def exportJSON(self):
        JSON = {
            "taskName": self.taskName,
            "taskMethods": self.taskMethods
        }

        return json.dumps(JSON)
    
    def taskFromJSON(JSON):
        taskPyDict = json.loads(JSON)        

        return task(taskPyDict["taskName"], taskPyDict["taskMethods"])
    
    


tasks = []

root = wx.App()
mainWindow = taskWindow(None, "Task Randomizer")






root.MainLoop()

"""
while(True):


    

    print ("press enter to continue")
    input()

    taskIndex = random.randint(0, len(tasks)-1)

    if specificTask[taskIndex]:
        print ("Do "+tasks[taskIndex])
    else:
        methodIndex = random.randint(0, len(taskMethods)-1)
        print(taskMethods[methodIndex]+tasks[taskIndex])
"""