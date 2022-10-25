###              ###
### RUN AS ADMIN ###
###              ###
import psutil, os, signal, time, threading
import gui

process_list = []

def get_processes():
    try:
        process_list.clear()
        # Iterating through all the running processes
        for process in list(psutil.process_iter()):
            process_list.append([process.pid, process.name()])
        return process_list
    except Exception as err:
        print(err)

def kill_process():
    time_elapsed = 0
    
    while True:
        time_elapsed += 1
        time_left = gui.dpg.get_value('i_time_to_finish') - time_elapsed
        gui.dpg.set_value('time_left_number', time_left)
        
        if time_elapsed >= gui.dpg.get_value('i_time_to_finish'):
            # Kill process by PID
            os.kill(gui.dpg.get_value('i_process_id'), signal.SIGTERM)
            gui.dpg.configure_item('l_process_list', items=get_processes())
            return True
        time.sleep(0)

def shutdown():
    time_elapsed = 0
    
    while True:
        time_elapsed += 1
        time_left = gui.dpg.get_value('i_time_to_finish') - time_elapsed
        gui.dpg.set_value('time_left_number', time_left)
        
        if time_elapsed >= gui.dpg.get_value('i_time_to_finish'):
            os.system("shutdown /s")
            os._exit(0)
        time.sleep(1)
    
def gui_callback():
    while True:
        if gui.dpg.is_item_clicked('b_process_kill'):
            kill_process()
        elif gui.dpg.is_item_clicked('b_shutdown'):
            shutdown()
        time.sleep(0.01)

def main():
    gui.init_gui()
    threading.Thread(target=gui_callback, name='gui_callback', daemon=True).start()
    threading.Thread(target=gui.make_interactive, name='make_interactive', daemon=True).start()
    
    gui.dpg.start_dearpygui()
    
if __name__ == '__main__':
    main()