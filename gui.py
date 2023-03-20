import dearpygui.dearpygui as dpg
import threading
import psutil
import signal
import time
import os

class Window():
    """Manage visual interface"""

    def __init__(self) -> None:
        """
        Window initialization
        """
        print('Window initialization started.')
        self.process_list = []

    def create(self) -> None:
        """
        Creates window context.
        """
        dpg.create_context()
        with dpg.window(
            label='Window',
            width=400,
            height=500,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            tag='w_main'):

            with dpg.tab_bar(label="Menu"):
                with dpg.tab(label="Main"):
                    dpg.add_button(label='Refresh List',
                                width=100,
                                height=20,
                                tag='b_refresh',
                                callback=lambda: dpg.configure_item(item='l_process_list',
                                                                    items=self.get_processes()))
                    with dpg.group(horizontal=True):
                        dpg.add_listbox(items=self.get_processes(),
                                        num_items=10,
                                        width=200,
                                        tag='l_process_list')
                        with dpg.group(horizontal=False):
                            dpg.add_button(label='Kill Process',
                                        tag='b_kill',
                                        callback=self.kill_process)

                            dpg.add_radio_button(items=['None' ,'+ Shutdown', '+ Hibernate'], default_value='None', tag='r_options')

                    dpg.add_separator()
                    dpg.add_input_int(label='Time To Wait',
                                      tag='i_wait_time')

                    with dpg.group(horizontal=True):
                        dpg.add_text('ETA:')
                        dpg.add_text('0',
                                    tag='t_timer')

    def update(self) -> None:
        """
        Keeps GUI updated.
        """
        while True:
            # Resizable
            vp_width = dpg.get_viewport_width()
            vp_height = dpg.get_viewport_height()
            dpg.configure_item(item='w_main', width=vp_width - 5)
            dpg.configure_item(item='w_main', height=vp_height - 5)
            
            time.sleep(0.001)

    def run(self) -> None:
        """
        Execute/Start window thread.
        """
        self.custom_themes()
        dpg.create_viewport(
            title=f'Save Energy v1.1',
            height=500,
            width=400,
            resizable=True,
            vsync=True)

        dpg.bind_theme('base_theme')
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

    def custom_themes(self) -> None:
        dpg.add_theme(tag='base_theme')

        with dpg.theme_component(parent='base_theme'):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 7)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 13)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,(0, 170, 50, 130))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,(0, 170, 50, 130))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(0, 170, 50, 130))

    def destroy(self) -> None:
        """
        Destroys window context.
        """
        dpg.destroy_context()

    def get_processes(self):
        try:
            self.process_list.clear()
            # Iterating through all the running processes
            for process in list(psutil.process_iter()):
                self.process_list.append([process.pid, process.name()])
            return self.process_list
        except Exception as err:
            print(err)

    def get_pid_from_list(self):
        try:
            data = dpg.get_value('l_process_list')
            data = data.split(',')
            return int(data[0].removeprefix('['))
        except Exception as err:
            print('Failed to parse PID')
            
    def kill_process(self):
        time_elapsed = 0
        pid = self.get_pid_from_list()
        total_wait_time = dpg.get_value('i_wait_time')
        add_option = dpg.get_value('r_additional')
        
        while True:
            time_elapsed += 1
            time_left = total_wait_time - time_elapsed
            dpg.set_value('t_timer', time_left)

            if time_left == 0:
                os.kill(pid, signal.SIGTERM)
                if add_option == '+ Shutdown':
                    os.system('shutdown /s /f /t 0')
                    break
                elif add_option == '+ Hibernate':
                    os.system('shutdown /h')
                    break
                else:
                    pass

                dpg.configure_item('l_process_list', items=self.get_processes())
                return
            time.sleep(1)