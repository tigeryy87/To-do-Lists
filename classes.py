"""Final Project (Command line task manager)

Tiger Chen
"""


import pickle, re
from datetime import datetime
from tabulate import tabulate
from operator import itemgetter

class Task:
    """Representation of a task
  
    Attributes:
              - created - date
              - completed - boolean
              - name - string
              - unique id - number
              - priority - int value of 1, 2, or 3; 1 is default
              - due date - date, this is optional
              - completed date - date
    Methods:
              - age - calculate the age of the tasks since created
              - string_to_date - convert string to datetime object
    """
    def __init__(self, name, id, priority = 1, date = None):
        '''intialize values'''
        self.name = name
        self.priority = priority
        self.id = id 
        self.created = datetime.now().astimezone()
        self.due_date = self.string_to_date(date) if date != None else '-' 
        self.completed = False
        self.completed_date = '-'

    def age(self):
        '''calculate the age'''
        start_day = self.created
        due = datetime.now().astimezone()
        self.age_diff = (due - start_day).days
        return self.age_diff

    def string_to_date(self, date):
        '''convert the input string into datetime object for calculating age'''
        match = re.findall(r'^\d{1,2}[\-\/]\d{1,2}[\-\/]\d{4}$', date)
        if match != []:
            date_time_obj = datetime.strptime(match[0], '%m/%d/%Y')
            return date_time_obj
        else:
            raise TypeError("Incorrect formate for due date, should be MM/dd/YYYY, -h for more information")

    def __str__(self):
        create_date = datetime.strftime(self.created, "%m/%d/%Y")
        return "%s | ID: %d | Created: %s | Priority: %s" %(self.name, self.id, create_date, self.priority)
        

class Tasks:
    """A list of `Task` objects.
    
    Attributes:
                - tasks - list of task
            
    Methods:
                - pickle_tasks - pickle task list to file
                - list - list incompleted tasks
                - sort_list - sort by due date and priority
                - report - list all tasks
                - report - list all tasks
                - query - list all search term tasks
                - add - add a new task into the list
                - delete - remove the specific task
                - done - mark the task to completed   
    """
    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        # if the file exist, open it
        # else create tasks
        try:
            with open('.todo.pickle', 'rb') as f:
                self.tasks = pickle.load(f)
        except:
            self.tasks = []

    def pickle_tasks(self):
        """Pickle your task list to a file"""
        with open('.todo.pickle', 'wb') as f:
            pickle.dump(self.tasks, f)

    # Complete the rest of the methods, change the method definitions as needed
    def sort_list(self, tables):
        '''sorted by due date and priority'''
        sort_date = sorted(tables, key=lambda x: x[2], reverse=True)
        date_list = []
        no_date_list = []
        for list in sort_date:
            if list[2] != '-':
                date_list.append(list)
            else:
                no_date_list.append(list)
        sort_priority = sorted(no_date_list, key=itemgetter(3))
        for i in sort_priority:
            date_list.append(i)
        return date_list

    def list(self):
        '''list incompleted tasks'''
        tables = []
        for task in self.tasks:
            if task.completed == False:
                tables.append([str(task.id), str(task.age()) + 'd', str(task.due_date), int(task.priority), task.name])           
        print(tabulate(self.sort_list(tables), headers = ['ID', 'Age', 'Due Date', 'Priority', 'Task']))

    def report(self):
        '''list all tasks'''
        tables = []
        for task in self.tasks:
            tables.append([str(task.id), str(task.age()) + 'd', str(task.due_date), str(task.priority), task.name, str(task.created), str(task.completed_date)])           
        print(tabulate(self.sort_list(tables), headers = ['ID', 'Age', 'Due Date', 'Priority', 'Task', 'Created', 'Completed']))

    def query(self, word):
        '''list all search term tasks'''
        query_list = []
        for query in word:
            for task in self.tasks:
                if query.lower() in task.name.lower():
                    query_list.append(task)
        tables = []
        for task in query_list:
           tables.append([str(task.id), str(task.age()) + 'd', str(task.due_date), int(task.priority), task.name])           
        print(tabulate(self.sort_list(tables), headers = ['ID', 'Age', 'Due Date', 'Priority', 'Task']))

    def add(self, name, priority, date):
        '''add a new task into the list'''
        priority = 1 if priority == None else priority
        if len(self.tasks) == 0:
            id = 1
        else: 
            id = self.tasks[len(self.tasks) - 1].id + 1 
        self.tasks.append(Task(name, id, priority, date))
        print("Created task " + str(id))

    def delete(self, id):
        '''delete the task for specific id'''
        for i in range(0, len(id)):
            delete_list = list(filter(lambda x: x.id in id, self.tasks))
            for element in delete_list:
                self.tasks.remove(element)
            print("Deleted task " + str(id[i]))
        
    def done(self, id):   
        '''complete the specific task'''
        completed_time = datetime.now().astimezone()
        for i in range(0, len(id)):
            for task in self.tasks:
                if task.id == id[i]:
                    task.completed = True
                    task.completed_date = completed_time
                    print("Completed task " + str(id[i]))
                    break
