import wx
import random
import json


class taskWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(350, 320))
        
        # = wx.Panel(self)
        self.taskWrapper = wx.BoxSizer(wx.VERTICAL)
        
        self.notebookOverview = wx.Notebook(self, style=wx.NB_TOP, name="Task Randomizer Tab Organizer", size=(60, 60))

        
        self.taskPanel = wx.Panel(self.notebookOverview)
        taskElements = []

        self.taskNameGrid = wx.GridSizer(cols = 2, rows=1, vgap=2, hgap=2)
        self.taskNameLabel = wx.StaticText(self.taskPanel, label="Task Name:")
        self.taskNameGrid.Add(self.taskNameLabel)

        #taskElements.append(self.taskNameLabel)
        self.taskNameInput = wx.TextCtrl(self.taskPanel, size=(70, 24))
        self.taskNameGrid.Add(self.taskNameInput)
        taskElements.append(self.taskNameGrid)
        #taskElements.append(self.taskNameInput)

        self.methodCheckCompletable = wx.CheckBox(self.taskPanel, label="Completable")
        taskElements.append(self.methodCheckCompletable)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))
        
        self.methodCheckList = wx.CheckBox(self.taskPanel, label="5 Key Sentences")
        taskElements.append(self.methodCheckList)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))

        self.methodCheckWords = wx.CheckBox(self.taskPanel, label="400 words")
        taskElements.append(self.methodCheckWords)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))

        self.methodCheckW3 = wx.CheckBox(self.taskPanel, label="Complete 3+ pages (W3)")
        taskElements.append(self.methodCheckW3)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))

        self.methodCheckProgram = wx.CheckBox(self.taskPanel, label="Make Program")
        taskElements.append(self.methodCheckProgram)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))

        self.methodCheckCustom = wx.CheckBox(self.taskPanel, label="Custom")
        taskElements.append(self.methodCheckCustom)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))

        self.addTaskButton = wx.Button(self.taskPanel, label="Add Task")
        self.Bind(wx.EVT_BUTTON, self.addTaskClick, self.addTaskButton)
        taskElements.append(self.addTaskButton)
        #Null Element
        #taskElements.append(wx.StaticText(self.taskPanel, label=""))


        
        
        self.taskSizer = wx.GridSizer(cols=1, rows=len(taskElements)+1, vgap=3, hgap=3)

        self.taskSizer.AddMany(taskElements)
        self.taskWrapper.Add(self.taskSizer, proportion=0, flag=wx.ALIGN_LEFT)
        #TODO: Make Display Tasks work properly
        
        self.randomPanel = wx.Panel(self.notebookOverview)

        self.randomOverviewLabel = wx.StaticText(self.randomPanel, label="Available Tasks:", pos=(1, 1))
        
        
        self.taskListBox = wx.ListBox(self.randomPanel, size=(300, 85), pos=(1, 20))

        self.randomizeButton = wx.Button(self.randomPanel, label="Randomize", pos=(1, 110))
        self.Bind(wx.EVT_BUTTON, self.drawRandomTask, self.randomizeButton)
        
        self.deleteButton = wx.Button(self.randomPanel, label="Delete", pos=(81, 110))
        self.Bind(wx.EVT_BUTTON, self.deleteTask, self.deleteButton)

        self.saveAllButton = wx.Button(self.randomPanel, label="Save All", pos=(156, 110))
        self.Bind(wx.EVT_BUTTON, self.saveTasks, self.saveAllButton)
        
        self.resultText = wx.StaticText(self.randomPanel, label="Teddy Task is awaiting your decision", pos= (1, 140))
        

        self.notebookOverview.InsertPage(0, self.randomPanel, "RandomizeTask")


        self.notebookOverview.InsertPage(1, self.taskPanel, "Insert Task")
        
        self.taskPanel.SetSizer(self.taskWrapper)

        
        
        self.Show(True)
        
    

    def insertTask(self, taskInserted):
        self.taskListBox.Insert(taskInserted.taskName, len(tasks)-1)
        
    
    def deleteTask(self, event):
        taskToDelete = self.taskListBox.GetSelection()

        if taskToDelete != wx.NOT_FOUND:
            tasks.pop(taskToDelete)
            self.taskListBox.Delete(taskToDelete)
        else:
            self.resultText.Label = "Not even Teddy has the power to delete nothing"

    
    def drawRandomTask(self, event):
        if len(tasks) < 1:
            self.resultText.Label = "Teddy has no task for you..."
        else:
            randomTaskIndex = random.randint(0, len(tasks)-1)

            teddyText = "Teddy task says that you should... " + tasks[randomTaskIndex].getTaskWithMethod()

            finalTeddyText = ""

            for signIndex in range(0, len(teddyText)):
                finalTeddyText += teddyText[signIndex]
                if signIndex % 60 == 59:
                    finalTeddyText += "\n"
            
        


            self.resultText.Label = finalTeddyText



        
    def saveTasks(self, event):
        jsonArray = []
        for task in tasks:
            jsonArray.append(task.exportJSON())
        
        with open ("tasks.json", "w") as JSONFile:
            JSONFile.write(json.dumps(jsonArray, indent=2))
            self.resultText.Label = "Teddy will remember that..."

        



    def addTaskClick(self, event):
        taskNameStr = self.taskNameInput.GetValue()
        
        taskMethodsList = []

        if self.methodCheckCompletable.GetValue():
            taskMethodsList.append("Do")
        
        if self.methodCheckList.GetValue():
            taskMethodsList.append("Write 5 key sentences about")
        
        if self.methodCheckWords.GetValue():
            taskMethodsList.append("Write 400 words about")

        if self.methodCheckW3.GetValue():
            taskMethodsList.append("Complete 3 or more pages (usually on W3) about")

        if self.methodCheckProgram.GetValue():
            taskMethodsList.append("Make a program about")
        
        if self.methodCheckCustom.GetValue():
            customTaskWindow(task(taskNameStr, taskMethodsList))
        else:
            tasks.append(task(taskNameStr, taskMethodsList))
            self.insertTask(task(taskNameStr, taskMethodsList))

            

    

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
        mainWindow.insertTask(self.taskForCustomization)
        

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
            return self.taskMethods[methodIndex]+": "+self.taskName
        elif len(self.taskMethods) == 1:
            return self.taskMethods[0]+": "+self.taskName
        else:
            return "Do: " + self.taskName
    
    def exportJSON(self):
        JSON = {
            "taskName": self.taskName,
            "taskMethods": self.taskMethods
        }

        #return json.dumps(JSON)
        return JSON
    
    def taskFromJSON(JSON):
        taskPyDict = json.loads(JSON)        

        return task(taskPyDict["taskName"], taskPyDict["taskMethods"])
    
    


tasks = []

root = wx.App()
mainWindow = taskWindow(None, "Task Randomizer")


with open ("tasks.json", "r") as JSONFile:
    taskListJSON = JSONFile.read()
    taskListLoaded = json.loads(taskListJSON)
    for specificTask in taskListLoaded:
        loadedTask = task(specificTask['taskName'], specificTask['taskMethods'])
        tasks.append(loadedTask)
        mainWindow.insertTask(loadedTask)



#Suggestions on feedback: Oddbjørn mentioned that it would be great if the program would display the task chosen as
#a person giving out the assignment, like "Oskar says, you need to write 5 key sentences about utilising user-feedback"

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