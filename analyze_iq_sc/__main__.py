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
import shutil
def generated_file_offline_mode(default_path_synced_files_iq,  default_path_analyzed_files_iq, default_path_synced_files_sc,default_path_analyzed_files_sc):
        #print(".... generated_file_offline_mode ...")
        file_iq = list_files_in_directory(default_path_synced_files_iq,".iq.tdms")
        for file in file_iq:
                add_file("synced_files_iq.txt",default_path_synced_files_iq, file, 0,"","")
                
        # Path to the synced_files_iq.txt file in the current directory
        source_file_iq = "synced_files_iq.txt"
        # Destination path where the file will be copied to
        destination_iq = os.path.join(default_path_synced_files_iq, "synced_files_iq.txt")
        # Copy the file to the destination
        shutil.copy(source_file_iq, destination_iq)
                                
        file_sc = list_files_in_directory(default_path_synced_files_sc,".sc.tdms")
        for file in file_sc:
                add_file("synced_files_sc.txt",default_path_synced_files_sc, file, 0,"","")
        # Path to the synced_files_sc.txt file in the current directory
        source_file_sc = "synced_files_sc.txt"
        # Destination path where the file will be copied to
        destination_sc = os.path.join(default_path_synced_files_sc, "synced_files_sc.txt")
        # Copy the file to the destination
        shutil.copy(source_file_sc, destination_sc)
         
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

def replace_path_segment(default_path, selected_directory):
        # Extract the last part of the selected_directory, e.g., 'IQ_2021-05-09_23-56-42'
        selected_segment = os.path.basename(selected_directory)
        
        # Split the default_path into its individual parts
        path_parts = default_path.split('/')
        
        # Assuming the second-to-last part needs to be replaced (based on the path structure)
        path_parts[-1] = selected_segment
        
        # Reassemble the path
        new_path = '/'.join(path_parts)
        return new_path


def browse_folder_and_update_list_filebox(folder_entry, default_path_synced_files, default_path_analyzed_files,file_listbox, analyzed_files_name="analyzed_files_iq.txt",end=".iq.tdms"):
    selected_directory = filedialog.askdirectory(initialdir=default_path_synced_files)
    if selected_directory:
        folder_entry.delete(0, tk.END)  # Clear previous entry
        folder_entry.insert(0, selected_directory)
        file_listbox.delete(0, tk.END)
        #print("default_path_analyzed_files ",default_path_analyzed_files)
        #print("selected_directory ",selected_directory)
        updated_analyzed_files = replace_path_segment(default_path_analyzed_files, selected_directory)
        update_file_list(file_listbox,selected_directory,updated_analyzed_files,analyzed_files_name,end)
        
def browse_folder(folder_entry, default_path):
    selected_directory = filedialog.askdirectory(initialdir=default_path)
    #print("chenrj ... browse_folder")
    if selected_directory:
        folder_entry.delete(0, tk.END)  # Clear previous entry
        folder_entry.insert(0, selected_directory)

def get_files(files_file = "analyzed_files_iq.txt"):
        if os.path.exists(files_file):
                with open(files_file, "r") as file:
                        #files = file.read().splitlines()
                        #files = [line.split()[0] for line in file.read().splitlines()]
                        files = [line.split()[0] for line in file.read().splitlines() if line.strip()]
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
            
#def add_file(output_file,directory1, file1_name, elapsed_time, directory2, file2_name):
#        # Prepend directory2 to the output_file path
#        output_path = directory2 + "/" + output_file
#        
#        with open(output_path, "a") as file:
#                file.write(directory1 + "/" + file1_name +"  " + str(elapsed_time)+ " [second] "+ directory2 + "/" + file2_name + "\n")

def add_file(output_file, directory1, file1_name, elapsed_time, directory2, file2_name):
        # Prepend directory2 to the output_file path
        output_path = directory2 + "/" + output_file
        
        # Create the line to be added to the file
        new_line = directory1 + "/" + file1_name + "  " + str(elapsed_time) + " [second] " + directory2 + "/" + file2_name + "\n"

        # Extract the part to check for existence in the file
        part_to_check = directory1 + "/" + file1_name
        
        # Open the file and check if the new line already exists
        try:
                with open(output_path, "r+") as file:
                        contents = file.read()
                        if part_to_check not in contents:
                        #if new_line not in file.read():
                                file.write(new_line)
        except FileNotFoundError:
                # If the file does not exist, create it and write the line
                with open(output_path, "w") as file:
                        file.write(new_line)
                        

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
    
    current_file_index = files.index(current_file_name) if current_file_name in files else None
    if current_file_index is not None:
        scroll_position = max(0, (current_file_index - 2) / len(files))  # You might want to adjust the offset
        file_listbox.yview_moveto(scroll_position)            

def thread_subprocess_iq(thread_file,file_listbox_synced_files_iq,should_stop_analyze,synced_files,folder_entry_dic):
    file= thread_file
    start_time = time.time()  # Record the start time
    default_path_synced_files_iq  = folder_entry_dic.get('synced_files_iq', None).get()
    default_path_analyzed_files_iq= folder_entry_dic.get('analyzed_files_iq', None).get()
    
    FramesStep   = folder_entry_dic.get("FramesStep", "Default Value if not found").get()
    WeightType   = folder_entry_dic.get("WeightType", "Default Value if not found").get()
    PlotOption   = folder_entry_dic.get("PlotOption", "Default Value if not found").get()
    FramesPerPlot= folder_entry_dic.get("FramesPerPlot", "Default Value if not found").get()
    FFTFreqLow   = folder_entry_dic.get("FFTFreqLow", "Default Value if not found").get()
    FFTFreqSpan  = folder_entry_dic.get("FFTFreqSpan", "Default Value if not found").get()
    FFTFreqBin   = folder_entry_dic.get("FFTFreqBin", "Default Value if not found").get()
    FFTNrOfFrames= folder_entry_dic.get("FFTNrOfFrames", "Default Value if not found").get()
    FFTFrameBin  = folder_entry_dic.get("FFTFrameBin", "Default Value if not found").get()
    # Print values to verify
    #print("FramesStep:", FramesStep)
    #print("WeightType:", WeightType)
    #print("PlotOption:", PlotOption)
    #print("FramesPerPlot:", FramesPerPlot)
    #print("FFTFreqLow:", FFTFreqLow)
    #print("FFTFreqSpan:", FFTFreqSpan)
    #print("FFTNrOfFrames:", FFTNrOfFrames)
    #print("FFTFrameBin:", FFTFrameBin)
    
    #   = folder_entry_dic.get("", "Default Value if not found")
    #FramesStep   = folder_entry_dic.get("", "Default Value if not found")
    
    command = f"../iqt7/convert_iqt_iq {FramesStep} {WeightType} {PlotOption} {FramesPerPlot} {FFTFreqLow} {FFTFreqSpan} {FFTFreqBin} {FFTNrOfFrames} {FFTFrameBin}  {default_path_synced_files_iq}/{file} {default_path_analyzed_files_iq}/"
    #command = f"ls {default_path_synced_files_iq}/{file}"
    try:
        set_listbox_iterm_color(file_listbox_synced_files_iq, file, "yellow")

        #time.sleep(1)
        subprocess.run(command, shell=True, check=True)

        set_listbox_iterm_color(file_listbox_synced_files_iq, file, "green")
        adjust_scroll_position(file, synced_files, file_listbox_synced_files_iq) 
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        file_root = file+".root"
        add_file("analyzed_files_iq.txt",default_path_synced_files_iq, file, elapsed_time,default_path_analyzed_files_iq,file_root)
        
    except subprocess.CalledProcessError:
        print(f"Analyze file failed for: {file}")
        set_listbox_iterm_color(file_listbox_synced_files_iq, file, "red")
            
def analyze_files_worker_iq(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files, thread_list):    
    while not should_stop_analyze[0]: # keep the threading runing until should_stop_analyze[0] = True.
        default_path_synced_files_iq  = folder_entry_dic.get('synced_files_iq', None).get()
        default_path_analyzed_files_iq= folder_entry_dic.get('analyzed_files_iq', None).get()
        file_listbox_synced_files_iq  = file_listbox_dic.get('synced_files_iq', None)
        file_listbox_synced_files_sc  = file_listbox_dic.get('synced_files_sc', None)   
        start_button_analysis         = button_dic.get('start_button_analysis', None)
        if default_path_synced_files_iq:
            #print("chenrj ... ",a)
            update_file_list(file_listbox_synced_files_iq,default_path_synced_files_iq,default_path_analyzed_files_iq,"analyzed_files_iq.txt",".iq.tdms")
            #a = "synced_files_iq.txt"
            b = default_path_synced_files_iq + "/synced_files_iq.txt"
            files0 = get_files(b)
            #print("files0 ",b, " ",files0)
            synced_files = filter_files(files0,".iq.tdms")
            #analyzed_files = get_files("analyzed_files_iq.txt")
            a = default_path_analyzed_files_iq + "/analyzed_files_iq.txt"
            analyzed_files = get_files(a)
            for file in synced_files:
                if should_stop_analyze[0]:  # Check if user wants to stop analyzing
                    break
                        
                file_fullpath=default_path_synced_files_iq + "/" + file
                num_threads = int(folder_entry_dic.get("num_threads", "Default Value if not found").get())
                print("num_threads ",num_threads)
                if file_fullpath not in analyzed_files and file not in unanalyzed_files:
                    
                    while True and should_stop_analyze[0] ==False:
                        active_thread_number = 0
                        for thread in thread_list:
                            if thread.is_alive():
                                active_thread_number=active_thread_number+1
                        print(" active_thread_number is ",active_thread_number,". Wait for free CPU. file = ",file)
                        #print(" unanalyzed_files:",unanalyzed_files)
                        if active_thread_number<num_threads:
                            break
                        else:
                            time.sleep(1)
                    print("chenrj file  ",file)
                    unanalyzed_files.append(file)
                    print("chenrj ... synced_files",synced_files)
                    print("chenrj ... unanalyzed_files ",unanalyzed_files)
                    thread = threading.Thread(target=thread_subprocess_iq,args=(file,file_listbox_synced_files_iq,should_stop_analyze,synced_files,folder_entry_dic))
                    thread.start()
                    time.sleep(1) 
                    thread_list.append(thread)
        time.sleep(1)

def analyze_files_worker_sc(folder_entry_dic, file_listbox_dic, button_dic,should_stop_analyze):
    while not should_stop_analyze[0]: # keep the threading runing until should_stop_analyze[0] = True.
        default_path_synced_files_sc  = folder_entry_dic.get('synced_files_sc', None).get()
        default_path_analyzed_files_sc= folder_entry_dic.get('analyzed_files_sc', None).get()
                        
        file_listbox_synced_files_iq = file_listbox_dic.get('synced_files_iq', None)
        file_listbox_synced_files_sc = file_listbox_dic.get('synced_files_sc', None)
        start_button_analysis        = file_listbox_dic.get('start_button_analysis', None)
        if default_path_synced_files_sc:
            #print("chenrj ... default_path_synced_files_sc = ",default_path_synced_files_sc)
            update_file_list(file_listbox_synced_files_sc, default_path_synced_files_sc,default_path_analyzed_files_sc, "analyzed_files_sc.txt", ".sc.tdms")
            # Update the file list with the new directory
            b = default_path_synced_files_sc + "/synced_files_sc.txt"
            #a =  "synced_files_sc.txt"
            files0 =get_files(b)
            synced_files = filter_files(files0,".sc.tdms")
            
            for file in synced_files:
                if should_stop_analyze[0]:
                    #print("analyze_files_worker_sc has been pressed, you can close the program.")
                    break
                file_fullpath=default_path_synced_files_sc + "/" + file                
                #analyzed_files = get_files("analyzed_files_sc.txt")        
                a = default_path_analyzed_files_sc + "/analyzed_files_sc.txt"
                analyzed_files = get_files(a) 
                if file_fullpath not in analyzed_files:
                    start_time = time.time()  # Record the start time
                    command = f"../iqt7/convert_iqt_sc  -i {default_path_synced_files_sc}/{file}  -o {default_path_analyzed_files_sc}/"
                    #command = f"ls {default_path_synced_files_sc}/{file}"
                    try:
                        # Update the listbox item color
                        
                        set_listbox_iterm_color(file_listbox_synced_files_sc, file, "yellow")
                        #print("chenrj ... subprocess.run(command,")
                        subprocess.run(command, shell=True, check=True)
                        
                        end_time = time.time()  # Record the end time
                        elapsed_time = end_time - start_time
                        
                        # Update the listbox item color
                        #index = file_listbox_synced_files_sc.get(0, tk.END).index(file)
                        #file_listbox_synced_files_sc.itemconfig(index, {'bg': 'green'})
                        set_listbox_iterm_color(file_listbox_synced_files_sc, file, "green")
                        
                        adjust_scroll_position(file, synced_files, file_listbox_synced_files_sc)
                        file_root = file+".root"
                        #print("chenrj ... add_file")
                        add_file("analyzed_files_sc.txt",default_path_synced_files_sc, file, elapsed_time,default_path_analyzed_files_sc, file_root)
                        #update_file_list(file_listbox_synced_files_sc,default_path_synced_files_sc,default_path_analyzed_files_sc, "analyzed_files_sc.txt",".sc.tdms")# Update the file list with the new directory 
                    except subprocess.CalledProcessError:
                        print(f"Analyze file failed for: {file}")
                        set_listbox_iterm_color(file_listbox_synced_files_sc, file, "red")
            time.sleep(1)

def analyze_data(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files_iq, thread_list_iq):

    stop_button = button_dic.get('stop_button', None)
    
    folder_entry_synced_files_iq = folder_entry_dic.get('synced_files_iq', None)
    folder_entry_analyzed_files_iq = folder_entry_dic.get('analyzed_files_iq', None)
    folder_entry_synced_files_sc = folder_entry_dic.get('synced_files_sc', None)
    folder_entry_analyzed_files_sc = folder_entry_dic.get('analyzed_files_sc', None)
    folder_entry_injection_files = folder_entry_dic.get('injection_files', None)
    
    default_path_synced_files_iq  = folder_entry_dic.get('synced_files_iq', None).get()
    default_path_analyzed_files_iq= folder_entry_dic.get('analyzed_files_iq', None).get()
    default_path_synced_files_sc  = folder_entry_dic.get('synced_files_sc', None).get()
    default_path_analyzed_files_sc= folder_entry_dic.get('analyzed_files_sc', None).get()
    file_listbox_synced_files_iq = file_listbox_dic.get('synced_files_iq', None)
    file_listbox_synced_files_sc = file_listbox_dic.get('synced_files_sc', None)   
    file_listbox_synced_files_iq = file_listbox_dic.get('synced_files_iq', None)
    
    update_file_list(file_listbox_synced_files_iq,default_path_synced_files_iq, default_path_analyzed_files_iq, "analyzed_files_iq.txt",".iq.tdms")

    update_file_list(file_listbox_synced_files_sc, default_path_synced_files_sc, default_path_analyzed_files_sc,"analyzed_files_sc.txt", ".sc.tdms")# Update the file list with the new directory
    
    # Check and create directories if they do not exist
    if not os.path.exists(default_path_analyzed_files_iq):
        os.makedirs(default_path_analyzed_files_iq, exist_ok=True)
    if not os.path.exists(default_path_analyzed_files_sc):
        os.makedirs(default_path_analyzed_files_sc, exist_ok=True)
                                                
    if not check_parent_directory(folder_entry_synced_files_iq,folder_entry_analyzed_files_iq,folder_entry_synced_files_sc, folder_entry_analyzed_files_sc):
        return

    WorkMode = folder_entry_dic.get("WorkMode", "Default Value if not found").get()  #
    if WorkMode == 1:
        generated_file_offline_mode(default_path_synced_files_iq, default_path_analyzed_files_iq,default_path_synced_files_sc,default_path_analyzed_files_sc)

    should_stop_analyze[0] = False
    stop_button.config(state=tk.NORMAL) # Enable the stop button later when needed
    
    for key, button in button_dic.items():
            if key == "stop_button":
                    button.config(state=tk.NORMAL)  # Enable only the stop_button
            else:
                    button.config(state="disabled")  # Disable all other buttons
                    
    for entry_widget in folder_entry_dic.values():
            entry_widget.config(state="disabled")
    # Run your analyze_data logic here
    print("Analyzing data...")

    unanalyzed_files_iq=[]
    thread_list_iq=[]
    
    sync_thread_iq = threading.Thread(target=analyze_files_worker_iq, args=(folder_entry_dic,file_listbox_dic,button_dic,should_stop_analyze,unanalyzed_files_iq,thread_list_iq))
    sync_thread_iq.start()
    
    sync_thread_sc = threading.Thread(target=analyze_files_worker_sc,args=(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze))
    sync_thread_sc.start()
    
def ini_file_listbox(file_listbox_synced_files_iq):
    existing_items = file_listbox_synced_files_iq.get(0, tk.END)
    for file in existing_items:
        index = file_listbox_synced_files_iq.get(0, tk.END).index(file)
        file_listbox_synced_files_iq.itemconfig(index, {'bg': 'white'})
        file_listbox_synced_files_iq.yview_moveto(0)
        
def reanalyze_sync_iq(file_listbox_synced_files_iq,default_path_analyzed_files_iq,file_listbox_synced_files_sc,default_path_analyzed_files_sc):
    try:
        os.remove("analyzed_files_iq.txt")
        os.remove("synced_files_iq.txt")
        print("analyzed_files_iq.txt has been deleted.")
        print("synced_files_iq.txt has been deleted.")
    except FileNotFoundError:
        print("analyzed_files_iq.txt not found. No action taken.")
        print("synced_files_iq.txt not found. No action taken.")
    ini_file_listbox(file_listbox_synced_files_iq)

def reanalyze_sync_sc(file_listbox_synced_files_iq,default_path_analyzed_files_iq,file_listbox_synced_files_sc,default_path_analyzed_files_sc):
    try:
        os.remove("analyzed_files_sc.txt")
        os.remove("synced_files_sc.txt")
        print("analyzed_files_sc.txt has been deleted.")
        print("synced_files_sc.txt has been deleted.")
    except FileNotFoundError:
        print("analyzed_files_sc.txt not found. No action taken.")
        print("synced_files_sc.txt not found. No action taken.")
    ini_file_listbox(file_listbox_synced_files_sc)
    
def stop_analyze_worker(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files_iq, thread_list_iq):
    stop_button = button_dic.get('stop_button', None)
    file_listbox_synced_files_iq = file_listbox_dic.get('synced_files_iq', None)
    file_listbox_synced_files_sc = file_listbox_dic.get('synced_files_sc', None)   
    while should_stop_analyze[0]: # keep the threading runing until should_stop_analyze[0] = True.
        yellow_files_iq = []  # # Used to store file names with yellow color
        for item_index in range(file_listbox_synced_files_iq.size()):
            item_color = file_listbox_synced_files_iq.itemcget(item_index, 'bg')
            item_name = file_listbox_synced_files_iq.get(item_index)
            if item_color == 'yellow':
                yellow_files_iq.append(item_name)
        yellow_files_sc = []  # # Used to store file names with yellow color
        
        for item_index in range(file_listbox_synced_files_sc.size()):
            item_color = file_listbox_synced_files_sc.itemcget(item_index, 'bg')
            item_name = file_listbox_synced_files_sc.get(item_index)
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
            for key, button in button_dic.items():
                    if key == "stop_button":
                            button.config(state="disabled")  # Dusable only the stop_button
                    else:
                            button.config(state="normal")  # Enable all other buttons
            for entry_widget in folder_entry_dic.values():
                    entry_widget.config(state="normal")
                            
            break
    
def stop_analyze(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files_iq, thread_list_iq):
    stop_button = button_dic.get('stop_button', None)    
    should_stop_analyze[0] = True
    stop_button.config(state=tk.DISABLED)  # Disable the stop button
    stop_analyze_worker_thread = threading.Thread(target=stop_analyze_worker, args=(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files_iq, thread_list_iq))
    stop_analyze_worker_thread.start()
         
def start_online_server_worker(should_stop_online_server, path_to_analyzed_files_iq, path_to_analyzed_files_sc, default_path_injection_files, frameID_offset, frameID_range, range_sc, nx_sc, range_iq, nx_iq):
        time.sleep(1)
        if not should_stop_online_server[0]:
                command = f"killall -9 CSR_Online_Server"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("stop CSR_Online_Server faild!")
                command = f"killall -9 combine_injection"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("stop combine_injection faild!")
                
                #command = f"../CSR_Online_Server/CSR_Online_Server ../CSR_Online_Server/config.txt"
                command = (
                        "../CSR_Online_Server/CSR_Online_Server "
                        f"--path_to_analyzed_files_sc='{path_to_analyzed_files_sc}' "
                        f"--path_to_analyzed_files_iq='{path_to_analyzed_files_iq}' "
                        f"--default_path_injection_files='{default_path_injection_files}' "
                        f"--frameID_offset={frameID_offset} "
                        f"--frameID_range={frameID_range} "
                        f"--range_sc={range_sc} "
                        f"--nx_sc={nx_sc} "
                        f"--range_iq={range_iq} "
                        f"--nx_iq={nx_iq}"
                )
                print(" command : ",command)
                try:
                        #print("start_online_server_worker") 
                        subprocess.run(command, shell=True, check=True)
                        
                except subprocess.CalledProcessError:
                        print("CSR_Online_Server stops running.")

def start_generate_full_spectrum_worker(should_stop_online_server, default_path_injection_files, frameID_offset, frameID_range):
        time.sleep(1)
        while not should_stop_online_server[0]: 
                #command = f"combine_injection get_full_spec {default_path_injection_files}/injection_list.txt  {default_path_injection_files} 10"
                command = (
                        f"combine_injection get_full_spec {default_path_injection_files}/injection_list.txt "
                        f"{default_path_injection_files} 10 {frameID_offset} {frameID_range}"
                )
                try:
                        print("combine_injection get_full_spec ../data/injection/injection_list.txt /lustre/astrum/experiment_data/2024-05_E018/OnlineDataAnalysisSystem/data 20") 
                        subprocess.run(command, shell=True, check=True)
                        
                except subprocess.CalledProcessError:
                        print("combine_injection stops running.")
                time.sleep(1)

def replace_directory_name(original_path, old_dir_name, new_dir_name):
        """
        Replace a specified directory name in the original path with a new directory name.
        
        Args:
        original_path (str): The original file path that may contain the old directory name.
        old_dir_name (str): The old directory name to replace.
        new_dir_name (str): The new directory name to use.
        
        Returns:
        str: The updated file path with the new directory name.
        
        This function splits the original path into parts, checks each part for the old directory name,
        replaces it if found, and then reassembles the path parts back into a full path.
        """
        # Split the original path into components
        path_parts = original_path.split('/')
        
        # Iterate over path components and replace the old directory name with the new one
        updated_parts = [new_dir_name if part == old_dir_name else part for part in path_parts]
        
        # Reconstruct the path from the updated parts
        new_path = '/'.join(updated_parts)
        
        return new_path

def replace_directory_name_if_prefix_found(original_path, new_dir_name):
        """
        Automatically identify and replace directory names in the original path if they contain
        specific prefixes ('IQ_' or 'SC_').
        
        Args:
        original_path (str): The original file path that may contain directory names with specific prefixes.
        new_dir_name (str): The new directory name to use for replacement.
        
        Returns:
        str: The updated file path with the directory name replaced if the condition is met.
        
        The function splits the path, checks each part for the specified prefixes, and replaces the 
        directory name if one of the prefixes is found.
        """
        # Split the original path into components
        path_parts = original_path.split('/')
        
        # Iterate over path components and replace any directory name containing 'IQ_' or 'SC_'
        updated_parts = []
        for part in path_parts:
                if "IQ_" in part or "SC_" in part:
                        updated_parts.append(new_dir_name)
                else:
                        updated_parts.append(part)
                        
        # Reconstruct the path from the updated parts
        new_path = '/'.join(updated_parts)
        return new_path
                                                                        
def start_online_server(start_button_online_server,stop_button_online_server, should_stop_online_server, update_button_online_server, should_stop_update_online_server,folder_entry_analyzed_files_iq,folder_entry_analyzed_files_sc,path_to_analyzed_files_iq,path_to_analyzed_files_sc,default_path_injection_files,frameID_offset,frameID_range,range_sc,nx_sc,range_iq,nx_iq):
    #print(" start_online_server")
    should_stop_online_server[0] = False
    start_button_online_server.config(state="disabled")  # Disable the start button during syncing
    stop_button_online_server.config(state=tk.NORMAL) # Enable the stop button later when needed

    # Remove CSR_Online_Server_status.txt if it exists
    try:
            os.remove("CSR_Online_Server_status.txt")
    except FileNotFoundError:
            pass  # Ignore if the file doesn't exist
    path_analyzed_files_iq = folder_entry_analyzed_files_iq.get()
    path_analyzed_files_sc = folder_entry_analyzed_files_sc.get()
    #print("chenrj ... ", path_analyzed_files_iq,"  ",path_analyzed_files_sc)
    # Extract the last part of the paths
    new_iq_dir_name = os.path.basename(path_analyzed_files_iq)
    new_sc_dir_name = os.path.basename(path_analyzed_files_sc)
    
    path_to_analyzed_files_iq   = replace_directory_name_if_prefix_found(path_to_analyzed_files_iq,   new_iq_dir_name)
    path_to_analyzed_files_sc   = replace_directory_name_if_prefix_found(path_to_analyzed_files_sc,   new_sc_dir_name)
    default_path_injection_files = replace_directory_name_if_prefix_found(default_path_injection_files, new_iq_dir_name)
    
    thread_start_online_server = threading.Thread(target=start_online_server_worker,args=(should_stop_online_server,path_to_analyzed_files_iq, path_to_analyzed_files_sc, default_path_injection_files,frameID_offset, frameID_range, range_sc, nx_sc, range_iq, nx_iq))
    thread_start_online_server.start()
    
    thread_start_generate_full_spectrum = threading.Thread(target=start_generate_full_spectrum_worker,args=(should_stop_online_server, default_path_injection_files, frameID_offset, frameID_range))
    thread_start_generate_full_spectrum.start()
    
    
    should_stop_update_online_server[0] = True
    update_online_server(update_button_online_server,stop_button_online_server, should_stop_update_online_server)    
                        
def update_online_server_worker(should_stop_update_online_server):
    while not should_stop_update_online_server[0]:
        #print("update_online_server_worker")
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
                        
                time.sleep(10)
    
    
def stop_online_server(start_button_online_server,update_button_online_server,stop_button_online_server, should_stop_online_server,should_stop_update_online_server):
        should_stop_online_server[0] = True
        should_stop_update_online_server[0] = True
        #print(" stop_online_server")
        if should_stop_online_server[0]:
                start_button_online_server.config(state=tk.NORMAL)  # Disable the start button during syncing
                update_button_online_server.config(state=tk.NORMAL)  # Disable the start button during syncing
                stop_button_online_server.config(state="disabled") # Enable the stop button later when needed
        
                command = f"killall -9 CSR_Online_Server"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("stop CSR_Online_Server faild!")
                command = f"killall -9 combine_injection"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("stop combine_injection faild!")
                        
def start_roody_worker(should_stop_roody):
        #time.sleep(40)  
        if not should_stop_roody[0]:  
                command = f"../roody/bin/roody -H127.0.0.1:9092"
                try:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError:
                        print("roody stops running.")
        
def start_roody(start_button_roody,stop_button_roody, should_stop_roody):
    #print(" start_roody")
    should_stop_roody[0] = False
    start_button_roody.config(state="disabled")  # Disable the start button during syncing
    stop_button_roody.config(state=tk.NORMAL) # Enable the stop button later when needed
    
    thread_start_roody = threading.Thread(target=start_roody_worker,args=(should_stop_roody,))
    thread_start_roody.start()

def stop_roody(start_button_roody,stop_button_roody, should_stop_roody):
        should_stop_roody[0] = True
        #print(" stop_roody")
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
def get_listbox_item_color(file_listbox, index):
        # Retrieve the background color of the listbox item at the given index
        return file_listbox.itemcget(index, 'bg')

#def update_file_list(file_listbox,directory,analyzed_files_name="analyzed_files_iq.txt",end=".iq.tdms"):
#        # Get the current items in the file_listbox
#        existing_items  = file_listbox.get(0, tk.END)
#        existing_colors = {item: get_listbox_item_color(file_listbox, i) for i, item in enumerate(existing_items)}
#        files_in_directory = list_files_in_directory(directory,end)
#        file_listbox.delete(0, tk.END)
#        scroll_position=0
#        for file in files_in_directory:
#                file_listbox.insert(tk.END, file)
#                # If the file originally exists in the list, retain its color
#                if file in existing_colors:
#                        index = file_listbox.get(0, tk.END).index(file)  # Get the newly inserted file index
#                        set_listbox_iterm_color(file_listbox, file, existing_colors[file])
#            
#        analyzed_files=get_files(analyzed_files_name)
#        for file in files_in_directory:
#                file_fullpath=directory+"/"+file
#                if file_fullpath in analyzed_files:
#                        set_listbox_iterm_color(file_listbox, file, "green")
#        file_listbox.yview(tk.END)
def update_file_list(file_listbox, default_path_synced_files,default_path_analyzed_files, analyzed_files_name="analyzed_files_iq.txt", end=".iq.tdms"):
        # Retrieve the current items in the listbox
        existing_items = file_listbox.get(0, tk.END)
        # Create a dictionary to store the color of each item
        existing_colors = {item: get_listbox_item_color(file_listbox, i) for i, item in enumerate(existing_items)}
        
        # List files in the synced_files with the specified file extension
        files_in_synced_files = list_files_in_directory(default_path_synced_files, end)
        
        # Save the current scroll position to restore later
        scroll_position = file_listbox.yview()[0]
        
        # Identify new files that are not already in the listbox
        new_files = [file for file in files_in_synced_files if file not in existing_items]
        #print("new_files ",new_files)
        for file in new_files:
                file_listbox.insert(tk.END, file)
                # If the file was originally in the list, retain its color
                #if file in existing_colors:
                #        index = file_listbox.get(0, tk.END).index(file)  # Get the newly inserted file index
                #        set_listbox_item_color(file_listbox, file, existing_colors[file])
        
        # Mark files that have been analyzed
        a = default_path_analyzed_files + "/" + analyzed_files_name
        analyzed_files = get_files(a)
        #print("analyzed_files_name = ",a)
        #print("analyzed_files ",analyzed_files)
        for file in new_files:
                file_fullpath = os.path.join(default_path_synced_files, file)
                #print("file_fullpath ",file_fullpath)
                if file_fullpath in analyzed_files:
                        set_listbox_iterm_color(file_listbox, file, "green")
                        
        # Restore the previous scroll position
        file_listbox.yview_moveto(scroll_position)
                        

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

def load_arguments_worker(config, folder_entry_list, file_listbox_synced_files_iq, file_listbox_synced_files_sc):
        file_path = filedialog.askopenfilename(title="Load Parameter File")
        config = load_arguments(file_path)
        if file_path:
                file_listbox_synced_files_iq.delete(0,tk.END)
                file_listbox_synced_files_sc.delete(0,tk.END)
        
        for entry, arg_name in zip(folder_entry_list, config.keys()):
                entry.delete(0, tk.END)
                entry.insert(0, config[arg_name])
        # Conditionally execute update_file_list if args.default_path_synced_files_iq is not equal to 0
        if config["default_path_synced_files_iq"] != 0:
                update_file_list(file_listbox_synced_files_iq, config["default_path_synced_files_iq"], config["default_path_analyzed_files_iq"], "analyzed_files_iq.txt", ".iq.tdms")
        if config["default_path_synced_files_sc"] != 0:
                update_file_list(file_listbox_synced_files_sc, config["default_path_synced_files_sc"], config["default_path_analyzed_files_sc"],"analyzed_files_sc.txt", ".sc.tdms")
        
def save_arguments_worker(config, folder_entry_list):
        file_path = filedialog.asksaveasfilename(
                title="Save Parameter File",
                defaultextension=".toml",
                filetypes=[("TOML files", "*.toml"), ("All files", "*.*")])
        
        if file_path:
                #print(" save_parameters ", file_path)
                
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
        
def update_file_list_periodically(file_listbox_synced_files_iq, default_path_synced_files_iq, analyzed_files_iq, file_extension_iq, file_listbox_synced_files_sc, default_path_synced_files_sc, analyzed_files_sc, file_extension_sc):
        while True:
                # Add your code logic here
                #print("Running update_file_list_periodically...")
                # Call your function
                update_file_list(file_listbox_synced_files_iq, default_path_synced_files_iq, default_path_analyzed_files_iq, analyzed_files_iq, file_extension_iq)
                update_file_list(file_listbox_synced_files_sc, default_path_synced_files_sc, default_path_analyzed_files_sc, analyzed_files_sc, file_extension_sc)
                time.sleep(5)

def create_listbox_with_scrollbar(parent, width, height, grid_row, grid_column):
        """
        Creates a Listbox with a vertical scrollbar and places it in the parent widget.
        
        Parameters:
        - parent: the parent widget (e.g., root window or a frame) where the Listbox and Scrollbar are to be added.
        - width: width of the Listbox.
        - height: height of the Listbox.
        - grid_row: grid row position for the Listbox and Scrollbar.
        - grid_column: grid column position for the Listbox.

        Returns:
        - A tuple containing the Listbox and Scrollbar objects.
        """
        # Create the Listbox
        file_listbox = tk.Listbox(parent, width=width, height=height)
        file_listbox.grid(row=grid_row, column=grid_column, rowspan=9, padx=10, pady=10, sticky="w")
        
        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(parent, orient="vertical")
        scrollbar.grid(row=grid_row, column=grid_column, rowspan=9, sticky="nse")
        
        # Associate the scrollbar with the Listbox
        file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=file_listbox.yview)
        
        # Return both widgets
        return file_listbox, scrollbar

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
        window_width = 1600
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
        
        path_to_analyzed_files_iq =config["path_to_analyzed_files_iq"]
        path_to_analyzed_files_sc =config["path_to_analyzed_files_sc"]
        default_path_injection_files =config["default_path_injection_files"]
        frameID_offset =config["frameID_offset"]
        frameID_range =config["frameID_range"]
        range_sc =config["range_sc"]
        nx_sc =config["nx_sc"]
        range_iq =config["range_iq"]
        nx_iq =config["nx_iq"]
        # =config[""]
        # Create a menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # Create a "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add a "Load Parameter" option to the "File" menu
        file_menu.add_command(label="Load Parameter", command=lambda:load_arguments_worker(config,folder_entry_list, file_listbox_synced_files_iq, file_listbox_synced_files_sc))
        
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

        ## Create a Label for injection_files
        comment_label_injection_files = tk.Label(root, text="INJECTION_FILES:")
        comment_label_injection_files.grid(row=4, column=0, padx=10, pady=10, sticky="w")  # Left-aligned
        # Create an Entry widget for injection_files
        folder_entry_injection_files = tk.Entry(root,width=90)
        folder_entry_injection_files.grid(row=4, column=1, columnspan=4,padx=10, pady=10, sticky="w")  # Left-aligned
        folder_entry_injection_files.insert(0, default_path_injection_files)  # Insert the default path
        
        file_listbox_synced_files_iq,file_listbox_synced_files_iq_scrollbar = create_listbox_with_scrollbar(root, width=20, height=25, grid_row=5, grid_column=0)
        update_file_list(file_listbox_synced_files_iq,default_path_synced_files_iq,default_path_analyzed_files_iq,"analyzed_files_iq.txt",".iq.tdms")  # Update the file list in file_listbox_synced_files_iq with default path
        file_listbox_analyzed_files_iq,file_listbox_analyzed_files_iq_scrollbar = create_listbox_with_scrollbar(root, width=20, height=25, grid_row=5, grid_column=1)
        file_listbox_synced_files_sc,file_listbox_synced_files_sc_scrollbar = create_listbox_with_scrollbar(root, width=20, height=25, grid_row=5, grid_column=2)
        update_file_list(file_listbox_synced_files_sc,default_path_synced_files_sc,default_path_analyzed_files_sc,"analyzed_files_sc.txt",".sc.tdms")  # Update the file list in file_listbox_synced_files_iq with default path
        file_listbox_analyzed_files_sc,file_listbox_analyzed_files_sc_scrollbar = create_listbox_with_scrollbar(root, width=20, height=25, grid_row=5, grid_column=3)
        file_listbox_injection_files,file_listbox_injection_files_scrollbar = create_listbox_with_scrollbar(root, width=20, height=25, grid_row=5, grid_column=4)

        #thread = threading.Thread(target=update_file_list_periodically, args=(file_listbox_synced_files_iq, default_path_synced_files_iq, "analyzed_files_iq.txt", ".iq.tdms",file_listbox_synced_files_sc, default_path_synced_files_sc, "analyzed_files_sc.txt", ".sc.tdms"))        
        #thread.start()
        ## Create a "Browse" button for folder selection
        browse_button_synced_files_iq = tk.Button(root, text="Browse", command=lambda: browse_folder_and_update_list_filebox(folder_entry_synced_files_iq,default_path_synced_files_iq,default_path_analyzed_files_iq,file_listbox_synced_files_iq,"analyzed_files_iq.txt",".iq.tdms"))
        browse_button_synced_files_iq.grid(row=0, column=5, padx=10, pady=10, sticky="w")  # Left-aligned
        
        ## Create a "Browse" button for folder selection
        browse_button_analyzed_files_iq = tk.Button(root, text="Browse", command=lambda: browse_folder(folder_entry_analyzed_files_iq,default_path_analyzed_files_iq))
        browse_button_analyzed_files_iq.grid(row=1, column=5, padx=10, pady=10, sticky="w")  # Left-aligned
        
        # Create a "Browse" button for folder selection
        browse_button_synced_files_sc = tk.Button(root, text="Browse", command=lambda: browse_folder_and_update_list_filebox(folder_entry_synced_files_sc,default_path_synced_files_sc,default_path_analyzed_files_sc,file_listbox_synced_files_sc,"analyzed_files_sc.txt",".sc.tdms"))
        browse_button_synced_files_sc.grid(row=2, column=5, padx=10, pady=10, sticky="w")  # Left-aligned
    
        # Create a "Browse" button for folder selection
        browse_button_analyzed_files_sc = tk.Button(root, text="Browse", command=lambda: browse_folder(folder_entry_analyzed_files_sc,default_path_analyzed_files_sc))
        browse_button_analyzed_files_sc.grid(row=3, column=5, padx=10, pady=10, sticky="w")  # Left-aligned

        # Create a "Browse" button for folder selection
        browse_button_injection_files = tk.Button(root, text="Browse", command=lambda: browse_folder(folder_entry_injection_files,default_path_injection_files))
        browse_button_injection_files.grid(row=4, column=5, padx=10, pady=10, sticky="w")  # Left-aligned
    
        
        ### Create the "Start" button
        unanalyzed_files_iq=[]
        thread_list_iq=[]
        
        object_list=[]
        
        start_button_analysis = ttk.Button(root, text="Start analysis", command=lambda:analyze_data(folder_entry_dic,file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files_iq,thread_list_iq))
        start_button_analysis.configure(style="TButton")
        start_button_analysis.grid(row=1, column=7, padx=5, pady=10, sticky="w")
                
        ### Create the "Stop" button
        stop_button = tk.Button(root, text="Stop analysis", command=lambda:stop_analyze(folder_entry_dic, file_listbox_dic, button_dic, should_stop_analyze, unanalyzed_files_iq, thread_list_iq))
        stop_button.grid(row=1, column=8, padx=5, pady=10, sticky="w")  # Left-aligned
    
        start_button_online_server = tk.Button(root, text="Start online server", command=lambda:start_online_server(start_button_online_server,stop_button_online_server,should_stop_online_server, update_button_online_server,should_stop_update_online_server,folder_entry_analyzed_files_iq,folder_entry_analyzed_files_sc,path_to_analyzed_files_iq,path_to_analyzed_files_sc,default_path_injection_files,frameID_offset,frameID_range,range_sc,nx_sc,range_iq,nx_iq))
        start_button_online_server.grid(row=1, column=9, padx=5, pady=10, sticky="w")  # Left-aligned
        
        #update_button_online_server = tk.Button(root, text="Update online server(60)", command=lambda:update_online_server(update_button_online_server,stop_button_online_server,should_stop_update_online_server))
        #update_button_online_server.grid(row=1, column=8, padx=5, pady=10, sticky="w")  # Left-aligned
               
        stop_button_online_server = tk.Button(root, text="Stop online server", command=lambda:stop_online_server(start_button_online_server,update_button_online_server,stop_button_online_server,should_stop_online_server,should_stop_update_online_server))
        stop_button_online_server.grid(row=1, column=10, padx=5, pady=10, sticky="w")  # Left-aligned
        
        start_button_roody = tk.Button(root, text="Start roody", command=lambda:start_roody(start_button_roody,stop_button_roody,should_stop_roody))
        start_button_roody.grid(row=2, column=9, padx=5, pady=10, sticky="w")  # Left-aligned

        stop_button_roody = tk.Button(root, text="Stop roody", command=lambda:stop_roody(start_button_roody,stop_button_roody,should_stop_roody))
        stop_button_roody.grid(row=2, column=10, padx=5, pady=10, sticky="w")  # Left-aligned
    
        ## Create the "Reanalyze" button iq
        reanalyze_button_iq = tk.Button(root, text="Re-analyze(IQ)", command=lambda:reanalyze_sync_iq(file_listbox_synced_files_iq,default_path_synced_files_iq,file_listbox_synced_files_sc,default_path_synced_files_sc))
        reanalyze_button_iq.grid(row=14, column=0, padx=5, pady=10, sticky="w")  # Left-aligned
        
        ## Create the "Reanalyze" button sc
        reanalyze_button_sc = tk.Button(root, text="Re-analyze(SC)", command=lambda:reanalyze_sync_sc(file_listbox_synced_files_iq,default_path_synced_files_iq,file_listbox_synced_files_sc,default_path_synced_files_sc))
        reanalyze_button_sc.grid(row=14, column=2, padx=5, pady=10, sticky="w")  # Left-aligned
        
        comment_label_num_threads,  folder_entry_num_threads  = create_folder_entry(root, num_threads,  "NUM_THREADS:",   3, 7)
        comment_label_FramesStep,   folder_entry_FramesStep   = create_folder_entry(root, FramesStep,   "FramesStep:",    4, 7)
        comment_label_WeightType,   folder_entry_WeightType   = create_folder_entry(root, WeightType,   "WeightType:",    5, 7)
        comment_label_PlotOption,   folder_entry_PlotOption   = create_folder_entry(root, PlotOption,   "PlotOption:",    6, 7)
        comment_label_FramesPerPlot,folder_entry_FramesPerPlot= create_folder_entry(root, FramesPerPlot,"FramesPerPlot:", 7, 7)
        comment_label_FFTFreqLow,   folder_entry_FFTFreqLow   = create_folder_entry(root, FFTFreqLow,   "FFTFreqLow:",    8, 7)
        comment_label_FFTFreqSpan,  folder_entry_FFTFreqSpan  = create_folder_entry(root, FFTFreqSpan,  "FFTFreqSpan:",   9, 7)
        comment_label_FFTFreqBin,   folder_entry_FFTFreqBin   = create_folder_entry(root, FFTFreqBin,   "FFTFreqBin:",   10, 7)
        comment_label_FFTNrOfFrames,folder_entry_FFTNrOfFrames= create_folder_entry(root, FFTNrOfFrames,"FFTNrOfFrames:",11, 7)
        comment_label_FFTFrameBin,  folder_entry_FFTFrameBin  = create_folder_entry(root, FFTFrameBin,  "FFTFrameBin:",  12, 7)
        comment_label_WorkMode,     folder_entry_WorkMode     = create_folder_entry(root, WorkMode,     "WorkMode:",     13, 7)
        
        comment_label_frameID_offset,folder_entry_frameID_offset= create_folder_entry(root, frameID_offset,"frameID_offset:",3, 9)
        comment_label_frameID_range, folder_entry_frameID_range = create_folder_entry(root, frameID_range, "frameID_range:", 4, 9)
        comment_label_range_sc,      folder_entry_range_sc      = create_folder_entry(root, range_sc,      "range_sc:",      5, 9)
        comment_label_nx_sc,         folder_entry_nx_sc         = create_folder_entry(root, nx_sc,         "nx_sc:",         6, 9)
        comment_label_range_iq,      folder_entry_range_iq      = create_folder_entry(root, range_iq,      "range_iq:",      7, 9)
        comment_label_nx_iq,         folder_entry_nx_iq         = create_folder_entry(root, nx_iq,         "nx_iq:",         8, 9)
    
        folder_entry_dic = {
                "synced_files_iq": folder_entry_synced_files_iq,
                "analyzed_files_iq": folder_entry_analyzed_files_iq,
                "synced_files_sc": folder_entry_synced_files_sc,
                "analyzed_files_sc": folder_entry_analyzed_files_sc,
                "injection_files": folder_entry_injection_files,
                "num_threads": folder_entry_num_threads,
                "FramesStep": folder_entry_FramesStep,
                "WeightType": folder_entry_WeightType,
                "PlotOption": folder_entry_PlotOption,
                "FramesPerPlot": folder_entry_FramesPerPlot,
                "FFTFreqLow": folder_entry_FFTFreqLow,
                "FFTFreqSpan": folder_entry_FFTFreqSpan,
                "FFTFreqBin": folder_entry_FFTFreqBin,
                "FFTNrOfFrames": folder_entry_FFTNrOfFrames,
                "FFTFrameBin": folder_entry_FFTFrameBin,
                "WorkMode": folder_entry_WorkMode,
                "frameID_offset": folder_entry_frameID_offset,
                "frameID_range": folder_entry_frameID_range,
                "range_sc": folder_entry_range_sc,
                "nx_sc": folder_entry_nx_sc,
                "range_iq": folder_entry_range_iq,
                "nx_iq": folder_entry_nx_iq
        }
        
        file_listbox_dic = {
                "synced_files_iq":  file_listbox_synced_files_iq,
                "analyzed_files_iq":file_listbox_analyzed_files_iq,
                "synced_files_sc":  file_listbox_synced_files_sc,
                "analyzed_files_sc":file_listbox_analyzed_files_sc,
                "injection_files":  file_listbox_injection_files
        }
        button_dic = {
                "browse_button_synced_files_iq": browse_button_synced_files_iq,
                "browse_button_analyzed_files_iq": browse_button_analyzed_files_iq,
                "browse_button_synced_files_sc": browse_button_synced_files_sc,
                "browse_button_analyzed_files_sc": browse_button_analyzed_files_sc,
                "browse_button_injection_files": browse_button_injection_files,
                "start_button_analysis": start_button_analysis,
                "stop_button": stop_button,
                "start_button_online_server": start_button_online_server,
                "stop_button_online_server": stop_button_online_server,
                "start_button_roody": start_button_roody,
                "stop_button_roody": stop_button_roody,
                "reanalyze_button_iq": reanalyze_button_iq,
                "reanalyze_button_sc": reanalyze_button_sc
        }
        # Run the main loop
        root.mainloop()

if __name__ == "__main__":
    main()
