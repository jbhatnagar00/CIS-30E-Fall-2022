# CIS-30E-Fall-2022

My project was solving a problem that a patient may face in scheduling and keeping track of their appointment, mainly getting lost in the process of choosing doctors and times. The objective and purpose of the program is streamlining and simplifying the process of creating an appointment with very clear instructions and options for each step. It removes any confusion someone may deal with as a result, avoiding possible time conflicts as one example. The solution/algorithm (goes hand-in-hand) involves a list of doctors being shown after the patient enters their desired date and chooses between scheduling an appointment with a doctor directly, or scheduling one by selecting a doctor based on their specialty first. Then, the doctors available have their schedules shown with what times they are available and what times are unavailable. This makes it extremely easy for the patient to find the right appointment time based on their personal schedule. Once the patient selects the time slot they want to book, a confirmation message is shown. 
The algorithm uses concurrency as another tool to generate and print the list of appointment times at the same time. Modules implemented in the program were random, datetime, and threading. Code from data.py is brought as well. Random randomly generates the appointment schedule (available/occupied times), datetime is used for scheduling and checking doctor availability, threading is used for the main thread, and data.py brings in a list of doctors (dictionary), list of patients (dictionary), and a list of appointments (dictionary). 
Limitations of the program include times being in military time instead of standard time, and the doctor section is not fully fleshed out to show the appointment for a certain doctor after scheduling one as a patient (I wanted to work on this but unfortunately time was cut short due to UCI’s hard deadline and needing my grade earlier to send my transcript). These limitations can be improved by making the schedule show standard time and giving doctors more utility by allowing them to see more information on what is happening on the patient scheduling side. 


Example of program simulation/sequence
### Providing User Inputs
1. First you will be asked to Enter 0 if you are a doctor or 1 if you are a patient
2. Say you enter 1 (being a patient)
3. You will be asked to Enter Patient's Name
4. Say you enter ‘XYZ’
5. You will be asked to Enter Appointment Date
6. Say you enter 11-04-2022
7. Then you will be prompted to Enter 1 to Schedule Appointment ... enter 1
8. Then you will be asked to Enter 1 if you know doctor you are visiting or 2 if you want to select the doctor from his/her specialty
9. Say you enter 1 - you will be presented with list of All Doctors
10. Enter the name of a doctor (must match exactly as shown)
11. Say you enter ‘Dr. Erica’
12. You will be presented with her available times on that date
13. And you will be asked to enter the ID# of the slot available (leftmost column)
14. Say you enter ‘3’
15. Your appointment will be scheduled and a message displayed
### Doctor Views Appointment
1. Start the Program - You get following options
* Enter 0 if you're a Doctor
* Enter 1 if you’re a Patient
* Enter 9 to Quit

You Select '0', you get following prompt

* Welcome Doctor
* Please Enter Doctor's Name to view Appointments:
* You enter: ‘Dr. Nikki Moreno’
* Please Enter Date to view Appointments (MM-DD-YYYY):
* You enter: ‘11-05-2022’
* Appointments Schedule for Dr. Dr. Nikki Moreno on 11-05-2022
Dr. Dr. Nikki Moreno has no scheduled appointments on 11-05-2022
