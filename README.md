# ImgControl

## Description
ImgControl is a timed image viewer for artists who want to practice quick sketching.
It lets the user select a directory from their hard drive, and collects all the images from it (including all its subdirectories as well).

Screenshots of the program during a drawing session and during a break:

![image](https://github.com/SilverCrimson/imgcontrol/assets/67794509/d79452ce-094a-4364-8333-dafbf9929c38)

It has a freely movable UI bar, but it can be controlled with keyboard input as well.

The functions of the UI bar:

R: enable/disable random ordering  
T: restart the timer  
left/right: step through the images (of course left is only enabled if there actually was a previous image)  
F: select a folder (there can be only one selected, but that can be changed anytime)  
S: settings, help, about  
timer circle (or space on keyboard): pause/resume the timer

The session timer and break timer can be set in the Settings window, as well as the length of the image history (which is implemented to enable backwards stepping, and to reduce repetiton in the random ordering of the images). The image history length cannot be larger than the count of the images from the current directory.


## Tech details
It was developed in `Python 3.11.7`, using the `PyQt6` library for graphics. That was actually the third option I've tried, because `Ruby2D` and `Tkinter` wasn't cutting it (I'm not saying they are bad, I just didn't feel like they were the right choice for me). I've had some problems with PyQt as well, for example it drawing some images very pixelated (which I've solved with a different method: using QSS border-image instead of a QPixmap object), but overall it felt pretty good to work with, with a nice documentation as well.
The program doesn't store the images: the collected images from the current directory and the image history are just arrays of filenames, and it always gets the needed file on the fly. This works for a lot of image filetypes, but .avif files pose quite a challenge: the only way I was able to handle them are to momentarily convert them into a .jpg (called temp.jpg, placed to the directory of the executable), collect it from there, than delete temp.jpg immediately.
Upon closing, the program stores its width, height, coordinates, menu position, random state, timer length, break length, image history size and the whole history as well. It writes everything into a config.txt file (and places it to its own directory), which can be deleted to reset the states (the program will just load a set of default values).


## Installation
~~What installation?~~ You can find releases for [Windows](https://github.com/SilverCrimson/imgcontrol/releases/tag/v0.9w) and [Linux](https://github.com/SilverCrimson/imgcontrol/releases/tag/v0.8l). Just download the `Source code (zip)` version, extract it wherever you want, and run the executable from there.  
The two versions are identical, except the UI bar left-right icons, and some placement in the settings and about page (these caused a lot of problems when tested, however I've only tested them under WSL. Maybe it would all be fine under a real linux install, which I'll certainly try, when I get my sound card working under Ubuntu).  
The program is not packaged to mac, because, frankly, I don't own a mac, and I don't intend to. (Maybe if i wouldn't have an AMD cpu, I could actually use a VM to do it...)

If you want to run the code itself though, no problem. You'll need the following things installed:
- `python 3.10` or higher - because of the match-case syntax
- the following libraries (usually installed with pip): `pyqt6`, `image`, `pillow-avif-plugin` (the last two are just to deal with avif files)
  
With these, you can run `ImgControl.py`. You'll even get a few images in the `testImages` folder to try the program out.
