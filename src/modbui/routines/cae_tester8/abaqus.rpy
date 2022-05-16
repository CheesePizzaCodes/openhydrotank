# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-19.49.31 163176
# Run by User on Thu May 12 14:47:40 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=58.3854179382324, 
    height=166.638885498047)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
import sys
sys.path.append(r'e:\ABQ2020FILES\Plugins\2020\WoundSimAbaqusPlugin\translate')
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
cliCommand("""import scipy""")
cliCommand("""scipy""")
#: <module 'scipy' from 'E:\Program Files\ABAQUS2020\win_b64\tools\SMApy\python2.7\lib\site-packages\scipy\__init__.pyc'>
cliCommand("""scipy.integrate""")
#* AttributeError: 'module' object has no attribute 'integrate'
cliCommand("""scipy.__file__""")
#: 'E:\\Program Files\\ABAQUS2020\\win_b64\\tools\\SMApy\\python2.7\\lib\\site-packages\\scipy\\__init__.pyc'
cliCommand("""scipy.__version__""")
#: '1.2.0'
cliCommand("""scipy.integrate""")
#* AttributeError: 'module' object has no attribute 'integrate'
cliCommand("""import numpy""")
cliCommand("""numpy.trapz""")
#: <function trapz at 0x000002395AF11C18>
cliCommand("""import scipy.integrate""")
cliCommand("""scipy.integrate""")
#: <module 'scipy.integrate' from 'E:\Program Files\ABAQUS2020\win_b64\tools\SMApy\python2.7\lib\site-packages\scipy\integrate\__init__.py'>
cliCommand("""from scipz.integrate import quad""")
#* ImportError: No module named scipz.integrate
cliCommand("""from scipy.integrate import quad""")
cliCommand("""quad""")
#: <function quad at 0x00000239614F1588>
cliCommand("""quad(lambda x: x ** 2, 2, 3)""")
#: (6.33333333333333, 7.03141248929266e-14)
cliCommand("""a + quad(lambda x: x ** 2, 2, 3)""")
#* NameError: name 'a' is not defined
cliCommand("""a = quad(lambda x: x ** 2, 2, 3)""")
cliCommand("""a""")
#: (6.33333333333333, 7.03141248929266e-14)
cliCommand("""b, a = quad(lambda x: x ** 2, 2, 3)""")
cliCommand("""b""")
#: 6.33333333333333
cliCommand("""a""")
#: 7.03141248929266e-14
cliCommand("""__version__""")
#* NameError: name '__version__' is not defined
cliCommand("""import sys""")
cliCommand("""sys.__version__""")
#* AttributeError: 'module' object has no attribute '__version__'
cliCommand("""sys.__file__""")
#* AttributeError: 'module' object has no attribute '__file__'
cliCommand("""sys.__version__()""")
#* AttributeError: 'module' object has no attribute '__version__'
cliCommand("""del scipy""")
cliCommand("""del scipy.integrate""")
#* NameError: name 'scipy' is not defined
cliCommand("""scipy.integrate""")
#* NameError: name 'scipy' is not defined
cliCommand("""quad""")
#: <function quad at 0x00000239614F1588>
cliCommand("""del quad""")
cliCommand("""scipy""")
#* NameError: name 'scipy' is not defined
cliCommand("""quad""")
#* NameError: name 'quad' is not defined
cliCommand("""from scipy.integrate import quad""")
cliCommand("""quad""")
#: <function quad at 0x00000239614F1588>
cliCommand("""np""")
#* NameError: name 'np' is not defined
cliCommand("""import numpy as np""")
cliCommand("""np.asarray""")
#: <function asarray at 0x000002395A5D1668>
cliCommand("""np.array""")
#: <built-in function array>
cliCommand("""r = [1, 2, 3]""")
cliCommand("""r = np.asarray(r)""")
cliCommand("""r""")
#: array([1, 2, 3], 'l')
cliCommand("""t = (m_R * n_R / pi) * (np.arccos(r_0 / r) - np.arccos((r_0 + b) / r)) * t_P""")
#* NameError: name 'm_R' is not defined
cliCommand("""t = (np.arccos(10 / r)
)""")
#* FloatingPointError: invalid value encountered in arccos
cliCommand("""t = (np.arccos(10 / r))""")
#* FloatingPointError: invalid value encountered in arccos
cliCommand("""t = (np.arccos(10 / 5))""")
#* FloatingPointError: invalid value encountered in arccos
cliCommand("""t = (np.arccos(1 / r))""")
cliCommand("""t""")
#: array([0.0, 1.5707963267949, 1.5707963267949], 'd')
cliCommand("""np.poly1d""")
#: <class 'numpy.lib.polynomial.poly1d'>
cliCommand("""np.poly1d([1, 2, 3])""")
#: poly1d([1, 2, 3]ØY9, 'l')
cliCommand("""np.poly1d([1, 2, 3])([1, 2])""")
#: array([6, 11]1d([1, 2, 3])([1, 2])
#: , 'l')
cliCommand("""pr = np.poly1d([1, 2, 3])""")
cliCommand("""pr(1)""")
#: 6
cliCommand("""pr([1, 2, 3, 4])""")
#: array([6, 11, 18, 27], 'l')
cliCommand("""np.nan_to_num""")
#: <function nan_to_num at 0x000002395AEEBBA8>
