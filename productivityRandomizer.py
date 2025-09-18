import wx
import random
import json


class taskWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 320))
        
        # = wx.Panel(self)
        self.taskWrapper = wx.BoxSizer(wx.VERTICAL)
        
        #We use notebook here to add tabs, later on adding taskpanel and randompanel to it. 
        self.notebookOverview = wx.Notebook(self, style=wx.NB_TOP, name="Task Randomizer Tab Organizer")

        #Panel for adding tasks, we have the taskElements label here because we believed it was necessary 
        self.taskPanel = wx.Panel(self.notebookOverview)
        taskElements = []

        #We make a separate gridsizer here to line up better with the rest of the functions.
        self.taskNameGrid = wx.GridSizer(cols = 2, rows=1, vgap=2, hgap=2)
        self.taskNameLabel = wx.StaticText(self.taskPanel, label="Task Name:")
        self.taskNameGrid.Add(self.taskNameLabel)

        #Text input
        self.taskNameInput = wx.TextCtrl(self.taskPanel, size=(70, 24))
        self.taskNameGrid.Add(self.taskNameInput)
        taskElements.append(self.taskNameGrid)

        #Checkboxes for different methods:
        #Default method, to see if the method is something that can just be done in a relatively short amount of time.
        self.methodCheckCompletable = wx.CheckBox(self.taskPanel, label="Completable")
        taskElements.append(self.methodCheckCompletable)
        
        #Method for writing 5 key sentences about a subject in question
        self.methodCheckList = wx.CheckBox(self.taskPanel, label="5 Key Sentences")
        taskElements.append(self.methodCheckList)

        #Method for writing a 400 word page about the subject in question
        self.methodCheckWords = wx.CheckBox(self.taskPanel, label="400 words")
        taskElements.append(self.methodCheckWords)

        #Method for completing 3+ pages on the W3 site of the subject.
        self.methodCheckW3 = wx.CheckBox(self.taskPanel, label="Complete 3+ pages (W3)")
        taskElements.append(self.methodCheckW3)
        
        #Method for working on making a program that involves the subject.
        self.methodCheckProgram = wx.CheckBox(self.taskPanel, label="Make Program")
        taskElements.append(self.methodCheckProgram)

        #Method for writing your own custom method if the existing checkboxes aren't enough
        self.methodCheckCustom = wx.CheckBox(self.taskPanel, label="Custom")
        taskElements.append(self.methodCheckCustom)
        
        #Button that adds a task to the list. 
        self.addTaskButton = wx.Button(self.taskPanel, label="Add Task")
        self.Bind(wx.EVT_BUTTON, self.addTaskClick, self.addTaskButton)
        taskElements.append(self.addTaskButton)
        

        #We establish the gridsizer here and add all the elements from the taskelements array immediately.
        #This is primarily because it allows us to establish the amount of rows already ready.
        self.taskSizer = wx.GridSizer(cols=1, rows=len(taskElements)+1, vgap=3, hgap=3)

        self.taskSizer.AddMany(taskElements)
        self.taskWrapper.Add(self.taskSizer, proportion=0, flag=wx.ALIGN_LEFT)
        #TODO: Make Display Tasks work properly
        
        #Panel for displaying and selecting random tasks and managing them.
        self.randomPanel = wx.Panel(self.notebookOverview)

        #Just some text at the start
        self.randomOverviewLabel = wx.StaticText(self.randomPanel, label="Available Tasks:", pos=(1, 1))
        
        #List box that displays the tasks that the program can choose from.
        self.taskListBox = wx.ListBox(self.randomPanel, size=(450, 85), pos=(1, 20))
        
        #Button to pick a random task
        self.randomizeButton = wx.Button(self.randomPanel, label="Randomize", pos=(1, 110))
        self.Bind(wx.EVT_BUTTON, self.drawRandomTask, self.randomizeButton)
        
        #User can select a task and delete it from both the list and the array
        self.deleteButton = wx.Button(self.randomPanel, label="Delete", pos=(81, 110))
        self.Bind(wx.EVT_BUTTON, self.deleteTask, self.deleteButton)

        #Button that can be pressed to save the current set of tasks to the JSON
        self.saveAllButton = wx.Button(self.randomPanel, label="Save All", pos=(156, 110))
        self.Bind(wx.EVT_BUTTON, self.saveTasks, self.saveAllButton)
        
        #Text that shows which task is selected to the user, and also conveys information where it's relevant.
        self.resultText = wx.StaticText(self.randomPanel, label="Teddy Task is awaiting your decision", pos= (1, 140))
        
        #We want to make the task for randomizing the page the default "index 0", so it has to be added first.
        self.notebookOverview.InsertPage(0, self.randomPanel, "RandomizeTask")

        #The insert task panel can still be made "index 1" and not be the default page by adding it after.
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

            teddyText = f"Teddy task says that you have to... {tasks[randomTaskIndex].getTaskWithMethod()}" 
            
            textWidth = self.GetSize().GetWidth()//6
            
            self.resultText.Label = manageLine(teddyText, textWidth)

        
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
        
        


        



#We make tasks a simple object with a string for a name and an array of strings for methods.
class task():
    def __init__(self, taskName, taskMethods):
        self.taskName = taskName
        self.taskMethods = taskMethods
        
    #Picks a random of the methods made for the tasks, defaults to the completable option
    def getTaskWithMethod(self):
        #Picks a random of the available tasks if there's more than 1.
        if len(self.taskMethods) > 1:
            methodIndex = random.randint(0, len(self.taskMethods)-1)
            return self.taskMethods[methodIndex]+": "+self.taskName
        #If there's only 1 task, it will just pick the one available
        elif len(self.taskMethods) == 1:
            return self.taskMethods[0]+": "+self.taskName
        #Otherwise, it defaults to just doing the task
        else:
            return "Do: " + self.taskName
    
    #Function that compresses the information of the task into a python dictionary so it's ready to be dumped into JSON.
    def exportJSON(self):
        JSON = {
            "taskName": self.taskName,
            "taskMethods": self.taskMethods
        }

        return JSON

#Function that puts a character limit (lineSplitCharacters) on lines in a string(inText).
def manageLine(inText, lineSplitCharacters):
    #splitting up the text by words
    splitText = inText.split()

    #Putting the first word into the first line of the out-string
    textLines = [splitText[0]]

    #splitting up the string into different lines in a list.
    textIndex = 0
    for wordIndex in range(1, len(splitText)):
        if len(textLines[textIndex] + " " + splitText[wordIndex]) > lineSplitCharacters:
            textIndex += 1
            textLines.append(splitText[wordIndex])
        else:
            textLines[textIndex] += " " + splitText[wordIndex]

    #Combining the lines from the list into a finished string product that is then returned.
    outText = textLines[0]
    for line in textLines[1:]:
        outText += "\n" + line
    return outText

#We make the array for the listed tasks
tasks = []

root = wx.App()
mainWindow = taskWindow(None, "Task Randomizer")


#We try to read the file and add tasks from it, but if the file doesn't exist, then it makes the JSON file with an empty array. 
try:
    with open ("tasks.json", "r") as JSONFile:
        taskListJSON = JSONFile.read()
        taskListLoaded = json.loads(taskListJSON)
        for specificTask in taskListLoaded:
            loadedTask = task(specificTask['taskName'], specificTask['taskMethods'])
            tasks.append(loadedTask)
            mainWindow.insertTask(loadedTask)
except:
    with open ("tasks.json", "w") as JSONFile:
        JSONFile.write(json.dumps([], indent=2))


#Suggestions on feedback: Oddbjørn mentioned that it would be great if the program would display the task chosen as
#a person giving out the assignment, like "Oskar says, you need to write 5 key sentences about utilising user-feedback"

root.MainLoop()

