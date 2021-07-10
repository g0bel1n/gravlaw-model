import os.path
import urllib
import zipfile


def gravity_law(p_i, p_j, r):
    return p_i * p_j / r ** 2


# mat is symmetric
def extr(mat, nb_cntry=30):
    if len(mat) < nb_cntry:
        nb_cntry = len(mat)
    maxi, mini = mat[0][1], mat[0][1]
    for i in range(nb_cntry):
        for j in range(i + 1, nb_cntry):
            if mat[i][j] > maxi:
                maxi = mat[i][j]
            elif mat[i][j] < mini:
                mini = mat[i][j]
    return maxi, mini


def extract(obj):
    url = None
    if obj == "tmja":
        extract_dir = "tmja2018"
        filename = "tmja2018"
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
