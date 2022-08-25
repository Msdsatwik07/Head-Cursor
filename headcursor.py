import serial
import mouse as ms
from pymouse import PyMouse
import pyautogui as pm
from scipy.interpolate import interp1d

serialPort = serial.Serial(port="COM5", baudrate=9600, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)

serialString = ""  # Used to hold data coming over UART
m = PyMouse()
xscr, yscr = pm.size()
ms.move(xscr / 2, yscr / 2)
x = 0.0
y = 0.0


while 1:
    if serialPort.in_waiting > 0:
        serialString = serialPort.readline()
        try:
            serialString = serialString.decode('Ascii')
        except UnicodeDecodeError:
            pass
        serialString = serialString.split(",")
        for i in range(0, len(serialString)):
            try:
                serialString[i] = float(serialString[i])
            except ValueError:
                pass

        try:
            x = 0.99*x + 0.01*serialString[0]
            y = 0.99*y + 0.01*serialString[1]
        except IndexError:
            pass
        except TypeError:
            pass

        #try:
        m = interp1d([-50, 50], [5, xscr-10])
        #except ValueError:
         #   pass

        #try:
        n = interp1d([-10, 10], [5, yscr-10])
        #except ValueError:
        #    pass

        #try:
        print(int(m(x)), int(n(y)))
        #except ValueError:
        #    pass

        try:
            ms.move(m(x), n(y))
        except ValueError:
            pass