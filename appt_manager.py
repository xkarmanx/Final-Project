# Appointment Management Application Code

from appointment import Appointment 
from appointment import print_border1
import csv
import os
################################################################################
##                          Create Weekly Calendar                            ##
################################################################################
def create_weekly_calendar(load_appointments=False, appointments_filename='appointments1.csv'):
    appointments = []
    
    # Days of the Week
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # Daily Hours
    start_time_hour = [9, 10, 11, 12, 13, 14, 15, 16]

    for days in days_of_the_week:
        for hours in start_time_hour:
            appointment = Appointment(days, hours)
            appointments.append(appointment)

    if load_appointments:
        load_scheduled_appointments(appointments_filename, appointments)
    
    return appointments
###############################################################################
##                         Load Scheduled Appointments                       ##
###############################################################################
def find_appointment_by_time(appointments, day, start_time_hour):
    for appointment in appointments:
        if appointment.get_day_of_week().lower() == day.lower() and appointment.get_start_time_hour() == start_time_hour:
            return appointment
    return None

def load_scheduled_appointments(filename, appointments):
    try:
        with open(filename, 'r') as file:
            next(file)
            for line in file:
                values = line.strip().split(',')
                day, start_time_hour = values[3], int(values[4])
                appointment = find_appointment_by_time(appointments, day, start_time_hour)
                if appointment:
                    appointment.schedule(values[0], values[1], int(values[2]))
    except FileNotFoundError:
        print(f"File {filename} not found.")
##############################################################################
##                             Print Menu                                   ##
##############################################################################

def print_menu():
    print("")
    print_border1(75, "*")
    print('\t\tJojo\'s Hair Salon Appointment Manager')
    print_border1(75, "*")
    print("")
    print('Select one of the following options: \n1. Schedule an Appointment \n2. Find appointment by name \n3. Print calendar for a specific day \n4. Cancel an appointment \n5. Save all appointments to CSV \n9. Exit the System')
    userInput = input('Enter your selection => ')
    return userInput


##############################################################################
##                        Schedule An Appointment                           ##
##############################################################################

def schedule_an_appointment(appointments):
    day = input("Enter the day: ").capitalize()
    start_time = int(input("Enter the time (in hours): "))
    
    for appointment in appointments:
        if day.lower() in appointment.get_day_of_week().lower() and appointment.start_time_hour == start_time:
                if appointment.get_appt_type() == 0:
                    client_name = input("Enter client name: ")
                    client_phone = input("Enter client phone: ")
                    appt_type = int(input("Enter appointment type (1-4): "))
                    appointment.schedule(client_name, client_phone, appt_type)
                    print("Appointment scheduled successfully!")
                else:
                    print("Appointment not available.")
                return
    print("Invalid day or time.")

##############################################################################
##                        Show Appointments By Name                         ##
##############################################################################

def show_appointments_by_name(appointments):
    client_name = input("Enter client name: ")
    appointment_lookup = []
    for appointment in appointments:
        if appointment.get_client_name().lower() == client_name.lower():
            appointment_lookup.append(appointment)
    if appointment_lookup:
        return appointment_lookup
    else:
        return f'No appointments found for {client_name}'



##############################################################################
##                        Show Appointments By Day                          ##
##############################################################################

def show_appointments_by_day(appointments):
    day_of_week = input("Enter day of the week: ").capitalize()
    daily_appointments = []
    for appointment in appointments:
        if appointment.get_day_of_week().lower() == day_of_week.lower():
            daily_appointments.append(appointment)
    if daily_appointments:
        return daily_appointments
    else:
        return f'No appointments scheduled for {day_of_week}'


##############################################################################
##                          Cancel Appointment                              ##
##############################################################################

def cancel_appointment(appointments):
    client_name = input("Enter client name: ")
    for appointment in appointments:
        if appointment.get_client_name().lower() == client_name.lower():
            print(f'Appointment for {client_name} found. Would you like to cancel the following appointment?: \n{appointment.__str__()}')
            cancel = input('(Y/N)? ')
            if cancel.upper() == 'Y':
                appointment.cancel()
                return 'The appointment has been cancelled. Please call to rebook.'
            else:
                return f'Appointment kept for {client_name}.'
    return f'Appointment not found for {client_name}.'


##############################################################################
##                      Save Scheduled Appointment                          ##
##############################################################################
def save_scheduled_appointments(appointments, filename):
    with open(filename, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        for appointment in appointments:
            csv_writer.writerow(appointment.format_record().split(','))
    print("Write Completed")
##############################################################################
##                      Save All Appointments to CSV                        ##
##############################################################################
#def save_all_appointments_to_csv(appointments, filename):
#    with open(filename, 'w') as file:
 #       file.write("client_name,client_phone,appt_type,day_of_week,start_time_hour\n")
  #      for appointment in appointments:
   #         file.write(appointment.format_record() + '\n')

##############################################################################
##                            Main Program                                  ##
##############################################################################

def main():

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    current_directory = os.getcwd()
    csv_filename = os.path.join(current_directory, "appointments1.csv")

    load_appointments = input("Do you want to load previously booked appointments? (Y/N): ").upper() == 'Y'
    appointments = create_weekly_calendar(load_appointments, "appointments1.csv")
    load_scheduled_appointments("appointments1.csv", appointments)

    while True:
        user_choice = print_menu()

        if user_choice == '1':
            schedule_an_appointment(appointments)
        elif user_choice == '2':
            result = show_appointments_by_name(appointments)
            for appointment in result:
                print(appointment)
        elif user_choice == '3':
            result = show_appointments_by_day(appointments)
            for appointment in result:
                print(appointment)
        elif user_choice == '4':
            result = cancel_appointment(appointments)
            print(result)
        elif user_choice == '5':
            save_scheduled_appointments(appointments, "appointments1.csv")
        elif user_choice == '9':
            break
        else:
            print('Invalid selection, please select from one of the following options')

if __name__ == "__main__":
    main()




