#!/bin/bash
#
#	***************************************************
#		This makefile is for testing only
#			Please use setup.py for build and install!
#	***************************************************
#
#OBJS=../../prefix/lib/libpnl.so  ../../prefix/lib/libhigh.so ../../prefix/lib/cxcore.so -lpython2.7
OBJS=-lpnl -lhigh -lcxcore -lpython2.7
INCLUDES=-I/usr/local/include/ -I/usr/local/include/opencx/ -I/usr/include/python2.7/

all: openpnl.i
	swig -builtin -c++ $(INCLUDES) -python openpnl.i
	g++ -Wno-vla -fPIC -c openpnl_wrap.cxx $(INCLUDES)
	g++ -shared openpnl_wrap.o $(OBJS) -o _openpnl.so

test:
	python -c 'import openpnl'

clean:
	rm -f _openpnl.so openpnl_wrap.cxx openpnl.py openpnl.pyc openpnl_wrap.o

qa:
	python qa*.py
