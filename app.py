###              ###
### RUN AS ADMIN ###
###              ###
import threading
import gui


def main():
    wnd.create()
    threading.Thread(target=wnd.update, name='make_interactive', daemon=True).start()
    wnd.run()
    
if __name__ == '__main__':
    wnd = gui.Window()
    main()