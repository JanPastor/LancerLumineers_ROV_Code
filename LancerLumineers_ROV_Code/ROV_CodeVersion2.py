import sys
import json 
import time
import pygame
import math #needed for joystick
from pygame.rect import Rect
import widgets
import serial #needed to talk with Arduino

# GUI window setup
sidebarwidth = 220
pygame.init()
pygame.display.set_caption ('ROV Control')
size = width, height = 160+sidebarwidth, 320    #size of GUI

#setup displays in GUI
screen = pygame.display.set_mode(size)
onstatus=widgets.toggleable("Running",sidebarwidth)     #label and size toggle
zslider=widgets.sliderdisplay("Z",75,160)
mleftslider=widgets.sliderdisplay("Leftslider",75,160)
mrightslider=widgets.sliderdisplay("Rightslider",75,160)
temp_display=widgets.display("Temp (C)",sidebarwidth)
th_up_display=widgets.display("Servo Up",sidebarwidth)
th_left_display=widgets.display("Servo Left",sidebarwidth)
th_right_display=widgets.display("Servo Right",sidebarwidth)
claw_display=widgets.display("Claw output",sidebarwidth) # Added 4/14/23 to setup object for claw value displays GUI

#open serial com to Arduino
ser= serial.Serial(port='COM5', baudrate=9600, timeout=.1,dsrdtr=True)         #dsrdtr=True stops Arduino Mega from autoresetting

clawValue = 0 # Initializes claw value to 0;value to store the claw state 

#init joystick
joystick = None
if pygame.joystick.get_count()==0:
    print ('No joystick Detected')
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()  #initalize joystick

#Main Loop
while True:
        # Get input from joystick and keyboard
    pygame.event.pump()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.JOYBUTTONDOWN: 
            if event.button ==0: # Button A; Button ID: 0 used for toggling max thruster status On/Off
                onstatus.toggle()
                # Code block below establishes the incremental range of values for opening and closing the claw. Range can be adjusted for finer servo controls.
            if event.button == 2: # X Button (Opens the claw)
                clawValue -= 10 # set 
                if clawValue < 0: # set minimum value/ Prevents any negative value for the motor direction values. Establishes a floor condition.
                    clawValue = 0 # Resets any negative motor direction values to the minimum value.
            if event.button == 3: # Y Button (Close the claw)
                clawValue += 10   # Increments value for fine tuning control
                if clawValue > 100: # set maximum value (ceiling)
                    clawValue = 100 # If this value is reached, the claw is completely open.
       
        
                
                

# Commands to send ROV
    commands = {} #define python dictionary
    if joystick is not None:
        x=joystick.get_axis(0)#left joystick -1 is left to +1 is right (left thruster)
        y=joystick.get_axis(1) #left joystick -1 is up +1 is down (right thruster)
        z=joystick.get_axis(2) #right joystick x-axis, used for vertical
        claw = joystick.get_button(1)

    if abs(y)<.2: #define a dead zone
        y=0
    if abs(x)<.2: #define a dead zone
        x=0
    if abs(z)<.2: #define a dead zone
        z=0
       
    if onstatus.state: # When the status is toggled to "On" by pressing Button A on the controller: Limits thrust for SURGE direction (forward/backward).
        y=-y*1.414 # gives value of 1 for full thrust forward and backwards
        x=x*1.414 # gives value of 1 for full thrust forward and backwards
            
    #rotate x and y axis of joystick 45 degrees
    x_new=(x*math.cos(math.pi/-4))-(y*math.sin(math.pi/-4)) #horizontal left
    y_new=(x*math.sin(math.pi/-4))+ (y*math.cos(math.pi/-4)) #horizontal right

    #limits joystick values to +/- 1
    if x_new>1:
        x_new=1.0
    if y_new>1:
        y_new=1.0
    if x_new<-1:
        x_new=-1.0
    if y_new<-1:
        y_new=-1.0
           
    #add to dictionary
    #cube gives more control with lower power
    # These are the commands being sent to the Arduino Mega Board 
    commands['tleft']=x_new**3
    commands['tright']=y_new**3
    commands['tup']=-z**3
    commands['claw'] = clawValue # send the claw value
   

    mleftslider.value=commands['tleft'] #assign thruster values to a display
    mrightslider.value=commands['tright']
    zslider.value=commands['tup']

    MESSAGE=json.dumps(commands)#puts python dictionary in Json format
    ser.write(bytes(MESSAGE, 'utf-8'))#byte format sent to arduino
    ser.flush()

    try:
        data = ser.readline().decode("utf-8")#decode into byte from Arduino
        dict_json=json.loads(data)  #data from arduino in dictionary form
        #print(dict_json)
        temp_display.value=dict_json['volt']#assign temp to dispaly
        th_up_display.value=dict_json['sig_up_1']#vertical thruster value from Arduino
        th_left_display.value=dict_json['sig_lf']#vertical thruster value from Arduino
        th_right_display.value=dict_json['sig_rt']#vertical thruster value from Arduino
        claw_display.value=dict_json['claw']#claw value from Arduino
        
        ser.flush()
    except Exception as e:
        print (e)
    pass

#Draw Stuff (Rendering the data as a display for the GUI)
    dheight=onstatus.get_height()
    screen.blit(onstatus.render(),(0,0))
    screen.blit(mleftslider.render(),(0,8*dheight))
    screen.blit(mrightslider.render(),(73, 8*dheight))
    screen.blit(zslider.render(), (146, 8*dheight)) #blitting thruster values
    screen.blit(temp_display.render(),(0,dheight))#blitting temperature values# pick a font you have and set its size
    screen.blit(th_up_display.render(),(0,2*dheight))
    screen.blit(th_left_display.render(),(0,3*dheight))
    screen.blit(th_right_display.render(),(0,4*dheight))
    screen.blit(claw_display.render(),(0,5*dheight)) # display the claw value on the screen

#Label GUI
    myfont=pygame.font.SysFont("cambriacambriamath", 14)# define font
    th_up= myfont.render("Z",0, (230,0,0),(230,230,0)) #render(text, antialias,color,background)
    screen.blit(th_up, (170, 7*dheight))# put the label object on the screen
    th_left = myfont.render("th_left", 1, (230,0,0),(230,230,0))
    screen.blit(th_left, (0, 7*dheight))# put the label object on the screen
    th_right = myfont.render("th_right", 1, (230,0,0),(230,230,0))
    screen.blit(th_right, (70, 7*dheight))# put the label object on the screen

    pygame.display.flip()   #update screen
    time.sleep(0.01)

pygame.quit()
