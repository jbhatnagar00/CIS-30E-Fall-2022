import datetime
from time import sleep, perf_counter
from threading import Thread
from data import lst_appointments, lst_doctors, lst_patients
import random


def view_appointments(name:str, dt:str, usertype=1):  # 1:patient, 0:doctor
    lst = []
    if usertype == 0:
        for lap in lst_appointments:
            if lap["dr_name"] == name and str(lap["appointment"]).split(" ")[0] == dt:
                lst.append(lap)
    elif usertype == 1:
        for lap in lst_appointments:
            if lap["pt_name"] == name and str(lap["appointment"]).split(" ")[0] == dt:
                lst.append(lap)
    else:
        print("Please Enter proper user type\n0 for Doctor, and\n1 for patient")
        return None
    return lst


def view_specialty():
    lst = []
    for ld in lst_doctors:
        if ld["specialty"] not in lst:
            lst.append(ld["specialty"])
    return lst


def view_doctors_by_specialty(speciality):
    lst = []
    for ld in lst_doctors:
        if ld["specialty"] == speciality:
            lst.append(ld)
    return lst


def show_all_doctors():
    print("Here is the List of Doctors in this Facility:")
    for ld in lst_doctors:
        print(ld["name"])


def get_weekday_from_date(dt:datetime):
    day_no = datetime.datetime.date(dt).weekday()
    if day_no == 0:
        return 'Monday'
    elif day_no == 1:
        return 'Tuesday'
    elif day_no == 2:
        return 'Wednesday'
    elif day_no == 3:
        return 'Thursday'
    elif day_no == 4:
        return 'Friday'
    elif day_no == 5:
        return 'Saturday'
    elif day_no == 6:
        return 'Sunday'
    else:
        return None


def check_doctor_availability(dr_name, dt):
    dte = datetime.datetime.strptime(str(dt), "%m-%d-%Y")
    day_asked = get_weekday_from_date(dte)
    days_available = []
    time_available = None
    time_slots_available = []
    for ld in lst_doctors:
        if ld["name"] == dr_name:
            da_list = ld["visit_days"]
            time_available = ld["visit_hours"]
            for dal in da_list:
                days_available.append(dal)
    if day_asked in days_available:
        lst_slots = create_time_slot(time_available, dte)
        return True, lst_slots
    return False, None


def create_time_slot(time_available:str, dt:datetime):  # e.g 9-15
    lst_slots = []
    lst_exact_slots = []
    s_time, e_time = time_available.split("-")
    yr = dt.year
    mn = dt.month
    dat = dt.day
    starting_time = datetime.datetime(yr, mn, dat, int(s_time))
    ending_time = datetime.datetime(yr, mn, dat, int(e_time))
    print("Starting time: ", starting_time)
    print("Ending time: ", ending_time)
    lst_slots.append(starting_time)
    slot = starting_time
    while slot != ending_time:
        slot = slot + datetime.timedelta(minutes=30)
        lst_slots.append(slot)
    n = len(lst_slots)
    rnd_pct = round(random.uniform(0.6, 0.7), 2)
    m = int(n * rnd_pct)
    rand_lst = []
    dx = {}
    for j in range(m):
        rand_lst.append(random.randint(0, n))

    for i, ls in enumerate(lst_slots):
        if i in rand_lst:
            dx[i] = str(ls) + "|" + "DOCTOR IS OCCUPIED"
        else:
            dx[i] = str(ls) + "|" + "AVAILABLE"
    lst_exact_slots.append(dx)
    return lst_exact_slots


def create_appointment(lst_slts, id_of_available_slot, dr_name, pat_name):  # e.g. 3  2022-11-03 10:30:00
    # status = ""
    latest_id = -1
    dx = {}
    for lsap in lst_appointments:
        if int(lsap["id"]) > latest_id:
            latest_id = int(lsap["id"])
    for ls in lst_slts: # ls is a dictionary
        for k, v in ls.items():
            if int(str(k).lstrip().rstrip().strip()) == int(id_of_available_slot):
                original, status = str(v).split("|")
                dt, tm = original.split(" ")
                if status == "AVAILABLE":
                    status = "DOCTOR IS OCCUPIED"
                    new_id = latest_id + 1
                    dx["id"] = new_id
                    dx["dr_name"] = dr_name
                    dx["pt_name"] = pat_name
                    dx["appointment"] = original + "|" + status
                    print("Appointment Created Successfully:")
                    print("---------------------------------------------------------------------")
                    print("Patient {} to see {} on {} at {}".format(pat_name, dr_name, dt, tm))
                    print("---------------------------------------------------------------------")
    if len(dx) > 0:
        lst_appointments.append(dx)


def main():
    while True:
        user_type = int(input("Enter 0 if your are Doctor\nEnter 1 if you are Patient\nEnter 9 to Quit\n"))
        if user_type == 0:
            print("Welcome Doctor")
            dr_name = input("Please Enter Doctor's Name to view Appointments:\n")
            dt = input("Please Enter Date to view Appointments (MM-dd-YYYY):\n")
            lst = view_appointments(dr_name, dt, usertype=0)
            print("Appointments Schedule for Dr. {} on {}".format(dr_name, dt))
            if len(lst) > 0:
                for l in lst:
                    for k, v in l.items():
                        print("{:<2}\t{}".format(k, v))
            else:
                print("Dr. {} has no scheduled appointments on {}".format(dr_name, dt))
            break
        if user_type == 1:
            print("Welcome Patient")
            while True:
                pt_name = input("Please Enter Patient's Name:\n")
                dt = input("Enter Appointment Date (MM-dd-YYYY):\n")
                pt_option = int(input("Please Enter 1 to Schedule an Appointment:\n"))
                if pt_option == 1:
                    print("Scheduling an Appointment ...")
                    appt_option = int(input("Enter 1 to Schedule Appointment using doctor's name:\nEnter 2 to "
                                            "Schedule Appointment selecting doctor from specialty:\n"))
                    if appt_option == 1:
                        show_all_doctors()
                        dr_name = input("Enter Doctor's name:\n")
                        is_doc_available, lst_of_slots = check_doctor_availability(dr_name, dt)
                        if is_doc_available:
                            print("Here is Schedule for {} on {}".format(dr_name, dt))
                            for los in lst_of_slots:
                                for k, v in los.items():
                                    print("{:<5} {}".format(k, v))
                            tm_slt_id = input("Select Id of Time Slot (e.g. 3):\n")
                            create_appointment(lst_of_slots, tm_slt_id, dr_name, pt_name)
                        else:
                            print("Doctor {} is not available on {}".format(dr_name, dt))
                    elif appt_option == 2:
                        splt_lst = view_specialty()
                        print("Specialties Available at this Facility:")
                        for sl in splt_lst:
                            print(sl)
                        selected_specialty = input("Enter chosen Specialty:\n")
                        splt_dr_lst = view_doctors_by_specialty(selected_specialty)
                        print("Here is a list of doctors specializing in {}".format(selected_specialty))
                        for sdl in splt_dr_lst:
                            days = ""
                            for dy in sdl["visit_days"]:
                                days = days + " " + dy
                            print("{:<25} {:<50} {:<15}".format(sdl["name"], days, sdl["visit_hours"]))
                        dr_name = input("Enter the name of Doctor you'd like to visit:\n")
                        is_doc_available, lst_of_slots = check_doctor_availability(dr_name, dt)
                        if is_doc_available:
                            print("Here is Schedule for {} on {}".format(dr_name, dt))
                            for los in lst_of_slots:
                                for k, v in los.items():
                                    print("{:<5} {}".format(k, v))
                            tm_slt_id = input("Select Id of Time Slot (e.g. 3):\n")
                            create_appointment(lst_of_slots, tm_slt_id, dr_name, pt_name)
                        else:
                            print("Doctor {} is not available on {}".format(dr_name, dt))
                    else:
                        print("Invalid Option")
                    break
                else:
                    print("Invalid Input")
                break
            break
        if user_type == 9:
            exit(0)


if __name__ == "__main__":
    threads = []
    for n in range(3):  # the loop will be executed 9 times
        t = Thread(target=main())
        threads.append(t)
        t.start()

    # while True:
    #     user_type = int(input("Enter 0 if your are Doctor\nEnter 1 if you are Patient\n"))
    #     if user_type == 0:
    #         print("Welcome Doctor")
    #         dr_name = input("Please Enter Doctor's Name to view Appointments:\n")
    #         dt = input("Please Enter Date to view Appointments:\n")
    #         lst = view_appointments(dr_name, dt, usertype=0)
    #         print("Appointments Schedule for Dr. {} on {}".format(dr_name, dt))
    #         if len(lst) > 0:
    #             for l in lst:
    #                 for k, v in l.items():
    #                     print("{:<2}\t{}".format(k, v))
    #         else:
    #             print("Dr. {} has no scheduled appointments on {}".format(dr_name, dt))
    #         break
    #     if user_type == 1:
    #         print("Welcome Patient")
    #         while True:
    #             pt_name = input("Please Enter Patient's Name:\n")
    #             dt = input("Enter Appointment Date:\n")
    #             pt_option = int(input("Please Enter 1 to Schedule an Appointment:\n"))
    #             if pt_option == 1:
    #                 print("Scheduling an Appointment ...")
    #                 appt_option = int(input("Enter 1 to Schedule Appointment using doctor's name:\nEnter 2 to "
    #                                         "Schedule Appointment selecting doctor from specialty:\n"))
    #                 if appt_option == 1:
    #                     show_all_doctors()
    #                     dr_name = input("Enter Doctor's name:\n")
    #                     is_doc_available, lst_of_slots = check_doctor_availability(dr_name, dt)
    #                     if is_doc_available:
    #                         print("Here is Schedule for {} on {}".format(dr_name, dt))
    #                         for los in lst_of_slots:
    #                             for k, v in los.items():
    #                                 print("{:<5} {}".format(k, v))
    #                         tm_slt_id = input("Select Id of Time Slot (e.g. 3):\n")
    #                         create_appointment(lst_of_slots, tm_slt_id, dr_name, pt_name)
    #                     else:
    #                         print("Doctor {} is not available on {}".format(dr_name, dt))
    #                 elif appt_option == 2:
    #                     pass
    #                 else:
    #                     print("Invalid Option")
    #                 break
    #             else:
    #                 print("Invalid Input")
    #             break
    #         break
