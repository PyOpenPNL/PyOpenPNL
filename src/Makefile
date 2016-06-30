#!/bin/bash
#
#	***************************************************
#		This makefile is for testing only
#			Please use setup.py for build and install!
#	***************************************************
#
#OBJS=../../prefix/lib/libpnl.so  ../../prefix/lib/libhigh.so ../../prefix/lib/cxcore.so -lpython2.7
OBJS=-lpnl -lhigh -lcxcore -lpython2.7
INCLUDES=-I/usr/local/include/ -I/usr/local/include/opencx/ -I/usr/include/python2.7/ -I$(shell python -c "import numpy; print numpy.get_include()")

all: openpnl.i
	swig -builtin -c++ $(INCLUDES) -python openpnl.i
	g++ -Wno-vla -fPIC -c openpnl_wrap.cxx $(INCLUDES) -fpermissive -D_GLIBCXX_USE_CXX11_ABI=0
	g++ -shared openpnl_wrap.o $(OBJS) -o _openpnl.so -fpermissive -D_GLIBCXX_USE_CXX11_ABI=0

test:
	python -c 'import openpnl'

clean:
	rm -f _openpnl.so openpnl_wrap.cxx openpnl.py openpnl.pyc openpnl_wrap.o

qa:
	python qa*.py
