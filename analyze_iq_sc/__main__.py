import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import time
import threading
import psutil
from tkinter import ttk
import argparse
import toml
import sys
def generated_file_offline_mode(default_path_synced_files_iq,  default_path_analyzed_files_iq, default_path_synced_files_sc,default_path_analyzed_files_sc):    
        file_iq = list_files_in_directory(default_path_synced_files_iq,".iq.tdms")
        for file in file_iq:
            add_file("synced_files_iq.txt",default_path_synced_files_iq, file, 0,"","")
            
        file_sc = list_files_in_directory(default_path_synced_files_sc,".sc.tdms")
        for file in file_sc:
            add_file("synced_files_sc.txt",default_path_synced_files_sc, file, 0,"","")

def list_files_in_directory(directory,end=".iq.tdms"):
    #files0 = os.listdir(directory)
    try:
        files0 = os.listdir(directory)
    except FileNotFoundError:
        # If the directory doesn't exist, return an empty list
        files0 = []
    files=[]
    for i in range(0, len(files0)):
        if files0[i].endswith(end):  # Check if the file has the .tdms extension
            files.append(files0[i])
    sorted_files = sorted(files)  # Sort files by name
    return sorted_files


def browse_folder_and_update_list_filebox(folder_entry, default_path,file_listbox, analyzed_files_name="analyzed_files_iq.txt",end=".iq.tdms"):
    selected_directory = filedialog.askdirectory(initialdir=default_path)
    if selected_directory:
        folder_entry.delete(0, tk.END)  # Clear previous entry
        folder_entry.insert(0, selected_directory)
        file_listbox.delete(0, tk.END)
        update_file_list(file_listbox,selected_directory,analyzed_files_name,end)
        
def browse_folder(folder_entry, default_path):
    selected_directory = filedialog.askdirectory(initialdir=default_path)
    if selected_directory:
        folder_entry.delete(0, tk.END)  # Clear previous entry
        folder_entry.insert(0, selected_directory)

def get_files(files_file = "analyzed_files_iq.txt"):
        if os.path.exists(files_file):
                with open(files_file, "r") as file:
                        #files = file.read().splitlines()
                        files = [line.split()[0] for line in file.read().splitlines()]
                        return files
        else:
                return []
    
def filter_files(files0,end):
    files=[]
    for file in files0:
        if file.endswith(end):  # Check if the file has the .tdms extension
            a = os.path.basename(file)
            files.append(a)
    return files
            
def add_file(output_file,directory1, file1_name, elapsed_time, directory2, file2_name):
    with open(output_file, "a") as file:
        file.write(directory1 + "/" + file1_name +"  " + str(elapsed_time)+ " [second] "+ directory2 + "/" + file2_name + "\n")
        
def check_parent_directory(folder_entry_synced_files_iq, folder_entry_analyzed_files_iq,folder_entry_synced_files_sc, folder_entry_analyzed_files_sc):
    path_synced_files_iq = folder_entry_synced_files_iq.get()
    path_analyzed_files_iq = folder_entry_analyzed_files_iq.get()
    path_synced_files_sc = folder_entry_synced_files_sc.get()
    path_analyzed_files_sc = folder_entry_analyzed_files_sc.get()
    
    BaseDir_path_synced_files_iq = os.path.basename(path_synced_files_iq)
    BaseDir_path_analyzed_files_iq = os.path.basename(path_analyzed_files_iq)
    BaseDir_path_synced_files_sc = os.path.basename(path_synced_files_sc)
    BaseDir_path_analyzed_files_sc = os.path.basename(path_analyzed_files_sc)
    
    if BaseDir_path_synced_files_iq != BaseDir_path_analyzed_files_iq:
        error_message = f"Error: Local directory '{BaseDir_path_synced_files_iq}' and server directory '{BaseDir_path_analyzed_files_iq}' do not match."
        print(error_message)
        folder_entry_synced_files_iq.config(bg="red")
        folder_entry_analyzed_files_iq.config(bg="red")
        return False
    else:
        folder_entry_synced_files_iq.config(bg="white")
        folder_entry_analyzed_files_iq.config(bg="white")
        
    if BaseDir_path_synced_files_sc!=BaseDir_path_analyzed_files_sc:
        error_message = f"Error: Local directory '{BaseDir_path_synced_files_sc}' and server directory '{BaseDir_path_analyzed_files_sc}' do not match."
        print(error_message)
        folder_entry_synced_files_sc.config(bg="red")
        folder_entry_analyzed_files_sc.config(bg="red")
        return False
    else:
        folder_entry_synced_files_sc.config(bg="white")
        folder_entry_analyzed_files_sc.config(bg="white")
    return True

def adjust_scroll_position(current_file_name, files, file_listbox):
    # Get the current file's index in the list
    current_file_name
    current_file_index = files.index(current_file_name) if current_file_name in files else None
    if current_file_index is not None:
        scroll_position = max(0, (current_file_index - 2) / len(files))  # You might want to adjust the offset
        file_listbox.yview_moveto(scroll_position)            

def thread_subprocess_iq(default_path_synced_files_iq,default_path_analyzed_files_iq,thread_file,file_listbox_iq,should_stop_analyze,synced_files,folder_entry_value_list):
    file= thread_file
    start_time = time.time()  # Record the start time
    FramesStep   =int(folder_entry_value_list[5])
    WeightType   =int(folder_entry_value_list[6])
    PlotOption   =int(folder_entry_value_list[7])
    FramesPerPlot=int(folder_entry_value_list[8])
    FFTFreqLow   =float(folder_entry_value_list[9])
    FFTFreqSpan  =float(folder_entry_value_list[10])
    FFTFreqBin   =int(folder_entry_value_list[11])
    FFTNrOfFrames=int(folder_entry_value_list[12])
    FFTFrameBin  =int(folder_entry_value_list[13])
    
    command = f"../iqt7/convert_iqt_iq {FramesStep} {WeightType} {PlotOption} {FramesPerPlot} {FFTFreqLow} {FFTFreqSpan} {FFTFreqBin} {FFTNrOfFrames} {FFTFrameBin}  {default_path_synced_files_iq}/{file} {default_path_analyzed_files_iq}/"
    #command = f"ls {default_path_synced_files_iq}/{file}"
    try:
        set_listbox_iterm_color(file_listbox_iq, file, "yellow")

        #time.sleep(1)
        subprocess.run(command, shell=True, check=True)

        set_listbox_iterm_color(file_listbox_iq, file, "green")
        adjust_scroll_position(file, synced_files, file_listbox_iq) 
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        file_root = file+".root"
        add_file("analyzed_files_iq.txt",default_path_synced_files_iq, file, elapsed_time,default_path_analyzed_files_iq,file_root)
        
    except subprocess.CalledProcessError:
        print(f"Analyze file failed for: {file}")
        set_listbox_iterm_color(file_listbox_iq, file, "red")
            
def analyze_files_worker_iq(default_path_synced_files_iq,default_path_analyzed_files_iq,file_listbox_iq,file_listbox_sc,start_button_analysis, should_stop_analyze,folder_entry_value_list,unanalyzed_files,thread_list):
    #unanalyzed_files=[]
    #thread_list=[]
    while not should_stop_analyze[0]: # keep the threading runing until should_stop_analyze[0] = True.
        #with open('paths_iq.txt', 'w') as f:
        #    f.write(f"{default_path_synced_files_iq}\n")
        #    f.write(f"{default_path_analyzed_files_iq}\n")
        if default_path_synced_files_iq:
            a = default_path_synced_files_iq + "/synced_files_iq.txt"
            update_file_list(file_listbox_iq,default_path_analyzed_files_iq,a,".iq.tdms")
            #a = "synced_files_iq.txt"
            files0 = get_files(a)
            synced_files = filter_files(files0,".iq.tdms")
            analyzed_files = get_files("analyzed_files_iq.txt")
            for file in synced_files:
                if should_stop_analyze[0]:  # Check if user wants to stop analyzing
                    #print("analyze_files_worker_iq has been stopped, you can close the program.")
                    break
                        
                file_fullpath=default_path_synced_files_iq + "/" + file
                num_threads = int(folder_entry_value_list[4])
                if file_fullpath not in analyzed_files and file not in unanalyzed_files:
                    
                    while True and should_stop_analyze[0] ==False:
                        active_thread_number = 0
                        for thread in thread_list:
                            if thread.is_alive():
                                active_thread_number=active_thread_number+1
                        #print(" active_thread_number is ",active_thread_number,". Wait for free CPU. file = ",file)
                        #print(" unanalyzed_files:",unanalyzed_files)
                        if active_thread_number<num_threads:
                            break
                        else:
                            time.sleep(1)
                    
                    unanalyzed_files.append(file)
                    thread = threading.Thread(target=thread_subprocess_iq,args=(default_path_synced_files_iq, default_path_analyzed_files_iq, file,file_listbox_iq,should_stop_analyze,synced_files,folder_entry_value_list))
                    thread.start()
                    time.sleep(1) 
                    thread_list.append(thread)
        time.sleep(1)

def analyze_files_worker_sc(default_path_synced_files_sc,default_path_analyzed_files_sc,file_listbox_iq,file_listbox_sc,start_button_analysis,should_stop_analyze):
    while not should_stop_analyze[0]: # keep the threading runing until should_stop_analyze[0] = True.
        #with open('paths_sc.txt', 'w') as f:
        #    f.write(f"{default_path_synced_files_sc}\n")
        #    f.write(f"{default_path_analyzed_files_sc}\n")
        
        if default_path_synced_files_sc:
            
            a = default_path_synced_files_sc + "/synced_files_sc.txt"
            update_file_list(file_listbox_sc,default_path_analyzed_files_sc,a,".sc.tdms")# Update the file list with the new directory

            #a =  "synced_files_sc.txt"
            files0 =get_files(a)
            synced_files = filter_files(files0,".sc.tdms")
            
            for file in synced_files:
                if should_stop_analyze[0]:
                    #print("analyze_files_worker_sc has been pressed, you can close the program.")
                    break
                file_fullpath=default_path_synced_files_sc + "/" + file                
                analyzed_files = get_files("analyzed_files_sc.txt")        
                
                if file_fullpath not in analyzed_files:
                    start_time = time.time()  # Record the start time
                    command = f"../iqt7/convert_iqt_sc  -i {default_path_synced_files_sc}/{file}  -o {default_path_analyzed_files_sc}/"
                    #command = f"ls {default_path_synced_files_sc}/{file}"
                    try:
                        # Update the listbox item color
                        
                        set_listbox_iterm_color(file_listbox_sc, file, "yellow")
                        #print("chenrj ... subprocess.run(command,")
                        subprocess.run(command, shell=True, check=True)
                        
                        end_time = time.time()  # Record the end time
                        elapsed_time = end_time - start_time
                        
                        # Update the listbox item color
                        #index = file_listbox_sc.get(0, tk.END).index(file)
                        #file_listbox_sc.itemconfig(index, {'bg': 'green'})
                        set_listbox_iterm_color(file_listbox_sc, file, "green")
                        
                        adjust_scroll_position(file, synced_files, file_listbox_sc)
                        file_root = file+".root"
                        #print("chenrj ... add_file")
                        add_file("analyzed_files_sc.txt",default_path_synced_files_sc, file, elapsed_time,default_path_analyzed_files_sc, file_root)
                        
                    except subprocess.CalledProcessError:
                        print(f"Analyze file failed for: {file}")
                        set_listbox_iterm_color(file_listbox_sc, file, "red")
            time.sleep(1)

def analyze_data(start_button_analysis,stop_button, folder_entry_synced_files_iq, folder_entry_analyzed_files_iq,folder_entry_synced_files_sc, folder_entry_analyzed_files_sc,default_path_synced_files_iq,default_path_analyzed_files_iq,file_listbox_iq,file_listbox_sc,reanalyze_button_iq,reanalyze_button_sc,browse_button_synced_files_iq,browse_button_analyzed_files_iq,browse_button_synced_files_sc,browse_button_analyzed_files_sc,should_stop_analyze,folder_entry_list,unanalyzed_files_iq,thread_list_iq):
    folder_entry_value_list=[]
    ####read FFT parameters.
    for obj in folder_entry_list:
        value = obj.get()
        folder_entry_value_list.append(value)
    ####
    default_path_synced_files_iq  = folder_entry_synced_files_iq.get()
    default_path_analyzed_files_iq = folder_entry_analyzed_files_iq.get()
    default_path_synced_files_sc  = folder_entry_synced_files_sc.get()
    default_path_analyzed_files_sc = folder_entry_analyzed_files_sc.get()
    if not check_parent_directory(folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc, folder_entry_analyzed_files_sc):
        return
    
    WorkMode=int(folder_entry_value_list[14])
    if WorkMode == 1:
        generated_file_offline_mode(default_path_synced_files_iq, default_path_analyzed_files_iq,default_path_synced_files_sc,default_path_analyzed_files_sc)

    should_stop_analyze[0] = False
    start_button_analysis.config(state="disabled")  # Disable the start button during syncing    
    folder_entry_synced_files_iq.config(state="disabled")  # Disable user input
    folder_entry_analyzed_files_iq.config(state="disabled")  # Disable user input
    folder_entry_synced_files_sc.config(state="disabled")  # Disable user input
    folder_entry_analyzed_files_sc.config(state="disabled")  # Disable user input
    stop_button.config(state=tk.NORMAL) # Enable the stop button later when needed
    reanalyze_button_iq.config(state="disabled")  # Disable the reanalyze button
    reanalyze_button_sc.config(state="disabled")  # Disable the reanalyze button
    browse_button_synced_files_iq.config(state="disabled")
    browse_button_analyzed_files_iq.config(state="disabled")
    browse_button_synced_files_sc.config(state="disabled")
    browse_button_analyzed_files_sc.config(state="disabled")
    for ifolder_entry_list in folder_entry_list:
        ifolder_entry_list.config(state="disabled")
    # Run your analyze_data logic here
    print("Analyzing data...")

    unanalyzed_files_iq=[]
    thread_list_iq=[]
    sync_thread_iq = threading.Thread(target=analyze_files_worker_iq, args=(default_path_synced_files_iq,default_path_analyzed_files_iq,file_listbox_iq,file_listbox_sc,start_button_analysis,should_stop_analyze,folder_entry_value_list,unanalyzed_files_iq,thread_list_iq))
    sync_thread_iq.start()
    
    sync_thread_sc = threading.Thread(target=analyze_files_worker_sc,args=(default_path_synced_files_sc,default_path_analyzed_files_sc,file_listbox_iq,file_listbox_sc,start_button_analysis,should_stop_analyze))
    sync_thread_sc.start()
    
def ini_file_listbox(file_listbox_iq):
    existing_items = file_listbox_iq.get(0, tk.END)
    for file in existing_items:
        index = file_listbox_iq.get(0, tk.END).index(file)
        file_listbox_iq.itemconfig(index, {'bg': 'white'})
        file_listbox_iq.yview_moveto(0)
        
def reanalyze_sync_iq(file_listbox_iq,default_path_analyzed_files_iq,file_listbox_sc,default_path_analyzed_files_sc):
    try:
        os.remove("analyzed_files_iq.txt")
        os.remove("synced_files_iq.txt")
        print("analyzed_files_iq.txt has been deleted.")
        print("synced_files_iq.txt has been deleted.")
    except FileNotFoundError:
        print("analyzed_files_iq.txt not found. No action taken.")
        print("synced_files_iq.txt not found. No action taken.")
    ini_file_listbox(file_listbox_iq)

def reanalyze_sync_sc(file_listbox_iq,default_path_analyzed_files_iq,file_listbox_sc,default_path_analyzed_files_sc):
    try:
        os.remove("analyzed_files_sc.txt")
        os.remove("synced_files_sc.txt")
        print("analyzed_files_sc.txt has been deleted.")
        print("synced_files_sc.txt has been deleted.")
    except FileNotFoundError:
        print("analyzed_files_sc.txt not found. No action taken.")
        print("synced_files_sc.txt not found. No action taken.")
    ini_file_listbox(file_listbox_sc)
    
def stop_analyze_worker(stop_button,start_button_analysis,folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc,folder_entry_analyzed_files_sc,reanalyze_button_iq,reanalyze_button_sc,browse_button_synced_files_iq,browse_button_analyzed_files_iq,browse_button_synced_files_sc,browse_button_analyzed_files_sc,should_stop_analyze,folder_entry_list,file_listbox_iq,file_listbox_sc):
    while should_stop_analyze[0]: # keep the threading runing until should_stop_analyze[0] = True.
        yellow_files_iq = []  # # Used to store file names with yellow color
        for item_index in range(file_listbox_iq.size()):
            item_color = file_listbox_iq.itemcget(item_index, 'bg')
            item_name = file_listbox_iq.get(item_index)
            if item_color == 'yellow':
                yellow_files_iq.append(item_name)
        yellow_files_sc = []  # # Used to store file names with yellow color
        
        for item_index in range(file_listbox_sc.size()):
            item_color = file_listbox_sc.itemcget(item_index, 'bg')
            item_name = file_listbox_sc.get(item_index)
            if item_color == 'yellow':
                yellow_files_sc.append(item_name)
        
        if len(yellow_files_iq) != 0 or len(yellow_files_sc) !=0:
            # Blink the stop_button by changing its background color
            stop_button.config(bg='yellow')
            time.sleep(0.5)
            stop_button.config(bg='green')
            time.sleep(0.5)
        else:
            # No yellow items, stop blinking
            time.sleep(1)
            should_stop_analyze[0]=False
            #original_bg_color = start_button_analysis.cget('bg')
            #stop_button.config(bg=original_bg_color)  # Restore the original color
            start_button_analysis.config(state=tk.NORMAL)
            folder_entry_synced_files_iq.config(state="normal")  # Enable user input
            folder_entry_analyzed_files_iq.config(state="normal")  # Enable user input
            folder_entry_synced_files_sc.config(state="normal")  # Enable user input
            folder_entry_analyzed_files_sc.config(state="normal")  # Enable user input
            reanalyze_button_iq.config(state="normal")  # Enable reanalyze_button_iq
            reanalyze_button_sc.config(state="normal")  # Enable reanalyze_button_sc
            browse_button_synced_files_iq.config(state="normal")
            browse_button_analyzed_files_iq.config(state="normal")
            browse_button_synced_files_sc.config(state="normal")
            browse_button_analyzed_files_sc.config(state="normal")
            for obj in folder_entry_list:
                obj.config(state="normal")
            
def stop_analyze(stop_button,start_button_analysis,folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc,folder_entry_analyzed_files_sc,reanalyze_button_iq,reanalyze_button_sc,browse_button_synced_files_iq,browse_button_analyzed_files_iq,browse_button_synced_files_sc,browse_button_analyzed_files_sc,should_stop_analyze,folder_entry_list,file_listbox_iq,file_listbox_sc):
    should_stop_analyze[0] = True
    stop_button.config(state=tk.DISABLED)  # Disable the stop button
    stop_analyze_worker_thread = threading.Thread(target=stop_analyze_worker, args=(stop_button,start_button_analysis,folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc,folder_entry_analyzed_files_sc,reanalyze_button_iq,reanalyze_button_sc,browse_button_synced_files_iq,browse_button_analyzed_files_iq,browse_button_synced_files_sc,browse_button_analyzed_files_sc,should_stop_analyze,folder_entry_list,file_listbox_iq,file_listbox_sc))
    stop_analyze_worker_thread.start()
         
def start_online_server_worker(should_stop_online_server):
        #print("start_online_server_worker")
        time.sleep(1)
        if not should_stop_online_server[0]: 
                command = f"../CSR_Online_Server/CSR_Online_Server"
                try:
                        print("start_online_server_worker") 
                        subprocess.run(command, shell=True, check=True)
                        
                except subprocess.CalledProcessError:
                        print("CSR_Online_Server stops running.")

def start_online_server(start_button_online_server,stop_button_online_server, should_stop_online_server, update_button_online_server, should_stop_update_online_server):
    print(" start_online_server")
    should_stop_online_server[0] = False
    start_button_online_server.config(state="disabled")  # Disable the start button during syncing
    stop_button_online_server.config(state=tk.NORMAL) # Enable the stop button later when needed

    # Remove CSR_Online_Server_status.txt if it exists
    try:
            os.remove("CSR_Online_Server_status.txt")
    except FileNotFoundError:
            pass  # Ignore if the file doesn't exist
    
    thread_start_online_server = threading.Thread(target=start_online_server_worker,args=(should_stop_online_server,))
    thread_start_online_server.start()
    should_stop_update_online_server[0] = True
    update_online_server(update_button_online_server,stop_button_online_server, should_stop_update_online_server)    
                        
def update_online_server_worker(should_stop_update_online_server):
    while not should_stop_update_online_server[0]:
        print("update_online_server_worker")
        # Find processes with the name "CSR_Online_Serv"
        online_server_procs = [p for p in psutil.process_iter(attrs=['name']) if p.info['name'] == 'CSR_Online_Server']
        if online_server_procs:
        # Get the PID of the first matching process
            online_server_pid = online_server_procs[0].pid
            print(f"online_server pid: {online_server_pid}")
            # Send signal 10 (SIGUSR1) to the process; you can replace it with the desired signal
            try:
                    os.kill(online_server_pid, 10)
                    print(f"Sent signal 10 to online_server (PID {online_server_pid})")
            except ProcessLookupError:
                    print("Process not found")
        time.sleep(10)  # Wait for 60 seconds after each operation
        
def update_online_server(update_button_online_server,stop_button_online_server, should_stop_update_online_server):
        while should_stop_update_online_server[0]:
                try:
                        with open("CSR_Online_Server_status.txt", "r") as file:
                                content = file.read().strip()
                                
                        # Check if the content is not empty
                        if content and "Return value: 1" in content:
                                should_stop_update_online_server[0] = False
                                update_button_online_server.config(state="disabled")  # Disable the start button during syncing
                                thread_update_online_server = threading.Thread(target=update_online_server_worker, args=(should_stop_update_online_server,))
                                thread_update_online_server.start()
                                break  # Exit the loop if actions are performed
                        
                except Exception as e:
                        print(f"Online server is not ready. Please wait.")
                        
                time.sleep(1)
    
    
def stop_online_server(start_button_online_server,update_button_online_server,stop_button_online_server, should_stop_online_server,should_stop_update_online_server):
        should_stop_online_server[0] = True
        should_stop_update_online_server[0] = True
        print(" stop_online_server")
        if should_stop_online_server[0]:
                start_button_online_server.config(state=tk.NORMAL)  # Disable the start button during syncing
                update_button_online_server.config(state=tk.NORMAL)  # Disable the start button during syncing
                stop_button_online_server.config(state="disabled") # Enable the stop button later when needed
        
                command = f"killall -9 CSR_Online_Server"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("stop CSR_Online_Server faild!")
def start_roody_worker(should_stop_roody):
        #time.sleep(40)  
        if not should_stop_roody[0]:  
                command = f"../roody/bin/roody -H127.0.0.1:9092"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("roody stops running.")
        
def start_roody(start_button_roody,stop_button_roody, should_stop_roody):
    print(" start_roody")
    should_stop_roody[0] = False
    start_button_roody.config(state="disabled")  # Disable the start button during syncing
    stop_button_roody.config(state=tk.NORMAL) # Enable the stop button later when needed
    
    thread_start_roody = threading.Thread(target=start_roody_worker,args=(should_stop_roody,))
    thread_start_roody.start()

def stop_roody(start_button_roody,stop_button_roody, should_stop_roody):
        should_stop_roody[0] = True
        print(" stop_roody")
        if should_stop_roody[0]:
                start_button_roody.config(state=tk.NORMAL)  # Disable the start button during syncing
                stop_button_roody.config(state="disabled") # Enable the stop button later when needed
                command = f"killall -9 roody"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("stop roody faild!")
                        
def set_listbox_iterm_color(file_listbox, file, color="green"):
    # Update the listbox item color
    file_list_items = file_listbox.get(0, tk.END)  # Get all items in the listbox
    if file in file_list_items:
        index = file_listbox.get(0, tk.END).index(file)
        file_listbox.itemconfig(index, {'bg': color})
        
def update_file_list(file_listbox,directory,analyzed_files_name="analyzed_files_iq.txt",end=".iq.tdms"):
    # Get the current items in the file_listbox
    existing_items = file_listbox.get(0, tk.END)
    files = list_files_in_directory(directory,end)
    scroll_position=0
    
    for file in files:
        if file not in existing_items:  # Only add new files
            file_listbox.insert(tk.END, file)
    
    analyzed_files=get_files(analyzed_files_name)
    for file in files:
        file_fullpath=directory+"/"+file
        if file_fullpath in analyzed_files:
            set_listbox_iterm_color(file_listbox, file, "green")
    
def update_file_list_iq_sc(file_listbox_iq,folder_entry_synced_files_iq,file_listbox_sc,folder_entry_synced_files_sc):    
    default_path_synced_files_iq  = folder_entry_synced_files_iq.get()
    default_path_synced_files_sc  = folder_entry_synced_files_sc.get()     
    update_file_list(file_listbox_iq,default_path_synced_files_iq,"analyzed_files_iq.txt",".iq.tdms")# Update the file list with the new directory
    update_file_list(file_listbox_sc,default_path_synced_files_sc,"analyzed_files_sc.txt",".sc.tdms")# Update the file list with the new directory
    print("update_file_list_iq_sc completed!")
    
def read_paths_file(default_path_synced_files_iq, default_path_analyzed_files_iq, paths="paths_iq.txt"):
    try:
        with open(paths, "r") as file:
            lines = file.readlines()
            return lines[0].strip(), lines[1].strip()
    except FileNotFoundError:
        return default_path_synced_files_iq, default_path_analyzed_files_iq
    
def create_folder_entry(root,num_threads, text="NUM_THREADS:", row=4, column=0):
    comment_label_num_threads = tk.Label(root, text=text)
    comment_label_num_threads.grid(row=row, column=column, padx=10, pady=10, sticky="w")  # Left-aligned
    # Create an Entry widget for num_threads
    folder_entry_num_threads = tk.Entry(root,width=10)
    folder_entry_num_threads.grid(row=row, column=column+1, padx=10, pady=10, sticky="w")  # Left-aligned
    folder_entry_num_threads.insert(0, num_threads)  # Insert the default path
    return comment_label_num_threads, folder_entry_num_threads

def read_parameters_from_file(file_path, parameters):
    # Open the parameter file and read its contents
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    
    # Parse the contents of the parameter file line by line
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            if key in parameters:
                parameters[key] = value
                    
    return parameters

def load_arguments_worker(config, folder_entry_list, file_listbox_iq, file_listbox_sc):
        file_path = filedialog.askopenfilename(title="Load Parameter File")
        config = load_arguments(file_path)
        if file_path:
                file_listbox_iq.delete(0,tk.END)
                file_listbox_sc.delete(0,tk.END)
        
        for entry, arg_name in zip(folder_entry_list, config.keys()):
                entry.delete(0, tk.END)
                entry.insert(0, config[arg_name])
        # Conditionally execute update_file_list if args.default_path_synced_files_iq is not equal to 0
        if config["default_path_synced_files_iq"] != 0:
                update_file_list(file_listbox_iq, config["default_path_synced_files_iq"], "analyzed_files_iq.txt", ".iq.tdms")
        if config["default_path_synced_files_sc"] != 0:
                update_file_list(file_listbox_sc, config["default_path_synced_files_sc"], "analyzed_files_sc.txt", ".sc.tdms")
        
def save_arguments_worker(config, folder_entry_list):
        file_path = filedialog.asksaveasfilename(
                title="Save Parameter File",
                defaultextension=".toml",
                filetypes=[("TOML files", "*.toml"), ("All files", "*.*")])
        
        if file_path:
                print(" save_parameters ", file_path)
                
                # Update values in the config dictionary
                for entry, arg_name in zip(folder_entry_list, config.keys()):
                        value = entry.get()
                        # Convert numeric values to appropriate types
                        if arg_name in ['num_threads', 'FramesStep', 'WeightType', 'PlotOption',
                                        'FramesPerPlot', 'FFTFreqLow', 'FFTFreqSpan', 'FFTFreqBin',
                                        'FFTNrOfFrames', 'FFTFrameBin', 'WorkMode']:
                                value = int(value)
                                config[arg_name] = value
                                
                # Save the config dictionary to the TOML file
                with open(file_path, 'w') as file:
                        toml.dump(config, file)
                
def load_arguments(config_file_path):
        try:
                # Load parameters from the TOML file
                with open(config_file_path, 'r') as config_file:
                        config = toml.load(config_file)
        except FileNotFoundError:
                print(f"Error: File '{config_file_path}' not found.")
                # You might want to handle this error by providing a default configuration or exiting the program.
                with open("parameters_default.toml", 'r') as config_file:
                        config = toml.load(config_file)
        return config

def has_display():
        try:
                # Try to get the DISPLAY environment variable
                display = os.environ['DISPLAY']
                
                print("#################################################################")
                print("#####Video output display detected. display", display," #####")
                print("#####X server Reminder:", "Please ensure that X server is running before executing the script.#####")
                print("#################################################################\n\n")
                return True
        except KeyError:
                # If DISPLAY environment variable is not set, there might not be a graphical display
                return False
        
            
######################################################################
def main():
        
        if len(sys.argv) != 2:
                print("Usage: Analyze_iq_sc <path_to_config_file>")
                sys.exit(1)
                
        config_file_path = sys.argv[1]
        # Check if there is a display
        if not has_display():
                print("No video output display detected.")
                # You can add appropriate handling here, such as switching to a non-graphical mode or other logic
                sys.exit(1)
                
                
        # Create the main window
        root = tk.Tk()
        root.title("Analyze data.")
        
        # Set the custom window size (width x height)
        window_width = 1200
        window_height = 800

        should_stop_analyze = [True]
        should_stop_update_online_server = [True]
        should_stop_online_server = [True]
        should_stop_roody = [True]
        root.geometry(f"{window_width}x{window_height}")
        
        config = load_arguments(config_file_path)
        default_path_synced_files_iq = config["default_path_synced_files_iq"]
        default_path_analyzed_files_iq = config["default_path_analyzed_files_iq"]
        default_path_synced_files_sc = config["default_path_synced_files_sc"]
        default_path_analyzed_files_sc = config["default_path_analyzed_files_sc"]
        num_threads = config["num_threads"]
        FramesStep = config["FramesStep"]
        WeightType = config["WeightType"]
        PlotOption = config["PlotOption"]
        FramesPerPlot = config["FramesPerPlot"]
        FFTFreqLow = config["FFTFreqLow"]
        FFTFreqSpan=config["FFTFreqSpan"]
        FFTFreqBin=config["FFTFreqBin"]
        FFTNrOfFrames=config["FFTNrOfFrames"]
        FFTFrameBin=config["FFTFrameBin"]
        WorkMode=config["WorkMode"]
        
        # Create a menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # Create a "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add a "Load Parameter" option to the "File" menu
        file_menu.add_command(label="Load Parameter", command=lambda:load_arguments_worker(config,folder_entry_list, file_listbox_iq, file_listbox_sc))
        
        # Add a "Save Parameter" option to the "File" menu
        file_menu.add_command(label="Save Parameter", command=lambda:save_arguments_worker(config,folder_entry_list))
        
        ## Create a Label for synced_files_iq
        comment_label_synced_files_iq = tk.Label(root, text="SYNCED_FILES_IQ:")
        comment_label_synced_files_iq.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Left-aligned
        # Create an Entry widget for synced_files_iq
        folder_entry_synced_files_iq = tk.Entry(root,width=90)
        folder_entry_synced_files_iq.grid(row=0, column=1, columnspan=4,padx=10, pady=10, sticky="w")  # Left-aligned
        folder_entry_synced_files_iq.insert(0, default_path_synced_files_iq)  # Insert the default path
        
        ## Create a Label for analyzed_files_iq
        comment_label_analyzed_files_iq = tk.Label(root, text="ANALYZED_FILES_IQ:")
        comment_label_analyzed_files_iq.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Left-aligned
        # Create an Entry widget for analyzed_files_iq
        folder_entry_analyzed_files_iq = tk.Entry(root,width=90)
        folder_entry_analyzed_files_iq.grid(row=1, column=1, columnspan=4,padx=10, pady=10, sticky="w")  # Left-aligned
        folder_entry_analyzed_files_iq.insert(0, default_path_analyzed_files_iq)  # Insert the default path
    
        ## Create a Label for synced_files_sc
        comment_label_synced_files_sc = tk.Label(root, text="SYNCED_FILES_SC:")
        comment_label_synced_files_sc.grid(row=2, column=0, padx=10, pady=10, sticky="w")  # Left-aligned
        # Create an Entry widget for synced_files_sc
        folder_entry_synced_files_sc = tk.Entry(root,width=90)
        folder_entry_synced_files_sc.grid(row=2, column=1,columnspan=4, padx=10, pady=10, sticky="w")  # Left-aligned
        folder_entry_synced_files_sc.insert(0, default_path_synced_files_sc)  # Insert the default path
        
        ## Create a Label for analyzed_files_sc
        comment_label_analyzed_files_sc = tk.Label(root, text="ANALYZED_FILES_SC:")
        comment_label_analyzed_files_sc.grid(row=3, column=0, padx=10, pady=10, sticky="w")  # Left-aligned
        # Create an Entry widget for analyzed_files_sc
        folder_entry_analyzed_files_sc = tk.Entry(root,width=90)
        folder_entry_analyzed_files_sc.grid(row=3, column=1, columnspan=4,padx=10, pady=10, sticky="w")  # Left-aligned
        folder_entry_analyzed_files_sc.insert(0, default_path_analyzed_files_sc)  # Insert the default path
        
        ## Create the file listbox
        file_listbox_iq = tk.Listbox(root, width = 30,height=25)  # Adjust the height as needed
        file_listbox_iq.grid(row=4, column=2, rowspan=9, padx=10, pady=10, sticky="w")  # Left-aligned
        # Create a vertical scrollbar for the file listbox
        file_listbox_iq_scrollbar = tk.Scrollbar(root, orient="vertical")
        file_listbox_iq_scrollbar.grid(row=4, column=2, rowspan=9,sticky="nse")  # Right-aligned    
        # Associate the scrollbar with the file listbox
        file_listbox_iq.config(yscrollcommand=file_listbox_iq_scrollbar.set)
        file_listbox_iq_scrollbar.config(command=file_listbox_iq.yview)
        update_file_list(file_listbox_iq,default_path_synced_files_iq,"analyzed_files_iq.txt",".iq.tdms")  # Update the file list in file_listbox_iq with default path
        
        ## Create the file listbox
        file_listbox_sc = tk.Listbox(root, width = 30,height=25)  # Adjust the height as needed
        file_listbox_sc.grid(row=4, column=3, rowspan=9,padx=10, pady=10, sticky="ns")  # Left-aligned
        # Create a vertical scrollbar for the file listbox
        file_listbox_sc_scrollbar = tk.Scrollbar(root, orient="vertical")
        file_listbox_sc_scrollbar.grid(row=4, column=3, rowspan=9,sticky="nse")  # Right-aligned
        # Associate the scrollbar with the file listbox
        file_listbox_sc.config(yscrollcommand=file_listbox_sc_scrollbar.set)
        file_listbox_sc_scrollbar.config(command=file_listbox_sc.yview)
        update_file_list(file_listbox_sc,default_path_synced_files_sc,"analyzed_files_sc.txt",".sc.tdms")  # Update the file list in file_listbox_iq with default path
        
        ## Create a "Browse" button for folder selection
        browse_button_synced_files_iq = tk.Button(root, text="Browse", command=lambda: browse_folder_and_update_list_filebox(folder_entry_synced_files_iq,default_path_synced_files_iq,file_listbox_iq,"analyzed_files_iq.txt",".iq.tdms"))
        browse_button_synced_files_iq.grid(row=0, column=6, padx=10, pady=10, sticky="w")  # Left-aligned
        
        ## Create a "Browse" button for folder selection
        browse_button_analyzed_files_iq = tk.Button(root, text="Browse", command=lambda: browse_folder(folder_entry_analyzed_files_iq,default_path_analyzed_files_iq))
        browse_button_analyzed_files_iq.grid(row=1, column=6, padx=10, pady=10, sticky="w")  # Left-aligned
        
        # Create a "Browse" button for folder selection
        browse_button_synced_files_sc = tk.Button(root, text="Browse", command=lambda: browse_folder_and_update_list_filebox(folder_entry_synced_files_sc,default_path_synced_files_sc,file_listbox_sc,"analyzed_files_sc.txt",".sc.tdms"))
        browse_button_synced_files_sc.grid(row=2, column=6, padx=10, pady=10, sticky="w")  # Left-aligned
    
        # Create a "Browse" button for folder selection
        browse_button_analyzed_files_sc = tk.Button(root, text="Browse", command=lambda: browse_folder(folder_entry_analyzed_files_sc,default_path_analyzed_files_sc))
        browse_button_analyzed_files_sc.grid(row=3, column=6, padx=10, pady=10, sticky="w")  # Left-aligned
    
        
        ### Create the "Start" button
        unanalyzed_files_iq=[]
        thread_list_iq=[]
        
        object_list=[]
    
        start_button_analysis = ttk.Button(root, text="Start analysis", command=lambda:analyze_data(start_button_analysis,stop_button,folder_entry_synced_files_iq, folder_entry_analyzed_files_iq,folder_entry_synced_files_sc,folder_entry_analyzed_files_sc,default_path_synced_files_iq,default_path_analyzed_files_iq,file_listbox_iq,file_listbox_sc, reanalyze_button_iq,reanalyze_button_sc,browse_button_synced_files_iq,browse_button_analyzed_files_iq,browse_button_synced_files_sc, browse_button_analyzed_files_sc,should_stop_analyze,folder_entry_list,unanalyzed_files_iq,thread_list_iq))
        start_button_analysis.configure(style="TButton")
        start_button_analysis.grid(row=0, column=7, padx=5, pady=10, sticky="w")
        
        
        ### Create the "Stop" button
        stop_button = tk.Button(root, text="Stop analysis", command=lambda:stop_analyze(stop_button,start_button_analysis,folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc,folder_entry_analyzed_files_sc,reanalyze_button_iq,reanalyze_button_sc,browse_button_synced_files_iq,browse_button_analyzed_files_iq, browse_button_synced_files_sc, browse_button_analyzed_files_sc, should_stop_analyze,folder_entry_list,file_listbox_iq,file_listbox_sc))
        
        stop_button.grid(row=0, column=8, padx=5, pady=10, sticky="w")  # Left-aligned
    
        start_button_online_server = tk.Button(root, text="Start online server", command=lambda:start_online_server(start_button_online_server,stop_button_online_server,should_stop_online_server, update_button_online_server,should_stop_update_online_server))
        start_button_online_server.grid(row=1, column=7, padx=5, pady=10, sticky="w")  # Left-aligned
        
        update_button_online_server = tk.Button(root, text="Update online server(60)", command=lambda:update_online_server(update_button_online_server,stop_button_online_server,should_stop_update_online_server))
        update_button_online_server.grid(row=1, column=8, padx=5, pady=10, sticky="w")  # Left-aligned
               
        stop_button_online_server = tk.Button(root, text="Stop online server", command=lambda:stop_online_server(start_button_online_server,update_button_online_server,stop_button_online_server,should_stop_online_server,should_stop_update_online_server))
        stop_button_online_server.grid(row=1, column=9, padx=5, pady=10, sticky="w")  # Left-aligned
        
        start_button_roody = tk.Button(root, text="Start roody", command=lambda:start_roody(start_button_roody,stop_button_roody,should_stop_roody))
        start_button_roody.grid(row=2, column=7, padx=5, pady=10, sticky="w")  # Left-aligned

        stop_button_roody = tk.Button(root, text="Stop roody", command=lambda:stop_roody(start_button_roody,stop_button_roody,should_stop_roody))
        stop_button_roody.grid(row=2, column=9, padx=5, pady=10, sticky="w")  # Left-aligned
    
        ## Create the "Reanalyze" button iq
        reanalyze_button_iq = tk.Button(root, text="Re-analyze(IQ)", command=lambda:reanalyze_sync_iq(file_listbox_iq,default_path_synced_files_iq,file_listbox_sc,default_path_synced_files_sc))
        reanalyze_button_iq.grid(row=13, column=2, padx=5, pady=10, sticky="w")  # Left-aligned
        
        ## Create the "Reanalyze" button sc
        reanalyze_button_sc = tk.Button(root, text="Re-analyze(SC)", command=lambda:reanalyze_sync_sc(file_listbox_iq,default_path_synced_files_iq,file_listbox_sc,default_path_synced_files_sc))
        reanalyze_button_sc.grid(row=13, column=3, padx=5, pady=10, sticky="w")  # Left-aligned
           
        comment_label_num_threads,  folder_entry_num_threads  = create_folder_entry(root, num_threads,  "NUM_THREADS:",   4, 0)
        comment_label_FramesStep,   folder_entry_FramesStep   = create_folder_entry(root, FramesStep,   "FramesStep:",    5, 0)
        comment_label_WeightType,   folder_entry_WeightType   = create_folder_entry(root, WeightType,   "WeightType:",    6, 0)
        comment_label_PlotOption,   folder_entry_PlotOption   = create_folder_entry(root, PlotOption,   "PlotOption:",    7, 0)
        comment_label_FramesPerPlot,folder_entry_FramesPerPlot= create_folder_entry(root, FramesPerPlot,"FramesPerPlot:", 8, 0)
        comment_label_FFTFreqLow,   folder_entry_FFTFreqLow   = create_folder_entry(root, FFTFreqLow,   "FFTFreqLow:",    9, 0)
        comment_label_FFTFreqSpan,  folder_entry_FFTFreqSpan  = create_folder_entry(root, FFTFreqSpan,  "FFTFreqSpan:",  10, 0)
        comment_label_FFTFreqBin,   folder_entry_FFTFreqBin   = create_folder_entry(root, FFTFreqBin,   "FFTFreqBin:",   11, 0)
        comment_label_FFTNrOfFrames,folder_entry_FFTNrOfFrames= create_folder_entry(root, FFTNrOfFrames,"FFTNrOfFrames:",12, 0)
        comment_label_FFTFrameBin,  folder_entry_FFTFrameBin  = create_folder_entry(root, FFTFrameBin,  "FFTFrameBin:",  13, 0)
        comment_label_WorkMode,     folder_entry_WorkMode     = create_folder_entry(root, WorkMode,     "WorkMode:",     14, 0)
    
        folder_entry_list =[folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc,folder_entry_analyzed_files_sc,folder_entry_num_threads,folder_entry_FramesStep,folder_entry_WeightType,folder_entry_PlotOption,folder_entry_FramesPerPlot,folder_entry_FFTFreqLow,folder_entry_FFTFreqSpan,folder_entry_FFTFreqBin,folder_entry_FFTNrOfFrames,folder_entry_FFTFrameBin,folder_entry_WorkMode]
        
        # Run the main loop
        root.mainloop()

if __name__ == "__main__":
    main()
