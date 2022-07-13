import fractions
import subprocess
import re
import tkinter as t
import os
import random


def findPwd():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

    wifi_list = []

    if len(profile_names) != 0:
        for name in profile_names:
        
            wifi_profile = {}
        
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
            
                wifi_profile["ssid"] = name
            
            
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
                if password == None:
                    wifi_profile["password"] = None
                else:
                
                    wifi_profile["password"] = password[1]
            
                wifi_list.append(wifi_profile) 

    for x in range(len(wifi_list)):
        print(wifi_list[x]) 
        pwdlabel = t.Label(frame, text=wifi_list[x], bg="white")
        pwdlabel.pack()


app = t.Tk()
app.title("Wi-Fi Password Finder")

canvas = t.Canvas(app, width=400, height=550, bg="#263D42")
canvas.pack()

frame = t.Frame(app, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

mainBtn = t.Button(app, bg="#263D42", fg="white", text="Get WiFi Passwords", command=findPwd, width="20", height="1")
mainBtn.configure(font=("", 15,""))
mainBtn.pack()




app.mainloop()


