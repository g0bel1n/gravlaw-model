import os.path
import urllib
import zipfile

import numpy as np
from typing import Tuple


def gravity_law(p_i: float, p_j: float, r: float) -> float:
    """
    :param p_i: Population of the city i
    :param p_j: Population of the city i
    :param r: Distance beetween city i and  j
    :return: the flow of traffic estimated according to a Gravity law model.
    Actually, the "true" result is proportional to this output
    """
    return p_i * p_j / r ** 2


def extr(mat: np.ndarray) -> Tuple[float, float]:
    """
    Iterates upon the array once to output max and min
    :param mat: matrix containing the distance between cities.
    Must be symmetric and each value  >0
    :return: the maximum and minimum value of the array
    """
    n = len(mat)
    maxi, mini = mat[0][1], mat[0][1]
    for i in range(n):
        for j in range(i + 1, n):
            if mat[i][j] > maxi:
                maxi = mat[i][j]
            elif mat[i][j] < mini:
                mini = mat[i][j]
    return maxi, mini


def extract(obj):
    """
    :param obj: object of the extraction. Is either a country name or "tmja".
    :return: the path towards the file asked
    """
    url = None
    if obj == "tmja":
        extract_dir = "../tmja2018"
        filename = "../tmja2018"
        if not os.path.isdir(extract_dir):
            url = "https://www.data.gouv.fr/fr/datasets/r/cf09b2c2-2500-4c1f-941f-83c9f17b95d8"
    else:
        extract_dir = "cities_{}".format(obj)
        filename = "geonames-all-cities-with-a-population-1000"
        if not os.path.isdir(extract_dir):
            url = 'https://data.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000@public' \
                  '/download/?format=shp&disjunctive.cou_name_en=true&refine.cou_name_en=' + obj + \
                  '&timezone=Europe/Berlin&lang=fr '

    if url is not None:
        zip_path, _ = urllib.request.urlretrieve(url)
        with zipfile.ZipFile(zip_path, "r") as f:
            f.extractall(extract_dir)
    return extract_dir + "/" + filename + ".shp"
