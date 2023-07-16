from threading import Thread, Event
from utils.menu_utils import menu_combinations, menu_conditions
from utils.keyboard_input import KeyboardListener
import menu_gui
import queue
from time import perf_counter
import itertools
import serial
import serial.tools.list_ports

import time

#these times are in hundreds of miliseconds 1 = 0.1s
LONG_PRESS = 20 #time for a press to be considered long

class ButtonFollower(Thread):
    """On button input this threaded class handles all the events leading to action

    Args:
        Thread (class): Python's Thread class
    """

    def __init__(self, gui_class, input_mode="bluetooth", *args, **kwargs):
        """Init method for the class.
        Inits all the necessary queues and event handlers
        """

        #queue that informs the thread when a new button is pressed/release
        self.new_button_queue = queue.Queue(maxsize=20)
        self.button_input_event = Event()
        #queue that informs the MenuDecoder class when a new action is available
        self.action_queue = queue.Queue(maxsize=20)
        self.read_event = Event()
        #used to kill the thread
        self.kill = Event()
        self.gui_class = gui_class
        self.input_mode = input_mode
        self.key_listener = KeyboardListener()
        
        super().__init__(*args, **kwargs)

    def run(self):
        """Run method from Thread. Starts the thread.
        """
        self.thread = Thread(target=self.button_keeper, args=(self.button_input_event, self.read_event, self.new_button_queue, self.action_queue))
        self.thread.daemon = True
        self.thread.start()

    def button_keeper(self, input_event, read_event, button_list, output_list):
        """Thread main loop. Wakes up when a button is pressed, updates everything and decides if an action is ready

        Args:
            input_event (Event): The event that is set when a new button press is to be read
            read_event (Event): The event that is set to inform MenuDecoder that an action was defined
            button_list (Queue): The input read by the thread when a new button is pressed
            output_list (Queue): The output sent by the thread when an action is set. Read by the MenuDecoder class
        """
        current_buttons_dict = {}
        int_timer = 0
        ser = serial.Serial('/dev/rfcomm0', 9600)

        while not self.kill.is_set():
            '''
            myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]

            if '/dev/rfcomm0' in myports[0]:
                self.gui_class.menu_list["nav"].button_info_blue["bg"] = "blue"
            else:
                self.gui_class.menu_list["nav"].button_info_blue["bg"] = "black"
            '''

            try:
                if self.input_mode == "bluetooth":
                    input_list = ser.readline().decode("utf-8").rstrip('\r\n').split(" ") #only unblocks when there is something to read
                else:
                    input_list = self.key_listener.listen_keyboard()

                if self.kill.is_set():
                    continue

                int_timer = perf_counter() #our timer for the loop. Used in double presses to query the first one
                self.update_press_type(current_buttons_dict, int_timer) #see if a button has been pressed long enough to be "long"

                input_button = int(input_list[0])
                input_state = int(input_list[1])

                if input_button not in current_buttons_dict: #never read button
                    
                    if input_state == 1: #has been pressed
                        
                        int_timer = perf_counter()

                        current_buttons_dict[input_button] = {
                            "time": int_timer,
                            "state": "active",
                            "pair": None,
                            "press_type": "short"
                        }

                        self.check_button_combination_presence(current_buttons_dict)
                    else: #new button, but only captured release -> error

                        print("Button released but not captured")
                else: #existing button
                    if input_state == 1: #just pressed
                        if current_buttons_dict[input_button]["state"] == "inactive":
                            
                            int_timer = perf_counter()
                            self.reset_button(input_button, current_buttons_dict, int_timer)
                            self.check_button_combination_presence(current_buttons_dict)

                        else:
                            print("Button was pressed and released, but release was not caught")
                    else: #released -> leads to action
                        if current_buttons_dict[input_button]["state"] != "inactive":

                            action = self.action_on_release(input_button, current_buttons_dict)

                            if action != None:
                                output_list.put(action)
                                read_event.set()

                        else:
                            print("button was released but press was never caught")
            except Exception as e:
                print(e)            

    def update_press_type(self, buttons_dict, present_timer):
        """If a button has been pressed long enough, change its press type to "long"

        Args:
            buttons_dict (dict): Dictionary with the current state of the buttons
            present_timer (float): Current time for comparison
        """

        for button in buttons_dict:
            if buttons_dict[button]["state"] != "inactive":
                if present_timer - buttons_dict[button]["time"] >= LONG_PRESS:
                    buttons_dict[button]["press_type"] = "long"

    def reset_button(self, button, buttons_dict, timer):
        """When a button is pressed after being inactive, resets the status

        Args:
            button (int): The button being pressed
            buttons_dict (dict): Dictionary with the current state of the buttons
            timer (float): Current time
        """

        buttons_dict[button]["time"] = timer
        buttons_dict[button]["state"] = "active"
        buttons_dict[button]["pair"] = None
        buttons_dict[button]["press_type"] = "short"

    def release_button(self, button, buttons_dict):
        """Method for setting button when released

        Args:
            button (int): The button being released
            buttons_dict (dict): Dictionary with the current state of the buttons
        """

        buttons_dict[button]["time"] = -1
        buttons_dict[button]["state"] = "inactive"
        buttons_dict[button]["pair"] = None

    def action_on_release(self, button, buttons_dict):
        """On release, an action usually follows. This method searches which one is correct.

        Args:
            button (int): The button being released
            buttons_dict (dict): Dictionary with the current state of the buttons

        Returns:
            str: The action to perform. None when nothing is to be done.
        """

        if buttons_dict[button]["state"] == "active": #active button is a single press
            #button is sigle action
            press_type = buttons_dict[button]["press_type"]

            self.release_button(button, buttons_dict)

            if button in menu_combinations["single"][press_type][self.gui_class.present_menu][self.gui_class.present_pos]:
                
                conditions_results = self.check_conditions(button, "single", press_type)

                if conditions_results == "ok":
                    return menu_combinations["single"][press_type][self.gui_class.present_menu][self.gui_class.present_pos][button]
                else:
                    return "warning " + conditions_results
            else:
                return "warning ACTION DOESN'T EXIST"


        elif buttons_dict[button]["state"] == "to_release": #pair of this button was already unpressed

            self.release_button(button, buttons_dict)
        
        else: #this button is paired
            
            pair_button = buttons_dict[button]["pair"]

            if buttons_dict[button]["time"] < buttons_dict[pair_button]["time"]: #find which one was pressed first
                pair_combination = (button, pair_button)
            else:
                pair_combination = (pair_button, button)
            
            self.release_button(button, buttons_dict)
            buttons_dict[pair_button]["state"] = "to_release"
            
            if pair_combination in menu_combinations["double"]:

                return menu_combinations["double"][pair_combination]

            else:
                return "warning ACTION DOESN'T EXIST"
    
    def check_conditions(self, button, n_buttons, press_type):
        
        # here we will check if we pass all the necessary conditions
            
        menu_conditions_dict = menu_conditions["single"][press_type][self.gui_class.present_menu][self.gui_class.present_pos]

        if menu_conditions_dict[button]["stream"] != self.gui_class.streaming and  menu_conditions_dict[button]["stream"] != "":

            return "stream should be " + str(menu_conditions_dict[button]["stream"])

        elif menu_conditions_dict[button]["sel_folder"] != self.gui_class.folder_selected and  menu_conditions_dict[button]["sel_folder"] != "":

            return "folder should be " + str(menu_conditions_dict[button]["sel_folder"])

        elif menu_conditions_dict[button]["in_perf"] != self.gui_class.in_perf and  menu_conditions_dict[button]["in_perf"] != "":

            return "performance shoud be " + str(menu_conditions_dict[button]["in_perf"])

        elif menu_conditions_dict[button]["play"] != self.gui_class.playing and  menu_conditions_dict[button]["play"] != "":

            return "playing shoud be " + str(menu_conditions_dict[button]["play"])
        
        elif menu_conditions_dict[button]["record"] != self.gui_class.recording and  menu_conditions_dict[button]["record"] != "":

            return "recording shoud be " + str(menu_conditions_dict[button]["record"])
        
        else:
            return "ok"

    def check_button_combination_presence(self, buttons_dict):
        """On new button press, checks if a new combination is present (for double button action)

        Args:
            buttons_dict (dict): Dictionary with the current state of the buttons
        """

        check_list = [button for button in buttons_dict if buttons_dict[button]["state"] == "active"]
        check_list_ordered = sorted(check_list, key=lambda x: buttons_dict[x]["time"])
        final_combinations = list(itertools.combinations(check_list_ordered, 2))

        for combination in final_combinations:
            buttons_dict[combination[0]]["state"] = "paired"
            buttons_dict[combination[1]]["state"] = "paired"

            buttons_dict[combination[0]]["pair"] = combination[1]
            buttons_dict[combination[1]]["pair"] = combination[0]              


class MenuDecoder(menu_gui.MenuGUI):
    """General class for decoding input from an menu controller

    Args:
        Thread (class): Python's Thread class
    """

    def __init__(self, master):
        """Inits the class. Defines the used queues and event handlers
        """
        #the raw inputs from the thread that reads the glove
        self.raw_input_queue = queue.Queue(maxsize=20)
        #to kill the thread
        self.kill = Event()
        #to inform the main thread we want to kill this one (it has to be done from outside the class)
        self.to_join = False
        super().__init__(master)

        #inits the ButtonFollower thread
        self.counter_thread = ButtonFollower(self)

        #DELETE
        self.current_folder = "./shared_low_res/"
 

    def run(self):
        """Method that starts the threads.
        """
        self.thread = Thread(target=self.receive_action, args=(self.counter_thread.read_event, self.counter_thread.action_queue))
        self.thread.daemon = True
        self.thread.start()

        self.counter_thread.start()

    def receive_action(self, read_event, action_queue):
        """Main thread method. Receives an action after a button release.

        Args:
            read_event (Event): Event handler that informs the thread when to run
            action_queue (Queue): Queue from Button Follower that has the action
        """

        while not self.kill.is_set():
            read_event.wait()#wait until something needs to be done
            
            if self.tcp_kill.is_set(): #join sequence
                
                self.kill.set()
                self.counter_thread.kill.set()
                self.close_tcp()
                continue

            while not action_queue.empty():#to read all that could be there

                action = action_queue.get()

                if action in self.menu_list: #we want to change menu
                    if self.joystick_mode[0] == False:
                        self.change_to_menu(action)
                elif "warning" in action:
                    self.show_popup(text=action)
                else:
                    # then read from the dictionary that has the methods
                    if self.joystick_mode[0] == True: #we are updating a given button through joystick
                        # left and right dont work
                        # we only accept up and down. Also updates on the
                        if action != "left" and action != "right":
                            self.menu_list[self.present_menu].message_for_action = action
                            self.active_joystick_button.invoke()

                    else:       
                        # this IF basicly detects loopr and loopl actions when not on current_value
                        if action in self.menu_list[self.present_menu].button_dict[self.present_pos].keys():
                            self.menu_list[self.present_menu].message_for_action = action
                            self.menu_list[self.present_menu].button_dict[self.present_pos][action].invoke()
                        else:
                            self.show_popup(text=action + " not available")

            read_event.clear() #to block the thread once again
       