# encoding: utf-8
from fabric.api import local
from os.path import join, dirname

FAB_PATH = dirname(__file__)
DEV_REQUIEREMENTS_FILE = join(FAB_PATH, 'requirements/develop.txt')

def freeze():
    '''Freezar los requerimientos del virtualenv'''
    with open(DEV_REQUIEREMENTS_FILE, 'wb') as f:    
        reqs = local('pip freeze', True)
        f.write(reqs)
    print "Requirements written to %s" % DEV_REQUIEREMENTS_FILE
        

def docs():
	'''Muestra la documentación'''
	local('restview README.rst')