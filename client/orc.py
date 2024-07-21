
import pytesseract          # Python-tesseract is an optical character recognition (OCR) tool for python.
import subprocess           # Built-in module that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import pyautogui            # Library that lets your Python scripts control the mouse and keyboard to automate interactions with other applications. 
import tkinter              # Library for screen, window manipulation

import time
import platform

from PIL import ImageGrab   # Python Imaging Library

if platform.system() == "Window":
    import pygetwindow      # Library that provides functions to manage and interact with application windows on your desktop. ONLY WINDOW


def open_vscode(resolution: tuple):
    """
    Automatic open vscode full screeen and Live Share using subprocess
    
    @param resolution: resolution width and height of the screen
    """
    
    print("Open Visual Studio Code ...")
    
    # Open the file with Visual Studio Code
    subprocess.run(["code"])
    
    # Give it some time to open
    time.sleep(2)

    # Maximize the Visual Studio Code window using wmctrl
    subprocess.run(["wmctrl", "-r", "Visual Studio Code", "-b", "add,maximized_vert,maximized_horz"])

    time.sleep(2)
    
    # Open Live Share
    pyautogui.click(21, 365)

    
def say_hello():
    """
    Special greeting
    """
    
    pyautogui.click(700, 700, duration=3)
    
    pyautogui.write("  jo-eun a-chim-i-e-yo, gong-ju-nim!!!   ")
    


def get_os():
    """
    Set up tesseract and return type of operation
    
    @return: Type of peration
    """
    
    # Path to tesseract executable
    # Set the tesseract command based on the operating system
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        return "Windows"
    elif platform.system() == "Darwin":  # macOS
        pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        return "MacOS"
    else:  # Linux
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        return "Linux"
    

def get_screen_resolution():
    """
    Return current screen resolution
    
    @return: Resolution of width and height in pixel
    """
    
    root = tkinter.Tk()
    root.withdraw()  # Hide the root window
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()  # Close the root window
    
    return (width, height)


def get_window(name, os_type):
    """
    Get the window object by the specified name.

    @param name: The name of the window to find.
    @return: The window object if found, string if os_type is not window. Else None.
    """

    if (os_type != "Window"):
        return "OtherOS"
    
    windows = pygetwindow.getWindowsWithTitle(name)
    
    if windows:
        return windows[0]
    
    return None


def capture_content(application_window, resolution: tuple):
    """
    Capture the content of the specified application window by screenshot

    @param application_window: The window object to capture content from.
    @param resolution: resolution width and height of the screen
    @return: The captured screenshot as an Image object.
    """
    
    if (application_window == "OtherOS"):
        screenshot = ImageGrab.grab((0, 0, resolution[0], resolution[1]))
    else:
        application_window.activate()      # This ensure that the capture content is happened in this window
        
        bbox = (application_window.left, 
                application_window.top, 
                application_window.right, 
                application_window.bottom)
        screenshot = ImageGrab.grab(bbox)
    
    return screenshot


def get_text_from_image(image):
    """
    Extract text from the given image using Tesseract OCR.

    @param image: The input image (PIL Image object) containing text.
    @return: The extracted text as a string.
    """
    
    return pytesseract.image_to_string(image)


def main():

    os_type = get_os()
    resolution = get_screen_resolution()

    open_vscode(resolution)
    
    while True:
        vscode_window = get_window("Visual Studio Code", os_type)
        if vscode_window:
            screenshot = capture_content(vscode_window, resolution)
            text = get_text_from_image(screenshot)
            
            print(text)
            
            # Add conditions based on the text to automate tasks using pyautogui
            if "Share (Read/Write)" in text:
                pyautogui.click(253, 201)   # Start share server in Live Share
                
            elif "SESSION DETAILS" in text:
                say_hello()
                break
        
        time.sleep(1)
