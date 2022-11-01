from pynput import keyboard, mouse
from pynput.mouse import *
from pynput.keyboard import *
from win32api import GetCurrentProcess,InitiateSystemShutdown
from win32security import LookupPrivilegeValue,AdjustTokenPrivileges,OpenProcessToken
from win32con import TOKEN_ALL_ACCESS,SE_SHUTDOWN_NAME,SE_PRIVILEGE_ENABLED
import ctypes

class SystemSettings:
    def __init__(self,changestatus):
        self.keyboard = keyboard.Listener()
        self.mouse = mouse.Listener()
        self.escpressed = False
        self.ypressed = False
        self.changestatus = changestatus
        pstoken = OpenProcessToken(GetCurrentProcess(),TOKEN_ALL_ACCESS)
        LUID = LookupPrivilegeValue(None,SE_SHUTDOWN_NAME)
        AdjustTokenPrivileges(pstoken,0,[(LUID,SE_PRIVILEGE_ENABLED)])

    def startKeyboard(self,status):
        self.keyboard = keyboard.Listener(on_press=self.on_press,on_release=self.on_release,suppress=status)
        self.keyboard.start()

    def startMouse(self,status):
        self.mouse = mouse.Listener(suppress=status)
        self.mouse.start()

    def stopKeyboard(self):
        self.keyboard.stop()

    def stopMouse(self):
        self.mouse.stop()

    def on_press(self, key):
        if key == Key.esc:
            self.escpressed = True

        if key == KeyCode.from_char('y'):
            self.ypressed = True

        if self.ypressed and self.escpressed:
            self.changestatus(None,"checked",None,"checked")
            self.escpressed = False
            self.ypressed = False
            self.stopKeyboard()
            self.stopMouse()

    def on_release(self, key):
        if key == Key.esc:
            self.escpressed = False

        if key == KeyCode.from_char('y'):
            self.ypressed = False

    def SystemSleep(self):
        ctypes.windll.PowrProf.SetSuspendState(False,True,False)

    def SystemHibernate(self):
        ctypes.windll.PowrProf.SetSuspendState(True,True,False)

    def SystemShutdown(self):
        InitiateSystemShutdown(None,None,5,False,False)

    def SystemReboot(self):
        InitiateSystemShutdown(None,None,5,False,True)

    def SystemAwake(self,status):
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        ES_DISPLAY_REQUIRED = 0x00000002
        ES_AWAYMODE_REQUIRED = 0x00000040
        if status:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS|ES_SYSTEM_REQUIRED|ES_DISPLAY_REQUIRED)
            print("SystemAwake: ON")
        else:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            print("SystemAwake: OFF")
