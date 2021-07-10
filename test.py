import os.path

from utilitaries.utils import extr, extract, gravity_law

def test_extr():
    liste = [[0,1,2,3,1,9,100,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    assert extr(liste) == (100,0)

def test_extract():
    assert os.path.isdir("tmja2018")
    assert os.path.isdir("cities_France")

def test_gravity_law():

    assert gravity_law(2,2,2) == 1