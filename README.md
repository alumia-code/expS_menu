> ### Developed with and for PhD candidate [Fil Botelho@Orpheus Institute](https://orpheusinstituut.be/en/orpheus-research-centre/researchers/filipa-botelho)
> This is part of the experimental_system (**expS**) repositories that are present on this github account.

# 🔲menu
`Python` code for a `tkinter` GUI application that serves as the GUI for the experimental system (expS) project.

Receives commands from a bluetooth device (serial) and outputs actions to other machines in the local network via TCP.

### Main characteristics:
> 1. Receives `Bluetooth` (serial) commands from a wireless glove.
> 2. Outputs/receives actions via TCP.
> 3. Allows the user to navigate a GUI with all the necessary actions (record video, change fps, manipulate audio, etc).
> 4. Can deal with joysticks and buttons.
> 5. Displays video.
> 6. Is updated with info coming from all clients.

# 💻Requirements
## Hardware
- This was running on very old laptop, no concerns here.
- Bluetooth adapter paired with the control device (in our case, it was a wireless bluetooth glove)
- This machine was communicating will all the other machines through a wired switch.
- 1 GigE was enough across all machines.
   
## Software
- Debian based OS
- `cifs-utils` and `samba client` for shared folder system
- `opencv-python`
- `pyserial` for serial bluetooth
- `tkinter`
- `pillow`
  
# 🖱️ Use
As mentioned, this app is part of a bigger (multi-system) project (all repositories belonging to this project have `expS` as a prefix). It constitutes the 
menu that is used by the performer to control all the necessary aspects of the used elements: video, audio and light.

The user can:
> 1. Use a bluetooth device to navigate the menu.
> 2. Turn on/off the real time video stream
> 3. Manipulate video/audio characteristics (fps, exposure time, iso, fx, etc) in real time.
> 4. Start/stop video/audio capture (to storage) at will.
> 5. Init video/audio play with editing functions.
> 6. Manipulate audio FX, change audio presets.
> 7. See a low res version of the recorded videos.

# ☮️Keep in mind
- I am sharing this here because some concepts might interest some people. **The code is not made to run first time**. All the system needs to be setup,
with all the credentials and the right hardware.
- If you want to use the code, or explore some idea, it is better if you contact me at: alumiamusic@gmail.com
