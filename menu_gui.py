import tkinter as tk
from tkinter import font as tkFont
from tkinter import Toplevel
import socket

import os

from utils.menu_utils import menu_labels
from threading import Thread, Event, Lock
import alumia_TCP
import time
import cv2
from threading import Thread, Event
import queue
from PIL import Image, ImageTk
import time

MONITOR_ROOT = "PATH_TO_LOW_RES_FOLDER"


class VideoPlayFrame(tk.Frame):

    def __init__(self, parent, upper_class, menu_name):
        super().__init__(parent)
        self.message_for_action = ""
        self.upper_class = upper_class
        self.menu_name = menu_name
        self["bg"] = "black"
        self.button_font = tkFont.Font(size=40, weight='bold')

        self.SIDE_B_W = 1
        self.SIDE_B_H = 100
        self.TOP_B_W = 200
        self.TOP_B_H = self.SIDE_B_W
        self.HAND_B_W = (1/8)*self.TOP_B_W
        self.HAND_B_H = 3*self.SIDE_B_H

        self.button_up = tk.Button(self, text="UP", padx=self.TOP_B_W, pady=self.TOP_B_H, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_down = tk.Button(self, text="DOWN", padx=self.TOP_B_W, pady=self.TOP_B_H, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_right = tk.Button(self, text="RIGHT", padx=self.SIDE_B_W, pady=self.SIDE_B_H, wraplength=1, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_left = tk.Button(self, text="LEFT", padx=self.SIDE_B_W, pady=self.SIDE_B_H, wraplength=1, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)

        self.move_buttons = [self.button_down, self.button_up, self.button_left, self.button_right]

        self.button_hand_1 = tk.Button(self, text="action1", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_2 = tk.Button(self, text="action2", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_3 = tk.Button(self, text="action3", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_4 = tk.Button(self, text="action4", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)

        self.button_hand_1["font"] = self.button_font
        self.button_hand_2["font"] = self.button_font
        self.button_hand_3["font"] = self.button_font
        self.button_hand_4["font"] = self.button_font

        self.button_info_rec = tk.Button(self, text="R", bg='black', borderwidth=0, highlightthickness=0)
        self.button_info_blue = tk.Button(self, text="B", bg='black', borderwidth=0, highlightthickness=0)
        self.button_info_perf = tk.Button(self, text="P", bg='black', borderwidth=0, highlightthickness=0)

        self.button_dummy_2 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_4 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_6 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_7 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_8 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)

        self.button_up.grid(row=0, column=1, columnspan=8, sticky="nesw")
        self.button_down.grid(row=3, column=1, columnspan=8, sticky="nesw")
        self.button_right.grid(row=1, column=9, rowspan=2, sticky="nesw")
        self.button_left.grid(row=1, column=0, rowspan=2, sticky="nesw")

        self.button_hand_1.grid(row=1, column=1, columnspan=2, sticky="nesw")
        self.button_hand_2.grid(row=1, column=3, columnspan=2, sticky="nesw")
        self.button_hand_3.grid(row=1, column=5, columnspan=2, sticky="nesw")
        self.button_hand_4.grid(row=1, column=7, columnspan=2, sticky="nesw")

        self.button_info_rec.grid(row=2, column=1, columnspan=1, sticky="nesw")
        self.button_info_perf.grid(row=2, column=3, columnspan=1, sticky="nesw")
        self.button_info_blue.grid(row=2, column=5, columnspan=1, sticky="nesw")

        self.button_dummy_2.grid(row=2, column=2, columnspan=1, sticky="nesw")
        self.button_dummy_4.grid(row=2, column=4, columnspan=1, sticky="nesw")
        self.button_dummy_6.grid(row=2, column=6, columnspan=1, sticky="nesw")
        self.button_dummy_7.grid(row=2, column=7, columnspan=1, sticky="nesw")
        self.button_dummy_8.grid(row=2, column=8, columnspan=1, sticky="nesw")

        self.grid(column=0, row=0, sticky="nesw")

        for row_num in range(self.grid_size()[1]):
            if row_num == 0 or row_num == 3:
                continue
            self.rowconfigure(row_num, weight=1)

        for col_num in range(self.grid_size()[0]):
            if col_num == 0 or col_num == 9:
                continue
            self.columnconfigure(col_num, weight=1)

        # this is a dict with keys: position -> action
        self.button_dict = {
            "center": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "play_": self.button_hand_1,
                "blk_": self.button_hand_2,
                "edt_": self.button_hand_3
            }
        }

        self.load_correct_labels()
        self.load_correct_invokes()

    def frame_update(self):
        self.upper_class.present_pos = "center"
        self.load_values_to_gui()
        return
    
    def frame_release(self):
        return

    def load_correct_labels(self):

        self.button_hand_1['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_1']
        self.button_hand_2['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_2']
        self.button_hand_3['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_3']
        self.button_hand_4['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_4']
    
    def load_correct_invokes(self):

        self.button_hand_1["command"] = lambda: self.send_message(self.button_hand_1)
        self.button_hand_2["command"] = lambda: self.joystick_moment(self.button_hand_2)
        self.button_hand_3["command"] = lambda: self.joystick_moment(self.button_hand_3)
            
    def send_message(self, button):
        # we want the button to press and unpress
        snippet_number = self.upper_class.video_to_play.path.split("/")[-1].replace("_lores.avi", "").split("_")[1]
        main_number = self.upper_class.video_to_play.path.split("/")[-1].replace("_lores.avi", "").split("_")[0]
        
        self.upper_class.client.client_send(self.message_for_action+main_number+"&"+snippet_number)

    def joystick_moment(self, button):
        
        button_content = button["text"].splitlines()

        if self.message_for_action not in ["up", "down", "loopr", "loopl"]: # we either entered the button or want to exit

            if self.upper_class.joystick_mode[0] == False: # we just entered the joystick mode

                self.upper_class.joystick_mode = (True, button_content[0], self.message_for_action)
                self.upper_class.active_joystick_button = button

                #ask for the current value
                self.upper_class.client.client_send(self.message_for_action+"0")

                button["bg"] ='dark slate gray'

            else: # we were in the joystick mode and now we should check if we are pressing the same button
                    
                if button_content[0] == self.button_dict[self.upper_class.present_pos][self.message_for_action]["text"].splitlines()[0]: # we want to exit
                    
                    # here, in play menu, we want to start play here

                    snippet_number = self.upper_class.video_to_play.path.split("/")[-1].replace("_lores.avi", "").split("_")[1]
                    main_number = self.upper_class.video_to_play.path.split("/")[-1].replace("_lores.avi", "").split("_")[0]

                    self.upper_class.client.client_send("play_"+main_number+"&"+snippet_number)

                    self.upper_class.joystick_mode = (False, "", "")
                    self.upper_class.active_joystick_button = ""

                    button["bg"] ='black'

        else: # we want to change the value

            if self.message_for_action == "up": # we want to up the number

                self.upper_class.client.client_send(self.upper_class.joystick_mode[2]+"1")
            elif self.message_for_action == "down": 

                self.upper_class.client.client_send(self.upper_class.joystick_mode[2]+"-1")
    
    def load_values_to_gui(self):
        # maybe the best solution is to simulate clicks on the buttons that can be read

        self.upper_class.populate_mode = True

        for button_key in self.button_dict[self.upper_class.present_pos].keys():

            if "msp" in button_key or "fps" in button_key or "blk" in button_key or "exp" in button_key or "edt" in button_key:
               
                self.upper_class.client.client_send(button_key+"0")
                
                # then we wait the reply
                while self.upper_class.populate_values_queue.empty():
                    time.sleep(0.01)

                current_value = self.upper_class.populate_values_queue.get()

                total_text = self.button_dict[self.upper_class.present_pos][button_key]["text"].splitlines()
                self.button_dict[self.upper_class.present_pos][button_key]["text"] = total_text[0] + "\n" + current_value

        self.upper_class.populate_mode = False
    
class VideoCheckFrame(tk.Frame):
    #we will start the thread in this class
    def __init__(self, parent, upper_class, menu_name):
        super().__init__(parent)
        self.current_video = ""
        self.upper_class = upper_class
        self.thumb_frame = tk.Frame(master=self, bg="black", highlightbackground="black", highlightthickness=0)
        self.video_dict = {"files": [], "buttons": []}
        self.button_dict = {"center": {}}
        self.init_thumb_number = 12
        self.video_change_button = tk.Button(self, text="", command=self.move_selection, bg='black')
        self.video_play_button = tk.Button(self, text="", command=self.play_selection, bg='black')

        for i in range(self.init_thumb_number):
            new_label = tk.Label(self.thumb_frame, bg="black", highlightbackground="white", borderwidth=0, highlightthickness=2, bd=0, padx=0, pady=0)
            self.video_dict["buttons"].append(new_label)

            new_label.grid(row=0, column=len(self.video_dict["buttons"]) - 1, sticky="nesw")

        self.menu_name = menu_name
        
        self.v1_label = tk.Label(self, bg="black", highlightbackground="white", borderwidth=0, highlightthickness=0, pady=350, height=700, bd=0)

        self.grid(column=0, row=0, sticky="nesw")

        self.v1_label.grid(row=0, column=0, sticky="nesw")
        self.thumb_frame.grid(row=1, column=0, sticky="nesw")

        for row_num in range(self.grid_size()[1]):
            self.rowconfigure(row_num, weight=1)

        for col_num in range(self.grid_size()[0]):
            self.columnconfigure(col_num, weight=1)

        for row_num in range(self.thumb_frame.grid_size()[1]):
            self.thumb_frame.rowconfigure(row_num, weight=1)

        for col_num in range(self.thumb_frame.grid_size()[0]):
            self.thumb_frame.columnconfigure(col_num, weight=1)

        self.frame_update()

        self.v1_queue = queue.Queue(maxsize=1)

        self.play_event = Event()
        self.video_kill = Event()

        self.message_for_action = ""

        self.start_video_thread()

        self.button_dict = {
            "center": {
                #"up": self.button_up,
                "play": self.video_play_button,
                "prevv": self.video_change_button,
                "nextv": self.video_change_button
                #"str_0": self.button_hand_1,
                #"bperf_0": self.button_hand_2,
                #"eperf_0": self.button_hand_3
            }
        }
    
    def play_selection(self):
        
        self.upper_class.change_to_menu("video_play")
        self.upper_class.video_to_play = self.current_video
        self.frame_release()

    def move_selection(self):
        # this is called everytime we move left or right in this menu. We first have to see if there are any button at all
        if len(self.video_dict["files"]) > 0:
            for idx, file_ in enumerate(self.video_dict["files"]):
                if file_ == self.current_video:
                    break
            
            if self.message_for_action == "prevv":
                if idx > 0:
                    self.change_selected_video(idx-1)

            elif self.message_for_action == "nextv":
                if idx < len(self.video_dict["files"]) - 1 :
                    self.change_selected_video(idx+1)

    def frame_update(self):
        self.upper_class.present_pos = "center"
        self.find_org_folder_videos()
        self.refresh_n_thumb_buttons()
        self.change_selected_video(-1)
    
    def frame_release(self):
        self.play_event.clear()

    def change_selected_video(self, new_sel_idx):
        if new_sel_idx == -1:
            # play last video if there is one
            if len(self.video_dict["files"]) > 0:
                for button_idx in range(len(self.video_dict["files"])):
                    self.video_dict["buttons"][button_idx]["bg"] = "black"

                self.video_dict["buttons"][len(self.video_dict["files"])-1]["bg"] = "red"
                self.current_video = self.video_dict["files"][-1]

                self.v1_queue.put(self.current_video.path)
                self.play_event.set()
        
        else:

            for button_idx in range(len(self.video_dict["files"])):
                self.video_dict["buttons"][button_idx]["bg"] = "black"

            self.video_dict["buttons"][new_sel_idx]["bg"] = "red"
            self.current_video = self.video_dict["files"][new_sel_idx]

            self.v1_queue.put(self.video_dict["files"][new_sel_idx].path)
            self.play_event.set()  

    def refresh_n_thumb_buttons(self):

        if len(self.video_dict["files"]) > self.init_thumb_number:
            
            while len(self.video_dict["buttons"]) < len(self.video_dict["files"]):

                new_label = tk.Label(self.thumb_frame, bg="black", highlightbackground="white", borderwidth=0, highlightthickness=2, bd=0, padx=0, pady=0)
                self.video_dict["buttons"].append(new_label)

                new_label.grid(row=0, column=len(self.video_dict["buttons"]) - 1, sticky="nesw")
            
            self.v1_label.config(height=700)
        else:
            # we want to reset to init n buttons, removing the last ones
            while len(self.video_dict["buttons"]) > self.init_thumb_number:
                self.video_dict["buttons"][-1].destroy()
                self.video_dict["buttons"].pop()
            
            for label in self.video_dict["buttons"]:
                label.configure(image="", bg="black", highlightbackground="white", borderwidth=0, highlightthickness=2, bd=0, padx=0, pady=0)
            
            self.v1_label.config(height=700)

    def find_org_folder_videos(self):

        if self.upper_class.current_folder != "":
            tmp_videos = []
            with os.scandir(self.upper_class.current_folder) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith(".avi"):
                        tmp_videos.append(entry)
            
            tmp_videos_sorted = sorted(tmp_videos, key=lambda x: int(x.name[:-10].split("_")[1]), reverse=False)

            self.video_dict["files"] = tmp_videos_sorted # i need to organize this list to 
    
    def start_video_thread(self):

        self.video_thread = Thread(target=self.play_video, args=())
        self.video_thread.start()

    def play_video(self):

        v1_path = ""
        while not self.video_kill.is_set() :
            
            if not self.v1_queue.empty():
                v1_path = self.v1_queue.get()
                cap1 = cv2.VideoCapture(v1_path)

            while self.play_event.is_set() and v1_path != "":
                
                if not self.v1_queue.empty():
                    v1_path = self.v1_queue.get()
                    cap1 = cv2.VideoCapture(v1_path)
                
                ret1, frame1 = cap1.read()
  
                if not ret1:
                    cap1 = cv2.VideoCapture(v1_path)
                    continue

                blue1,green1,red1 = cv2.split(frame1)

                img1 = cv2.merge((red1,green1,blue1))
                
                im1 = Image.fromarray(img1)
                imgtk1 = ImageTk.PhotoImage(image=im1)

                imgtk1 = imgtk1._PhotoImage__photo.zoom(2)
                
                self.v1_label.configure(image=imgtk1)
                self.v1_label.image = imgtk1
            
            time.sleep(0.1)
          
            v1_path = ""

class NavigationFrame(tk.Frame):
    def __init__(self, parent, upper_class, menu_name):
        super().__init__(parent)
        self.message_for_action = ""
        self.upper_class = upper_class
        self.menu_name = menu_name
        self["bg"] = "black"
        self.button_font = tkFont.Font(size=40, weight='bold')

        self.SIDE_B_W = 1
        self.SIDE_B_H = 100
        self.TOP_B_W = 200
        self.TOP_B_H = self.SIDE_B_W
        self.HAND_B_W = (1/8)*self.TOP_B_W
        self.HAND_B_H = 3*self.SIDE_B_H

        self.button_up = tk.Button(self, text="UP", padx=self.TOP_B_W, pady=self.TOP_B_H, command=self.go_up, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_down = tk.Button(self, text="DOWN", padx=self.TOP_B_W, pady=self.TOP_B_H, command=self.go_down, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_right = tk.Button(self, text="RIGHT", padx=self.SIDE_B_W, pady=self.SIDE_B_H, wraplength=1, command=self.go_right, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_left = tk.Button(self, text="LEFT", padx=self.SIDE_B_W, pady=self.SIDE_B_H, wraplength=1, command=self.go_left, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)

        self.move_buttons = [self.button_down, self.button_up, self.button_left, self.button_right]

        self.button_hand_1 = tk.Button(self, text="action1", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_2 = tk.Button(self, text="action2", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_3 = tk.Button(self, text="action3", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_4 = tk.Button(self, text="action4", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)

        self.button_hand_1["font"] = self.button_font
        self.button_hand_2["font"] = self.button_font
        self.button_hand_3["font"] = self.button_font
        self.button_hand_4["font"] = self.button_font

        self.button_info_rec = tk.Button(self, text="R", bg='black', borderwidth=0, highlightthickness=0)
        self.button_info_blue = tk.Button(self, text="B", bg='black', borderwidth=0, highlightthickness=0)
        self.button_info_perf = tk.Button(self, text="P", bg='black', borderwidth=0, highlightthickness=0)

        self.button_dummy_2 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_4 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_6 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_7 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_8 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)

        self.button_up.grid(row=0, column=1, columnspan=8, sticky="nesw")
        self.button_down.grid(row=3, column=1, columnspan=8, sticky="nesw")
        self.button_right.grid(row=1, column=9, rowspan=2, sticky="nesw")
        self.button_left.grid(row=1, column=0, rowspan=2, sticky="nesw")

        self.button_hand_1.grid(row=1, column=1, columnspan=2, sticky="nesw")
        self.button_hand_2.grid(row=1, column=3, columnspan=2, sticky="nesw")
        self.button_hand_3.grid(row=1, column=5, columnspan=2, sticky="nesw")
        self.button_hand_4.grid(row=1, column=7, columnspan=2, sticky="nesw")

        self.button_info_rec.grid(row=2, column=1, columnspan=1, sticky="nesw")
        self.button_info_perf.grid(row=2, column=3, columnspan=1, sticky="nesw")
        self.button_info_blue.grid(row=2, column=5, columnspan=1, sticky="nesw")

        self.button_dummy_2.grid(row=2, column=2, columnspan=1, sticky="nesw")
        self.button_dummy_4.grid(row=2, column=4, columnspan=1, sticky="nesw")
        self.button_dummy_6.grid(row=2, column=6, columnspan=1, sticky="nesw")
        self.button_dummy_7.grid(row=2, column=7, columnspan=1, sticky="nesw")
        self.button_dummy_8.grid(row=2, column=8, columnspan=1, sticky="nesw")

        self.grid(column=0, row=0, sticky="nesw")

        for row_num in range(self.grid_size()[1]):
            if row_num == 0 or row_num == 3:
                continue
            self.rowconfigure(row_num, weight=1)

        for col_num in range(self.grid_size()[0]):
            if col_num == 0 or col_num == 9:
                continue
            self.columnconfigure(col_num, weight=1)

        # this is a dict with keys: position -> action
        self.button_dict = {
            "center": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "str_0": self.button_hand_1,
                "bperf_0": self.button_hand_2,
                "eperf_0": self.button_hand_3
            },
            "up": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "msppresetchange_current&": self.button_hand_1,
            },
            "down": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "mspwavplay_current&": self.button_hand_1,
            },
            "left": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "fps_": self.button_hand_1,
                "blk_": self.button_hand_2,
                "exp_": self.button_hand_3
            },
            "right": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "fps_": self.button_hand_1,
                "exp_": self.button_hand_2,
                "stop_0": self.button_hand_3
            }
        }

        self.load_correct_labels()
        self.load_correct_invokes()

    def frame_update(self):
        self.go_center()
    
    def frame_release(self):
        return
    
    def go_up(self):

        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)

        if self.upper_class.present_pos != 'down':

            self.upper_class.present_pos = 'up'
            self.change_move_button_state('disabled', self.button_up)

        else:

            self.upper_class.present_pos = 'center'
        
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()
    
    def go_down(self):

        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)


        if self.upper_class.present_pos != 'up':

            self.upper_class.present_pos = 'down'
            self.change_move_button_state('disabled', self.button_down)

        else:

            self.upper_class.present_pos = 'center'
        
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()

    def go_left(self):
        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)


        if self.upper_class.present_pos != 'right':

            self.upper_class.present_pos = 'left'
            self.change_move_button_state('disabled', self.button_left)

        else:

            self.upper_class.present_pos = 'center'   
        
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()

    def go_right(self):
        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)


        if self.upper_class.present_pos != 'left':

            self.upper_class.present_pos = 'right'
            self.change_move_button_state('disabled', self.button_right)

        else:

            self.upper_class.present_pos = 'center' 

        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()


    def go_center(self):
        #with this we go to the center layout of the present menu

        #change actual position
        self.upper_class.present_pos = 'center'

        #load center labels for all buttons
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()
        #change state of all arrows to normal
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)

    def send_message(self, button):
        # we want the button to press and unpress
        
        self.upper_class.client.client_send(self.message_for_action)

    def joystick_moment(self, button):
        
        button_content = button["text"].splitlines()
        
        if self.message_for_action not in ["up", "down", "loopr", "loopl"]: # we either entered the button or want to exit

            if self.upper_class.joystick_mode[0] == False: # we just entered the joystick mode

                self.upper_class.joystick_mode = (True, button_content[0], self.message_for_action)
                self.upper_class.active_joystick_button = button

                #ask for the current value
                self.upper_class.client.client_send(self.message_for_action+"0")
                # visual activation
                button["bg"] ='dark slate gray'

            else: # we were in the joystick mode and now we should check if we are pressing the same button
                    
                if button_content[0] == self.button_dict[self.upper_class.present_pos][self.message_for_action]["text"].splitlines()[0]: # we want to exit
                    self.upper_class.joystick_mode = (False, "", "")
                    self.upper_class.active_joystick_button = ""
                    button["bg"] ='black'

                    if self.upper_class.present_pos == "right": #ISTO ESTÁ HARDCODED!!!

                        self.upper_class.client.client_send("rec_0")
                    
                    elif self.upper_class.present_pos == "down": #ISTO ESTÁ HARDCODED!!!

                        self.upper_class.client.client_send("mspwavplay_current&act")

                else: # we want to change to a differnt button
                    self.upper_class.joystick_mode = (True, self.button_dict[self.upper_class.present_pos][self.message_for_action]["text"].splitlines()[0], self.message_for_action)
                    self.upper_class.active_joystick_button = self.button_dict[self.upper_class.present_pos][self.message_for_action]
                    
                    #ask for the current value
                    self.upper_class.client.client_send(self.message_for_action+"0")

                    button["bg"] ='black'
                    self.upper_class.active_joystick_button["bg"] = 'dark slate gray'

        elif self.message_for_action in ["up", "down"]: # we want to change the value

            if self.message_for_action == "up": # we want to up the number

                self.upper_class.client.client_send(self.upper_class.joystick_mode[2]+"1")
            elif self.message_for_action == "down": 

                self.upper_class.client.client_send(self.upper_class.joystick_mode[2]+"-1")

        elif self.message_for_action in ["loopr", "loopl"]: # we want to start a loop

            send_obj = self.upper_class.joystick_mode[2].split("_")[0] + "_"

            if "current" in self.upper_class.joystick_mode[2]: # we only start and end loops inside "current" type buttons

                if self.message_for_action == "loopr": # clockwise
                    
                    self.upper_class.client.client_send(send_obj+"loopr")

                elif self.message_for_action == "loopl": # counter clockwise

                    self.upper_class.client.client_send(send_obj+"loopl")

    def load_values_to_gui(self):
        # maybe the best solution is to simulate clicks on the buttons that can be read

        self.upper_class.populate_mode = True

        for button_key in self.button_dict[self.upper_class.present_pos].keys():

            if "msp" in button_key or "fps" in button_key or "blk" in button_key or "exp" in button_key or "edt" in button_key:
               
                self.upper_class.client.client_send(button_key+"0")
                
                # then we wait the reply
                while self.upper_class.populate_values_queue.empty():
                    time.sleep(0.01)

                current_value = self.upper_class.populate_values_queue.get()

                total_text = self.button_dict[self.upper_class.present_pos][button_key]["text"].splitlines()
                self.button_dict[self.upper_class.present_pos][button_key]["text"] = total_text[0] + "\n" + current_value

        self.upper_class.populate_mode = False

    def load_correct_labels(self):

        self.button_hand_1['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_1']
        self.button_hand_2['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_2']
        self.button_hand_3['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_3']
        self.button_hand_4['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_4']
    
    def load_correct_invokes(self):
        
        if self.upper_class.present_pos == "center":
            self.button_hand_1["command"] = lambda: self.send_message(self.button_hand_1)
            self.button_hand_2["command"] = lambda: self.send_message(self.button_hand_2)
            self.button_hand_3["command"] = lambda: self.send_message(self.button_hand_3)
            self.button_hand_4["command"] = lambda: self.send_message(self.button_hand_4)

        elif self.upper_class.present_pos == "left":
            self.button_hand_1["command"] = lambda: self.joystick_moment(self.button_hand_1)
            self.button_hand_2["command"] = lambda: self.joystick_moment(self.button_hand_2)
            self.button_hand_3["command"] = lambda: self.joystick_moment(self.button_hand_3)

        elif self.upper_class.present_pos == "right":
            self.button_hand_1["command"] = lambda: self.joystick_moment(self.button_hand_1)
            self.button_hand_2["command"] = lambda: self.joystick_moment(self.button_hand_2)
            self.button_hand_3["command"] = lambda: self.send_message(self.button_hand_3)
        
        elif self.upper_class.present_pos == "down":
            self.button_hand_1["command"] = lambda: self.joystick_moment(self.button_hand_1)

        elif self.upper_class.present_pos == "up":
            self.button_hand_1["command"] = lambda: self.joystick_moment(self.button_hand_1)

    def change_move_button_state(self, state, button):

        if state == 'normal':
            button["state"] = "normal"
            button['bg'] = "black"
        
        elif state == 'disabled':

            button["state"] = "disabled"
            button['bg'] = "red"

class AudioFrame(tk.Frame):
    def __init__(self, parent, upper_class, menu_name):
        super().__init__(parent)

        self.message_for_action = ""
        self.upper_class = upper_class
        self.menu_name = menu_name
        self["bg"] = "black"
        self.button_font = tkFont.Font(size=40, weight='bold')

        self.SIDE_B_W = 1
        self.SIDE_B_H = 100
        self.TOP_B_W = 200
        self.TOP_B_H = self.SIDE_B_W
        self.HAND_B_W = (1/8)*self.TOP_B_W
        self.HAND_B_H = 3*self.SIDE_B_H

        self.button_up = tk.Button(self, text="UP", padx=self.TOP_B_W, pady=self.TOP_B_H, command=self.go_up, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_down = tk.Button(self, text="DOWN", padx=self.TOP_B_W, pady=self.TOP_B_H, command=self.go_down, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_right = tk.Button(self, text="RIGHT", padx=self.SIDE_B_W, pady=self.SIDE_B_H, wraplength=1, command=self.go_right, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)
        self.button_left = tk.Button(self, text="LEFT", padx=self.SIDE_B_W, pady=self.SIDE_B_H, wraplength=1, command=self.go_left, bg='black', activebackground="#18135e", borderwidth=0, highlightthickness=0)

        self.move_buttons = [self.button_down, self.button_up, self.button_left, self.button_right]

        self.button_hand_1 = tk.Button(self, text="action1", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_2 = tk.Button(self, text="action2", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_3 = tk.Button(self, text="action3", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)
        self.button_hand_4 = tk.Button(self, text="action4", padx=self.HAND_B_W, pady=self.HAND_B_H, bg='black', fg='white', activebackground="#18135e", borderwidth=0, compound="bottom", highlightthickness=0)

        self.button_hand_1["font"] = self.button_font
        self.button_hand_2["font"] = self.button_font
        self.button_hand_3["font"] = self.button_font
        self.button_hand_4["font"] = self.button_font

        self.button_info_rec = tk.Button(self, text="R", bg='black', borderwidth=0, highlightthickness=0)
        self.button_info_blue = tk.Button(self, text="B", bg='black', borderwidth=0, highlightthickness=0)
        self.button_info_perf = tk.Button(self, text="P", bg='black', borderwidth=0, highlightthickness=0)

        self.button_dummy_2 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_4 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_6 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_7 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)
        self.button_dummy_8 = tk.Button(self, text="", bg='black', borderwidth=0, highlightthickness=0)

        self.button_up.grid(row=0, column=1, columnspan=8, sticky="nesw")
        self.button_down.grid(row=3, column=1, columnspan=8, sticky="nesw")
        self.button_right.grid(row=1, column=9, rowspan=2, sticky="nesw")
        self.button_left.grid(row=1, column=0, rowspan=2, sticky="nesw")

        self.button_hand_1.grid(row=1, column=1, columnspan=2, sticky="nesw")
        self.button_hand_2.grid(row=1, column=3, columnspan=2, sticky="nesw")
        self.button_hand_3.grid(row=1, column=5, columnspan=2, sticky="nesw")
        self.button_hand_4.grid(row=1, column=7, columnspan=2, sticky="nesw")

        self.button_info_rec.grid(row=2, column=1, columnspan=1, sticky="nesw")
        self.button_info_perf.grid(row=2, column=3, columnspan=1, sticky="nesw")
        self.button_info_blue.grid(row=2, column=5, columnspan=1, sticky="nesw")

        self.button_dummy_2.grid(row=2, column=2, columnspan=1, sticky="nesw")
        self.button_dummy_4.grid(row=2, column=4, columnspan=1, sticky="nesw")
        self.button_dummy_6.grid(row=2, column=6, columnspan=1, sticky="nesw")
        self.button_dummy_7.grid(row=2, column=7, columnspan=1, sticky="nesw")
        self.button_dummy_8.grid(row=2, column=8, columnspan=1, sticky="nesw")

        self.grid(column=0, row=0, sticky="nesw")

        for row_num in range(self.grid_size()[1]):
            if row_num == 0 or row_num == 3:
                continue
            self.rowconfigure(row_num, weight=1)

        for col_num in range(self.grid_size()[0]):
            if col_num == 0 or col_num == 9:
                continue
            self.columnconfigure(col_num, weight=1)

        # this is a dict with keys: position -> action
        self.button_dict = {
            "center": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "mspmaingain_current&": self.button_hand_1,
                "mspmaingain_umax&": self.button_hand_2,
                "mspmaingain_umin&": self.button_hand_3,
                "mspmaingain_cycle&": self.button_hand_4
            },
            "up": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "mspcrossfreq2_current&": self.button_hand_1,
                "mspcrossfreq2_umax&": self.button_hand_2,
                "mspcrossfreq2_umin&": self.button_hand_3,
                "mspcrossfreq2_cycle&": self.button_hand_4
            },
            "down": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "mspodlevel_current&": self.button_hand_1,
                "mspodlevel_umax&": self.button_hand_2,
                "mspodlevel_umin&": self.button_hand_3,
                "mspodlevel_cycle&": self.button_hand_4
            },
            "left": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "mspcrossfreq_current&": self.button_hand_1,
                "mspcrossfreq_umax&": self.button_hand_2,
                "mspcrossfreq_umin&": self.button_hand_3,
                "mspcrossfreq_cycle&": self.button_hand_4
            },
            "right": {
                "up": self.button_up,
                "down": self.button_down,
                "left": self.button_left,
                "right": self.button_right,
                "mspcrossfreq3_current&": self.button_hand_1,
                "mspcrossfreq3_umax&": self.button_hand_2,
                "mspcrossfreq3_umin&": self.button_hand_3,
                "mspcrossfreq3_cycle&": self.button_hand_4
            }
        }

        self.load_correct_labels()
        self.load_correct_invokes()

    def frame_update(self):
        self.go_center()
    
    def frame_release(self):
        return
    
    def go_up(self):
        
        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)

        if self.upper_class.present_pos != 'down':

            self.upper_class.present_pos = 'up'
            self.change_move_button_state('disabled', self.button_up)

        else:

            self.upper_class.present_pos = 'center'
        
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()
    
    def go_down(self):

        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)


        if self.upper_class.present_pos != 'up':

            self.upper_class.present_pos = 'down'
            self.change_move_button_state('disabled', self.button_down)

        else:

            self.upper_class.present_pos = 'center'
        
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()

    def go_left(self):
        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)


        if self.upper_class.present_pos != 'right':

            self.upper_class.present_pos = 'left'
            self.change_move_button_state('disabled', self.button_left)

        else:

            self.upper_class.present_pos = 'center'   
        
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()

    def go_right(self):
        #first check all buttons and see if any is disabled. If so, 
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)


        if self.upper_class.present_pos != 'left':

            self.upper_class.present_pos = 'right'
            self.change_move_button_state('disabled', self.button_right)

        else:

            self.upper_class.present_pos = 'center' 

        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()


    def go_center(self):
        #with this we go to the center layout of the present menu

        #change actual position
        self.upper_class.present_pos = 'center'

        #load center labels for all buttons
        self.load_correct_labels()
        self.load_correct_invokes()
        self.load_values_to_gui()
        
        #change state of all arrows to normal
        for button in self.move_buttons:
            if button['state'] == 'disabled':
                self.change_move_button_state('normal', button)       

    def send_message(self, button):
        # we want the button to press and unpress
        
        self.upper_class.client.client_send(self.message_for_action)

    def joystick_moment(self, button):
        
        button_content = button["text"].splitlines()
        
        if self.message_for_action not in ["up", "down", "loopr", "loopl"]: # we either entered the button or want to exit

            if self.upper_class.joystick_mode[0] == False: # we just entered the joystick mode

                self.upper_class.joystick_mode = (True, button_content[0], self.message_for_action)
                self.upper_class.active_joystick_button = button

                #ask for the current value
                self.upper_class.client.client_send(self.message_for_action+"0")
                # visual activation
                button["bg"] ='dark slate gray'

            else: # we were in the joystick mode and now we should check if we are pressing the same button
                    
                if button_content[0] == self.button_dict[self.upper_class.present_pos][self.message_for_action]["text"].splitlines()[0]: # we want to exit
                    self.upper_class.joystick_mode = (False, "", "")
                    self.upper_class.active_joystick_button = ""
                    button["bg"] ='black'

                else: # we want to change to a differnt button

                    self.upper_class.joystick_mode = (True, self.button_dict[self.upper_class.present_pos][self.message_for_action]["text"].splitlines()[0], self.message_for_action)
                    self.upper_class.active_joystick_button = self.button_dict[self.upper_class.present_pos][self.message_for_action]
                    
                    #ask for the current value
                    self.upper_class.client.client_send(self.message_for_action+"0")

                    button["bg"] ='black'
                    self.upper_class.active_joystick_button["bg"] = 'dark slate gray'

        elif self.message_for_action in ["up", "down"]: # we want to change the value

            if self.message_for_action == "up": # we want to up the number

                self.upper_class.client.client_send(self.upper_class.joystick_mode[2]+"1")
            elif self.message_for_action == "down": 

                self.upper_class.client.client_send(self.upper_class.joystick_mode[2]+"-1")

        elif self.message_for_action in ["loopr", "loopl"]: # we want to start a loop

            send_obj = self.upper_class.joystick_mode[2].split("_")[0] + "_"

            if "current" in self.upper_class.joystick_mode[2]: # we only start and end loops inside "current" type buttons

                if self.message_for_action == "loopr": # clockwise
                    
                    self.upper_class.client.client_send(send_obj+"loopr")

                elif self.message_for_action == "loopl": # counter clockwise

                    self.upper_class.client.client_send(send_obj+"loopl")

    def load_correct_labels(self):

        self.button_hand_1['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_1']
        self.button_hand_2['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_2']
        self.button_hand_3['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_3']
        self.button_hand_4['text'] = menu_labels[self.menu_name][self.upper_class.present_pos]['button_hand_4']
    
    def load_correct_invokes(self):
        
        self.button_hand_1["command"] = lambda: self.joystick_moment(self.button_hand_1)
        self.button_hand_2["command"] = lambda: self.joystick_moment(self.button_hand_2)
        self.button_hand_3["command"] = lambda: self.joystick_moment(self.button_hand_3)
        self.button_hand_4["command"] = lambda: self.joystick_moment(self.button_hand_4)

    def load_values_to_gui(self):
        # maybe the best solution is to simulate clicks on the buttons that can be read

        self.upper_class.populate_mode = True

        for button_key in self.button_dict[self.upper_class.present_pos].keys():

            if "msp" in button_key or "fps" in button_key or "blk" in button_key or "exp" in button_key or "edt" in button_key:
               
                self.upper_class.client.client_send(button_key+"0")
                
                # then we wait the reply
                while self.upper_class.populate_values_queue.empty():
                    time.sleep(0.01)

                current_value = self.upper_class.populate_values_queue.get()

                total_text = self.button_dict[self.upper_class.present_pos][button_key]["text"].splitlines()
                self.button_dict[self.upper_class.present_pos][button_key]["text"] = total_text[0] + "\n" + current_value

        self.upper_class.populate_mode = False
                    
    def change_move_button_state(self, state, button):

        if state == 'normal':
            button["state"] = "normal"
            button['bg'] = "black"
        
        elif state == 'disabled':

            button["state"] = "disabled"
            button['bg'] = "red"

class MenuGUI():

    def __init__(self, master):
        
        self.shared_lock = Lock()

        self.root = master
        self.root["bg"] = "black"
        self.client = alumia_TCP.TCPClient(server_ip="193.168.1.3", server_port=12840, code="mon")
        self.tcp_kill = Event()

        self.current_folder = ""

        # for conditions comparison
        self.streaming = False
        self.recording = False
        self.playing = False
        self.in_perf = False
        self.folder_selected = False
        self.populate_mode = False

        self.populate_values_queue = queue.Queue(maxsize=1)

        self.menu_list = {}
        
        self.present_menu = "menu1"
        self.present_pos = "center"

        self.joystick_mode = (False, "", "")
        self.active_joystick_button = ""

        self.video_to_play = ""

        self.root = master
        self.root.title("Menu test")
        self.root.attributes('-fullscreen', True)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.menu_list["nav"] = NavigationFrame(master, self, "nav")
        self.menu_list["video_sel"] = VideoCheckFrame(master, self, "video_sel")
        self.menu_list["video_play"] = VideoPlayFrame(master, self, "video_play")
        self.menu_list["audio"] = AudioFrame(master, self, "audio")

        self.change_to_menu("nav")

        self.run_tcp()

    def change_to_menu(self, menu):

        for menu_type in self.menu_list:
            if menu_type == menu:
                self.menu_list[menu_type].frame_update()
                self.present_menu = menu
                self.menu_list[menu_type].tkraise()       
     
            else:
                self.menu_list[menu_type].forget()
                self.menu_list[menu_type].frame_release()

    def show_popup(self, text="default"):
        
        top = Toplevel(self.root)
        top.geometry("1000x500")
        top.title("WARNING")

        top.attributes('-fullscreen', True)

        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        tk.Label(top, text=text, font=('Mistral 30 bold')).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        time.sleep(1)

        top.destroy()
        top.update()

    def run_tcp(self):
        """Run method from Thread. Starts the thread.
        """

        self.thread_tcp = Thread(target=self.tcp_comm, args=())
        self.thread_tcp.daemon = True
        self.thread_tcp.start()
    
    def close_tcp(self):

        self.root.destroy()
        
    def tcp_comm(self):
        self.client.client_connect()

        while not self.tcp_kill.is_set():
            if self.client.connected:
                data_in = self.client.client_recv()
                if self.populate_mode == False:
                    if data_in[2] == "win":
                        if data_in[0] == "end":

                            self.tcp_kill.set() 
                            self.client.client_close()                    

                        elif data_in[0] == "fld":
                            
                            params = data_in[1].split("&")
                            self.current_folder = MONITOR_ROOT + params[0] + "/" + params[1] + "/"

                            self.client.client_send("fld_"+data_in[1])
                            self.folder_selected = True

                        elif data_in[0] == "vid":
                            if data_in[1] == "1":
                                self.menu_list["nav"].button_info_rec["bg"] = "red"
                                self.recording = True
                                
                            else:
                                self.menu_list["nav"].button_info_rec["bg"] = "black"
                                self.recording = False

                        elif data_in[0] == "str":
                            if data_in[1] == "1":
                                print("started_stream")
                                self.streaming = True
                                #this will then update the GUI
                            else:
                                print("stopped stream")
                                #this will then update the GUI
                                self.streaming = False

                        elif data_in[0] == "fps":

                            total_text = self.active_joystick_button["text"].splitlines()
                            self.active_joystick_button["text"] = total_text[0] + "\n" + data_in[1]
                        
                        elif data_in[0] == "exp":
 
                            total_text = self.active_joystick_button["text"].splitlines()
                            self.active_joystick_button["text"] = total_text[0] + "\n" + data_in[1]

                        elif data_in[0] == "blk":

                            total_text = self.active_joystick_button["text"].splitlines()
                            self.active_joystick_button["text"] = total_text[0] + "\n" + data_in[1]

                        elif data_in[0] == "edt":

                            total_text = self.active_joystick_button["text"].splitlines()
                            self.active_joystick_button["text"] = total_text[0] + "\n" + data_in[1]

                        elif data_in[0] == "bperf":

                            self.menu_list["nav"].button_info_perf["bg"] = "yellow"
                            self.in_perf = True

                        elif data_in[0] == "eperf":

                            self.menu_list["nav"].button_info_perf["bg"] = "black"
                            self.in_perf = False
                        
                        elif "msp" in data_in[0]:

                            total_text = self.active_joystick_button["text"].splitlines()
                            self.active_joystick_button["text"] = total_text[0] + "\n" + data_in[1]

                        else:
                            print(data_in)
                else:
                    if any(substring in data_in[0] for substring in ["msp", "blk", "exp", "fps", "edt"]):
                        
                        self.populate_values_queue.put(data_in[1])
