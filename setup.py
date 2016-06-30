from distutils.core import setup, Extension
import numpy

swig_inc = [
    "/usr/local/include/",
    "/usr/local/include/opencx/",
    "/usr/include/",
    "/usr/include/opencx/",
    numpy.get_include()
    ]
libdir_search = [
    "/usr/lib",
    "/usr/local/lib/"
    ]
swig_inc_flags = map(lambda x: "-I%s"%(x), swig_inc)

openpnl_module = Extension('openpnl._openpnl',
                sources=['src/openpnl.i'],
                swig_opts=['-builtin', '-c++'] + swig_inc_flags,
                include_dirs=swig_inc,
                runtime_library_dirs=libdir_search,
                libraries=["pnl","high","cxcore"],
                extra_compile_args=['-Wno-write-strings','-Wno-maybe-uninitialized','-Wno-cpp','-fpermissive'])

setup(  name            = 'openpnl',
        version         = '0.1',
        author          = 'PyOpenPNL',
        author_email    = 'contact@inferred.info',
        description     = '',
        license         = 'GPLv3',
        url             = '',
        platforms       = ['x86_64'],
        ext_modules     = [openpnl_module],
        py_modules      = ["src/openpnl"],
        packages        = ['openpnl'],
        package_dir     = {'openpnl': 'src'},
        package_data    = {'openpnl': ['data/*.dat']} )
