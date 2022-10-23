import dearpygui.dearpygui as dpg
import app

def init_gui():
    x1 = 380
    y1 = 450
    x2 = 370
    y2 = 445
    dpg.create_context()
    dpg.create_viewport(title='SaveEnergy', width=x1, height=y1, min_width=x1, min_height=y1)
    dpg.setup_dearpygui()
    
    with dpg.window(tag='w_main', width=x2, height=y2, no_move=True, no_title_bar=True):
        dpg.add_input_int(label='PID', tag='i_process_id', enabled=False, readonly=True)
        dpg.add_input_int(label='Timer (sec)', tag='i_time_to_finish')
        
        with dpg.group(horizontal=True):
            dpg.add_button(label='5 min', tag='time_5')
            dpg.add_button(label='30 min', tag='time_30')
            dpg.add_button(label='60 min', tag='time_60')
            dpg.add_button(label='3 h', tag='time_3')
        with dpg.group(horizontal=True):
            dpg.add_text('Not set yet!', tag='time_left_number')
            dpg.add_text('Time Left (sec)', tag='time_left')
        dpg.add_button(label='Refresh List', tag='b_process_list')
        dpg.add_listbox(app.get_processes(), tag='l_process_list', width=x2-15, num_items=8)
        dpg.add_button(label='KILL!', tag='b_process_kill', width=x2-15, height=40)
        dpg.add_button(label='Shutdown', tag='b_shutdown', width=x2-15, height=40)
    dpg.show_viewport()

def make_interactive():
    try:
        while True:
            dpg.set_value('i_process_id', get_pid_from_list())
            
            # Update process list. Could make it dynamic.
            if dpg.is_item_clicked('b_process_list'):
                dpg.configure_item('l_process_list', items=app.get_processes())
            
            if dpg.is_item_clicked('time_5'):
                dpg.set_value('i_time_to_finish', 300)
                dpg.set_value('time_left_number', '300')
            elif dpg.is_item_clicked('time_30'):
                dpg.set_value('i_time_to_finish', 1800)
                dpg.set_value('time_left_number', '1800')
            elif dpg.is_item_clicked('time_60'):
                dpg.set_value('i_time_to_finish', 3600)
                dpg.set_value('time_left_number', '3600')
            elif dpg.is_item_clicked('time_3'):
                dpg.set_value('i_time_to_finish', 10800)
                dpg.set_value('time_left_number', '10800')
            
            dpg.set_item_width('w_main', dpg.get_viewport_width()-15)
            dpg.set_item_height('w_main', dpg.get_viewport_height())
            app.time.sleep(0.001)
    
    except Exception as err:
        print(err)

def get_pid_from_list():
    try:
        c = dpg.get_value('l_process_list')
        a = c.split(',')
        f = a[0].removeprefix('[')
        
        return int(f)
    except Exception as err:
        pass