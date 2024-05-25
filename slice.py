import time
import subprocess
import os
import sys
import pyinotify
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

slicer_exec_path = "/slic3r/slic3r-dist/prusa-slicer"
slicer_paramas = "--merge --export-gcode"
slicer_configs_path = "/configs/"

def on_created(event):
    print(f"{event.src_path} has been created")
    full_path = event.src_path
    dirname = os.path.dirname(full_path)
    proj_dirname = os.path.basename(dirname)
    filename = os.path.basename(full_path)
    filename_without_ext = os.path.splitext(os.path.basename(full_path))[0]
    ext = os.path.splitext(os.path.basename(full_path))[1]

    print(f"full_path: {full_path}")
    print(f"dirname: {dirname}")
    print(f"proj_dirname: {proj_dirname}")
    print(f"filename: {filename}")
    print(f"filename_without_ext: {filename_without_ext}")
    print(f"ext: {ext}")

    config_file = f"{slicer_configs_path}{filename_without_ext}.ini"
    if not os.path.exists(config_file):
        print(f"config file not found {config_file}")
        return

    files_in_folder = os.listdir(dirname)
    stl_files_to_slice = []
    for stl_file in files_in_folder:
        full_stl_path = os.path.join(dirname, stl_file)
        if (os.path.isfile(full_stl_path) and stl_file.endswith(".stl")):
            print(f"found: {full_stl_path}")
            stl_files_to_slice.append(f"\"{full_stl_path}\"")

    print(f"need to slice {len(stl_files_to_slice)} files")
    stls_param = " ".join(stl_files_to_slice)

    output_file = f"{dirname}/{proj_dirname}_{filename_without_ext}.gcode"

    if os.path.exists(output_file):
        print("output already exists")
        return

    slice_command = f"{slicer_exec_path} {slicer_paramas} --load {config_file} --output \"{output_file}\" {stls_param}"
    print(f"slice command: {slice_command}")
    print("slicing...")
    ret = subprocess.call(slice_command, shell=True)
    print("ret: %d" % ret)
    if ret == 0:
        print("success.")
    else:
        print("error slicing.")

def Watch(path):
    print("Watching for *.slice in %s" % path)

    patterns = ["*.slice"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()

if __name__ == '__main__':
    try:
        path = "/prints"
    except IndexError:
        print ("error")
    else:
        print("docker-prusaslicer v0.1 by vk")
        print("Watching: %s" % path)
        Watch(path)