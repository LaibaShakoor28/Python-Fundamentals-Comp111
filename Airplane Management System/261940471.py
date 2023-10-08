# Function to load data from the text file and convert it to a dictionary
global flightsDict

def loadDataFromFile():
    loaded_flights = {}
    try:
        with open('flights_data.txt', 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                flight_name = lines[i].strip()
                i += 1
                seat_matrix = []

                while i < len(lines) and not lines[i].strip().isdigit():
                    row_data = lines[i].strip().split()
                    seat_matrix.append(row_data)
                    i += 1

                arrival_time = ""  # Initialize arrival_time
                departure_time = ""  # Initialize departure_time

                # Check if there are lines for arrival and departure times
                if i < len(lines):
                    arrival_time = lines[i].strip()
                    i += 1

                if i < len(lines):
                    departure_time = lines[i].strip()
                    i += 1

                loaded_flights[flight_name] = {
                    'seats': seat_matrix,
                    'arrival_time': arrival_time,
                    'departure_time': departure_time
                }
                i+=1
    except FileNotFoundError:
        return {}
    return loaded_flights

def saveDataInFile():
    with open('flights_data.txt', 'w') as file:
        for flight_name, flight_data in flightsDict.items():
            file.write(flight_name + "\n")
            seat_matrix = flight_data['seats']
            for row in seat_matrix:
                file.write(" ".join(row) + "\n")
            file.write(str(flight_data['arrival_time']) + "\n")
            file.write(str(flight_data['departure_time']) + "\n\n")

flightsDict = loadDataFromFile() # it will load all data from file and store in this variable as dictionary

def display_seat_matrix(flight_name, seat_matrix):
    print("FLIGHT: "+flight_name)
    if 'seats' in seat_matrix:
        actual_seat_matrix = seat_matrix['seats']
    else:
        actual_seat_matrix = []  # Default to an empty matrix if 'seats' key is missing

    num_rows = len(actual_seat_matrix)
    if num_rows > 0:
        seats_per_row = len(actual_seat_matrix[0])
    else:
        seats_per_row = 0
    print(f"{' ':<6}", end='')
    column_headers = ['A', 'B', 'C', 'D']
    for col_header in column_headers[:seats_per_row]:
        print(f"{col_header:^3}", end='')
    print()

    row_num = 1
    arrival_time = ""
    departure_time = ""
    for row in actual_seat_matrix:
        if row_num > 4:
            if arrival_time == "":
                arrival_time = row[0]
            else:
                departure_time = row[0]
        else:
            print("Row{:<5}".format(row_num), end='')
            for seat in row:
                print("{:^3}".format(seat), end='')
            print()
        row_num += 1

    # Display arrival and departure times
    print("Arrival time: "+ str(seat_matrix["arrival_time"]))
    print("Departure time: "+ str(seat_matrix['departure_time']))

    # Add an extra line for separation
    print()

def addFlight():
    print("Available flights already:")
    number = 1
    for flight_name, seat_matrix in flightsDict.items():
        print(f"    {number} .Flight: {flight_name}")
        number+=1
    while True:
        newFlightName = input("Enter the new Flight Name to add: ")
        if newFlightName.strip() in flightsDict:
            print("\nThe flight with the same name exist already, try with a differnt name. Thanks!\n")
        else:
            while True:
                try:
                    arrival_time = int(input("Enter the arrival time in 24-hour format (numeric from 0 to 24): "))
                    departure_time = int(input("Enter the departure time in 24-hour format (numeric from 0 to 24): "))
                    # Check if the entered times are within the valid range (0 to 24)
                    if 0 <= arrival_time <= 24 and 0 <= departure_time <= 24:
                        break
                    else:
                        print("Please enter valid times between 0 and 24.")
                except ValueError:
                    print("Please enter valid numeric times in 24-hour format.")
            # adding new flight details into my dictionary
            num_rows = 4
            #columns
            seats_per_row = 4
            #now will add flights with all empty seats first (-)
            new_flight =[]
            for x in range(num_rows):
                row = []
                for y in range(seats_per_row):
                    seat = "-"
                    row.append(seat)
                new_flight.append(row)

            flightsDict[newFlightName] = {
                'seats': new_flight,
                'arrival_time': arrival_time,
                'departure_time': departure_time
            }
            #flightsDict[newFlightName] = new_flight_details
            print("\nThe Flight "+newFlightName+" has been added successfully\n")
            saveDataInFile()
            break



def modifyFlight():
    global flightsDict
    print("Available flights for modification:")
    number = 1
    for flight_name, _ in flightsDict.items():
        print(f"{number}. {flight_name}")
        number += 1
    while True:
        try:
            flight_to_modify = input("Enter the name of the flight to modify: ")
            if flight_to_modify not in flightsDict:
                print("Flight not found. Please enter a valid flight name.")
                continue
            print("1. Modify FLight Name")
            print("2. Modify Arrival time")
            print("3. Modify departure time")
            print("4. Exit")
            while True:
                correspondingNumber = input("Enter the corresponding number from above options: ")
                if correspondingNumber == "1":
                    new_flight_name = input("Enter the new flight name: ")
                    flightsDict[new_flight_name] = flightsDict.pop(flight_to_modify)
                    saveDataInFile()
                    print(f"{flight_to_modify} has been renamed to {new_flight_name}.")
                    break
                elif correspondingNumber == "2":
                    new_arrival_time = input("Enter the new arrival time in 24-hour format: ")
                    flightsDict[flight_to_modify]["arrival_time"] = new_arrival_time
                    saveDataInFile()
                    print(f"Arrival time for {flight_to_modify} has been updated to {new_arrival_time}.")
                    break
                elif correspondingNumber == "3":
                    new_departure_time = input("Enter the new departure time in 24-hour format: ")
                    flightsDict[flight_to_modify]["departure_time"] = new_departure_time
                    print(f"Departure time for {flight_to_modify} has been updated to {new_departure_time}.")
                    saveDataInFile()
                    break
                elif correspondingNumber == "4":
                    print("Exiting the modification menu.")
                    break
        except:
            pass
        break


def removeFlight():
    global flightsDict
    print("Available flights for deletion: ")
    number = 1
    for flight_name, _ in flightsDict.items():
        print(f"{number}. {flight_name}")
        number += 1
    while True:
        try:
            flight_to_delete = input("Enter the name of the flight to delete: ")
            if flight_to_delete not in flightsDict:
                print("Flight not found. Please enter a valid correspon.")
                continue
            confirmation = input(f"Are you sure you want to delete {flight_to_delete}? (yes/no): ").strip().lower()
            if confirmation == "yes":
                # Delete the flight from the dictionary
                del flightsDict[flight_to_delete]
                # Save the updated data to the file
                saveDataInFile()
                print(f"{flight_to_delete} has been deleted successfully.")
                flightsDict = loadDataFromFile()
            else:
                print(f"{flight_to_delete} was not deleted.")
            break
        except:
            print("\nDeletion canceled.")
            break

def adminInterface(admin):
   print("Welcome "+admin +": ")
   print("   1. Add a flight")
   print("   2. Modify a flight")
   print("   3. Remove a flight")
   while True:
    correspondingNumber = input("Enter the corresponding number: ")
    if correspondingNumber == "1":
        addFlight()
        break
    elif correspondingNumber == "2":
        modifyFlight()
        break
    elif correspondingNumber == "3":
        removeFlight()
        showFlights()
        break
    else:
        print("Please select number only from above options, Thanks!")

def userInterface(user):
     print("Welcome "+user +": ")
     print("   1. Book a Ticket")
     print("   2. Cancel e Booking")
     print("   3. Show Flights")
     while True:
        correspondingNumber = input("Enter the corresponding number: ")
        if correspondingNumber == "1":
            bookTicket()
            break
        elif correspondingNumber =="2":
            cancelBooking()
            break
        elif correspondingNumber =="3":
            showFlights()
            print("\nseat layout for selected flight: \n")
            for flight_name in flightsDict.keys():
                #print(flight_name)
                display_seat_matrix(flight_name, flightsDict[flight_name])
            break
     

def bookTicket():
    global flightsDict
    showFlights()
    selected_flight = ""
    while True:
        selected_flight = input("Enter the name of the flight you want to book: ")
        if selected_flight not in flightsDict:
            print("Flight not found. Please enter a valid flight name.")
            continue
        else:
            break
    print(f"Seat layout for {selected_flight}:")
    display_seat_matrix(selected_flight, flightsDict[selected_flight])
    while True:

        seat_indices = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        row_num = int(input("Enter the row number (1-4): "))
        if row_num < 1 or row_num > 4:
            print("Invalid row number. Please enter a number between 1 and 4.")
            continue
        seat_choice = input("Choose a seat (A/B/C/D): ").upper()
        if seat_choice not in ['A', 'B', 'C', 'D']:
            print("Invalid seat choice. Please choose A, B, C, or D.")
            continue
        # Convert seat choice to an index
        seat_index = seat_indices.get(seat_choice)
        # Check if the seat is already booked
        if flightsDict[selected_flight]['seats'][row_num - 1][seat_index] == 'X':
            print("Seat already booked. Please choose another seat.")
            continue
        # Book the seat ('X' indicates a booked seat)
        flightsDict[selected_flight]['seats'][row_num - 1][seat_index] = 'X'
        print(f"\nSeat {seat_choice} in Row {row_num} has been successfully booked.\n")
        saveDataInFile()
        print("\nseat layout for selected flight: \n")
        display_seat_matrix(selected_flight, flightsDict[selected_flight])
        break


def cancelBooking():
    global flightsDict
    showFlights()
    selected_flight = ""
    while True:
        selected_flight = input("Enter the name of the flight you want to cancel your booking for: ")
        if selected_flight not in flightsDict:
            print("Flight not found. Please enter a valid flight name.")
            continue
        else:
            break

    display_seat_matrix(selected_flight, flightsDict[selected_flight])
    while True:
        seat_indices = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        row_num = int(input("Enter the row number (1-4) of the seat you want to cancel: "))
        if row_num < 1 or row_num > 4:
            print("Invalid row number. Please enter a number between 1 and 4.")
            continue
        seat_choice = input("Choose a seat (A/B/C/D) to cancel: ").upper()
        if seat_choice not in ['A', 'B', 'C', 'D']:
            print("Invalid seat choice. Please choose A, B, C, or D.")
            continue
        seat_index = seat_indices.get(seat_choice)
        
        # Check if the seat is already booked
        if flightsDict[selected_flight]['seats'][row_num - 1][seat_index] == 'X':
            # Mark the seat as available ('-') to cancel the booking
            flightsDict[selected_flight]['seats'][row_num - 1][seat_index] = '-'
            print(f"Booking for Seat {seat_choice} in Row {row_num} on {selected_flight} has been canceled.")
            saveDataInFile()
            display_seat_matrix(selected_flight, flightsDict[selected_flight])
            break
        else:
            print("The selected seat is not booked. Please choose a booked seat to cancel.")


def showFlights():
    global flightsDict
    print("\nAvailable flights:")
    for flight_name in flightsDict.keys():
        print(flight_name)


while True:
    userName = input("\nusername: ")
    password = input("password: ")
    
    if userName == "user" and password == "user123":
        userInterface(userName)
        break
    elif userName =="admin" and password == "admin123":
        adminInterface(userName)
        break
    else:
        print("Error! Wrong username or password. Try Again!")