import alumia_menu_decoder
import serial
import tkinter as tk


if __name__ == "__main__":

    root = tk.Tk()

    menu_action = alumia_menu_decoder.MenuDecoder(root)
    menu_action.run()

    root.mainloop()    

    menu_action.thread_tcp.join()
    menu_action.counter_thread.thread.join()
    menu_action.thread.join()

    print("MON END SIGNAL")