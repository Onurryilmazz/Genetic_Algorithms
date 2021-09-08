import random as rnd
import prettytable
POPULATION_SIZE = 10
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1

class Department:
    
    def __init__(self,name,courses):
        self._name = name
        self._courses = courses

    def get_name(self):
        return self._name

    def get_courses(self):
        return self._courses

class Class:
    
    def __init__(self,id,dept,course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None 
        self._room = None

    def get_id(self):
        return self._id

    def get_dept(self):
        return self._dept

    def get_course(self):
        return self._course

    def get_instructor(self):
        return self._instructor

    def get_meetingTime(self):
        return self._meetingTime

    def get_room(self):
        return self._room

    def set_instructor(self, instructor):
        self._instructor = instructor

    def set_room(self, room):
        self._room = room

    def set_meetingTime(self, meetingTime):
        self._meetingTime = meetingTime


    def __str__(self) -> str:
        return str(self._dept.get_name()) + ',' + str(self._course.get_number()) + ',' + \
               str(self._room.get_number()) + ',' + str(self._instructor.get_id()) + ',' + str(self._meetingTime.get_id())

class Course:
    
    def __init__(self,number,name,instructer,maxNumberOfStudents):
        self._number = number
        self._name = name
        self._instructer = instructer
        self._maxNumberOfStudents = maxNumberOfStudents

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_instructer(self):
        return self._instructer

    def get_maxNumbOfStudents(self):
        return self._maxNumberOfStudents

    def __str__(self):
        return self._name

class Instructer:
    
    def __init__(self,id,name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name

class Room:
    
    def __init__(self,number,seatingCapacity):
        self._number=number
        self._seatingCapacity = seatingCapacity

    def get_number(self):
        return self._number

    def get_seatingCapacity(self):
        return self._seatingCapacity

class MeetingTime:
    
    def __init__(self,id,time):
        self._id = id
        self._time = time

    def get_id(self):
        return self._id

    def get_time(self):
        return self._time

class Data:
    ROOMS = [['1B',100],['1A',100],['1C',100]]
    MEETING_TIMES = [['MT1','MWF 09:00 - 10:00'],
    ['MT2','MWF 09:00 - 10:00'],
    ['MT4','TTH 10:30 - 12:00'],
    ['MT3','TTH 09:00 - 10:30']]

    INSTRUCTORS = [['I1','JAMES'],
    ['I2','ONUR'],
    ['I3','MURAT'],
    ['I4','YILMAZ']]

    def __init__(self):
        self._rooms = []; self._meetingTimes = []; self._instructors = []

        for i in range(len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0],self.ROOMS[i][1]))

        for i in range(len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0],self.MEETING_TIMES[i][1]))

        for i in range(len(self.INSTRUCTORS)):
            self._instructors.append(Instructer(self.INSTRUCTORS[i][0],self.INSTRUCTORS[i][1]))


        course1 = Course("c1","325K",[self._instructors[0],self._instructors[1]],50)
        course2 = Course("c2","320K",[self._instructors[0],self._instructors[1]],50)
        course3 = Course("c3","462k",[self._instructors[0],self._instructors[1]],50)
        course4 = Course("c4","464K",[self._instructors[2],self._instructors[3]],50)
        course5 = Course("c5","360C",[self._instructors[3]],50)
        course6 = Course("c6","303K",[self._instructors[0],self._instructors[2]],50)
        course7 = Course("c7","303L",[self._instructors[1],self._instructors[3]],50)

        self._courses = [course1,course2,course3,course4,course5,course6,course7]
        
        dept1 = Department("Math",[course1,course3])
        dept2 = Department("ee",[course2,course3])
        dept3 = Department("phy",[course1,course2])

        self._depts = [dept1,dept2,dept3]
        self._numberOfClasses = 0

        for i in range(len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_rooms(self):
        return self._rooms
        
    def get_meetingTimes(self):
        return self._meetingTimes

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

data = Data()

class Schudela:
   
    def __init__(self):
       self._data = data
       self._classes = []
       self._numOfConflicts = 0
       self._fitness = -1
       self._classNumb = 0
       self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numOfConflicts(self):
        return self._numOfConflicts

    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False

        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(len(depts)):
            courses = depts[i].get_courses()
            for j in range(len(courses)):
                newClass = Class(self._classNumb,depts[i],courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0,len(data.get_meetingTimes()))])
                newClass.set_room(data.get_rooms()[rnd.randrange(0,len(data.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructer()[rnd.randrange(0,len(courses[j].get_instructer()))])
                self._classes.append(newClass)

        return self

    def calculate_fitness(self):
        self._numOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if(classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numOfConflicts += 1

            for j in range(len(classes)):
                if (j >= i):
                    if(classes[i].get_meetingTime()==classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()):
                            self._numOfConflicts += 1

                        if (classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numOfConflicts += 1
                        
        return 1 / (1.0 * (self._numOfConflicts + 1))


    def __str__(self) -> str:
        returnValue = ''
        for i in range(len(self._classes)-1):
            returnValue += str(self._classes[i]) + ','
        
        returnValue += str(self._classes[len(self._classes)-1])

        return returnValue

class Population:
    def __init__(self,size):
        self._size = size
        self._data = data
        self._schudela = []
        for i in range(size):
            self._schudela.append(Schudela().initialize())

    def get_schudeles(self):
        return self._schudela

class GeneticAlgoritm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _mutate_population(self,population):
        for i in range(NUMB_OF_ELITE_SCHEDULES,POPULATION_SIZE):
            self._mutate_schedule(population.get_schudeles()[i])

        return population
    
    def _crossover_population(self,pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schudeles().append(pop.get_schudeles()[i])

        i = NUMB_OF_ELITE_SCHEDULES

        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schudeles()[0]
            schedule2 = self._select_tournament_population(pop).get_schudeles()[0]
            crossover_pop.get_schudeles().append(self._crossover_schedule(schedule1,schedule2))

            i +=1

        return crossover_pop

    def _mutate_schedule(self, mutateSchedule):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schudeles()[i])

        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schudela().initialize()
        for i in range(0,len(crossoverSchedule.get_classes())):
            if(rnd.random()>0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]

            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]

        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schudela().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self,pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schudeles().append(pop.get_schudeles()[rnd.randrange(0,POPULATION_SIZE)])
            i += 1

        tournament_pop.get_schudeles().sort(key = lambda x : x.get_fitness(), reverse = True) 

        return tournament_pop

class DisplayMgr:

    @staticmethod
    def display_input_data():
        print('all data')
        DisplayMgr.display_dept()
        DisplayMgr.display_course()
        DisplayMgr.display_room()
        #DisplayMgr.display_instructor()
        DisplayMgr.display_meeting_times()

    @staticmethod
    def display_dept():
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept','courses'])
        
        for i in range(len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["

            for j in range(len(courses)-1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses)-1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(),tempStr])

        print(availableDeptsTable)

    
    @staticmethod
    def display_course():
        availableCourseTable = prettytable.PrettyTable(['id','course','maxS','ins'])
        courses = data.get_courses()

        for i in range(len(courses)):
            instructors = courses[i].get_instructer()
            tempStr = ""

            for j in range(len(instructors)-1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors)-1].__str__()
            availableCourseTable.add_row(
                [courses[i].get_number(),courses[i].get_name(),str(courses[i].get_maxNumbOfStudents()),tempStr]
            )

        print(availableCourseTable)


    @staticmethod
    def display_instructor():
        availableInstructorTable = prettytable.PrettyTable(['id','ins'])
        instructors = data.get_instructors()

        for i in range(len(instructors)):
            availability = []
            for j in range(len(instructors[i].get_availability())):
                availability.append(instructors[i].get_availability()[j].get_id())
            availableInstructorTable.add_row([instructors[i].get_id(),instructors[i].get_name()])
        print(availableInstructorTable)

    @staticmethod
    def display_room():
        availableRoomsTable = prettytable.PrettyTable(['room','max'])
        rooms = data.get_rooms()
        for i in range(len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()),str(rooms[i].get_seatingCapacity())])

        print(availableRoomsTable)

    @staticmethod
    def display_meeting_times():
        availableMeetingTimeTable = prettytable.PrettyTable(['id','mt'])
        meetingTimes = data.get_meetingTimes()

        for i in range(len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(),meetingTimes[i].get_time()])

        print(availableMeetingTimeTable)

    @staticmethod
    def display_generation(population):
        table1 = prettytable.PrettyTable(['sche','fitnes','classes'])
        schedules = population.get_schudeles()

        for i in range(len(schedules)):
            table1.add_row([str(i+1),round(schedules[i].get_fitness(),3),schedules[i].__str__()])

        print(table1)


display = DisplayMgr()
display.display_input_data()

generation_number = 0
print(generation_number)

population = Population(POPULATION_SIZE)
population.get_schudeles().sort(key=lambda x : x.get_fitness(), reverse=True)
display.display_generation(population)
geneticAlgorithm = GeneticAlgoritm()

while (population.get_schudeles()[0].get_fitness() != 1.0):
    generation_number += 1
    print(generation_number)
    display.display_generation(population)
    population = geneticAlgorithm.evolve(population)
    population.get_schudeles().sort(key=lambda x : x.get_fitness(), reverse=True)
