from distutils.core import setup
import py2exe

options = {"py2exe": {'dist_dir': "../dist"},
           'build': {'build_base': '../build'}}
           
setup(windows=[{'script': 'CoordXY.py',
                "icon_resources": [(1, "CoordXY.ico")]
                }],options=options)

