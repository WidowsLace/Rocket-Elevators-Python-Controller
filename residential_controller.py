#since both the tests do basically the same thing, ill be explaining this one a little bit more simply. The class column is to 
class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id 
        self.status = "online"
        self.numOfFloors = _amountOfFloors
        self.numOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

        self.fillElevatorList(self.numOfElevators, self.numOfFloors)
        self.fillCallButtonList(self.numOfFloors)
    
    def fillElevatorList(self, numOfElevators, numOfFloors):
        elevId = 1
        i = 0
        while i < numOfElevators:
            elevator = Elevator(elevId, numOfFloors)
            self.elevatorList.append(elevator)
            elevId += 1
            i += 1
    def fillCallButtonList(self, numOfFloors):
        buttonId = 1
        floor = 1
        i = 0

        while i < numOfFloors:
            if floor == 1:
                self.callButtonList.append(CallButton(buttonId, floor, "up"))
            elif floor < numOfFloors and floor != 1:
                self.callButtonList.append(CallButton(buttonId, floor, "up"))
                buttonId += 1
                self.callButtonList.append(CallButton(buttonId, floor, "down"))
            else:
                self.callButtonList.append(CallButton(buttonId, floor, "down"))
            buttonId += 1
            floor += 1
            i += 1

    def requestElevator(self, requestedFloor, direction):
            chosenElevator = self.findBestElevator(requestedFloor, direction)
            chosenElevator.floorRequestList.append(requestedFloor)
            chosenElevator.move()
            chosenElevator.door.status = "opened"
            return chosenElevator

    def findBestElevator(self, requestedFloor, requestedDirection):
            bestElevator = None
            bestScore = 100
            referenceGap = 10000
            bestElevatorInformation = ""

            for elev in self.elevatorList:
                if requestedFloor == elev.currentFloor and elev.status == "stopped" and requestedDirection == elev.direction:
                    bestElevatorInformation = self.checkIfElevatorIsBetter(1, elev, bestScore, referenceGap, bestElevator, requestedFloor)
                elif elev.currentFloor > requestedFloor and elev.direction == "down" and requestedDirection == elev.direction:
                    bestElevatorInformation = self.checkIfElevatorIsBetter(2, elev, bestScore, referenceGap, bestElevator, requestedFloor)
                elif elev.currentFloor < requestedFloor and elev.direction == "up" and requestedDirection == elev.direction:
                    bestElevatorInformation = self.checkIfElevatorIsBetter(2, elev, bestScore, referenceGap, bestElevator, requestedFloor)
                elif elev.status == "idle":
                    bestElevatorInformation = self.checkIfElevatorIsBetter(3, elev, bestScore, referenceGap, bestElevator, requestedFloor)
                else:
                    bestElevatorInformation = self.checkIfElevatorIsBetter(4, elev, bestScore, referenceGap, bestElevator, requestedFloor)
                bestElevator = bestElevatorInformation["bestElevator"]
                bestScore = bestElevatorInformation["bestScore"]
                referenceGap = bestElevatorInformation["referenceGap"]
          
            return bestElevator
     
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap        
        return {
            "bestElevator": bestElevator,
            "bestScore": bestScore,
            "referenceGap": referenceGap
        }

class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.amountOfFloors = _amountOfFloors
        self.status = "idle"
        self.currentFloor = 1
        self.direction = ""
        self.door = Door(_id)
        self.floorRequestList = []
        self.floorRequestButtonList = []

        self.createFloorRequestButtons(self.amountOfFloors)

    def createFloorRequestButtons(self, _amountOfFloors):
        i = 0
        buttonFloor = 1
        buttonId = 1

        while i < _amountOfFloors:
            floorRequestButton = FloorRequestButton(buttonId, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            buttonId += 1
            i += 1

    def requestFloor(self, requestedFloor):
        self.floorRequestList.append(requestedFloor)
        self.move()
        self.door.status = "opened"

    def move(self):
        element = 0

        while len(self.floorRequestList) != 0:
            for element in self.floorRequestList:
                if self.currentFloor < element:
                    self.direction = "up"
                    if self.door.status == "opened":
                        self.door.status = "closed"
                    self.status = "moving"
                    while self.currentFloor < element:
                        self.currentFloor += 1                    
                    self.status = "stopped"
                
                elif self.currentFloor > element:
                    self.direction = "down"
                    if self.door.status == "opened":
                        self.door.status = "closed"
                    self.status = "moving"
                    while self.currentFloor > element:
                        self.currentFloor -= 1
                    
                    self.status = "stopped"
                self.floorRequestList.pop(0)
        self.status = "idle"

class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = "off"
        self.floor = _floor
        self.direction = _direction
        

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = "off"
        self.floor = _floor

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = "closed"


#===================================================#
#                    PYTHON SCENARIOS               #
#===================================================#

column = Column(1, 10, 2)

# ================ Scenario 1 =====================
def scenario1():
  column.elevatorList[0].currentFloor = 2
  column.elevatorList[1].currentFloor = 6

  elevator = column.requestElevator(3, "up")
  elevator.requestFloor(7)

# scenerio1()
# ============== END Scenario 1 ===================


# ================ Scenario 2 =====================
def scenario2():
  column.elevatorList[0].currentFloor = 10
  column.elevatorList[1].currentFloor = 3

  elevator = column.requestElevator(1, "up")
  elevator.requestFloor(6)
  elevator = column.requestElevator(3, "up")
  elevator.requestFloor(5)
  elevator = column.requestElevator(9, "down")
  elevator.requestFloor(2)

# scenerio2()
# ============== END Scenario 2 ===================

# ================ Scenario 3 =====================

def scenario3():
    column.elevatorList[0].currentFloor = 10
    column.elevatorList[1].currentFloor = 3

    elevator = column.requestElevator(3, "down", 2)
    elevator.requestFloor(6)    
    elevator = column.requestElevator(10, "down")
    elevator.requestFloor(3)
    