from distutils.core import setup
import py2exe

options = {"py2exe": {"packages": ['wx.lib.floatcanvas.NavCanvas','wx.lib.floatcanvas.FloatCanvas'],"dist_dir": "../dist"},
           'build': {'build_base': '../build'}}
           
setup(windows=[{'script': 'CoordXY.py',
                "icon_resources": [(1, "CoordXY.ico")]
                }],options=options)

