import geopandas as gpd
import numpy as np
import contextily as ctx
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from utilitaries.utils import extract, extr, gravity_law

plt.style.use("seaborn-pastel")
sns.set(rc={'figure.figsize': (20, 20)})


class GravLawModel:

    def __init__(self, country, iso_a3):
        """
        :param country: country's name
        :param iso_a3: iso a3 code. (ex : France -> FRA)
        """

        # to avoid bothersome warnings :
        warnings.simplefilter(action="ignore", category=FutureWarning)
        warnings.filterwarnings("ignore")

        self.iso_a3 = iso_a3
        self.country = country
        # As Korea was the main country studied, I used this line to avoid typing the whole country name.
        if self.country == "Korea":
            self.country = "Korea,+Republic+of"
        self.coord = []
        # cntry contains the most populated cities of country
        self.cntry = gpd.read_file(extract(self.country))

        # For France only I managed to get the actual traffic values
        if self.country == "France":
            self.traffic = gpd.read_file(extract("tmja"))
            self.traffic = self.traffic.to_crs(3857)
            assert (len(self.traffic)) > 0, "Erreur lors du chargement des données réelles"

        assert len(self.cntry) > 0, "Le nom du pays est erroné"
        # To match contextily coordinates format
        self.cntry = self.cntry.to_crs(3857)
        #  world is the base map on which we will display our flows and cities
        self.world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Same reason
        self.world = self.world.to_crs(3857)
        # Some columns are useless. Let's get rid of them.
        self.cntry = self.cntry.sort_values(by=["population"], ascending=False)[["name", "population", "geometry"]]
        # Once again, a line only for Korea
        # As Jeju Island is not accesible by road from the Korea, it is not pertinent to keep it.
        if country == "Korea":
            self.cntry = self.cntry.drop(self.cntry.loc[self.cntry['name'] == "Jeju City"].index)
        # We keep the 30 most populated cities

        self.cntry = self.cntry[:30]
        self.T = np.zeros((30, 30))

    def flow_calculate(self):
        """
        Computes the estimated flows between cities
        :return: None
        """
        for i in tqdm(range(30)):
            dist = list(self.cntry.distance(self.cntry.iloc[i]["geometry"]))
            for j in range(i + 1, 30):
                cit_i, cit_j = np.ravel(self.cntry.iloc[i][["geometry", "population"]]), np.ravel(
                    self.cntry.iloc[j][["geometry", "population"]])

                if dist[j] > 10000:
                    self.T[i, j] = gravity_law(cit_i[1], cit_j[1], dist[j])

        for i in tqdm(range(30)):
            self.coord.append(list(np.ravel(self.cntry.iloc[i]["geometry"].bounds[1:-1])))

        maxi, mini = extr(self.T)
        self.T = (self.T - mini) / (maxi - mini)
        maxi, mini = self.cntry["population"].max(), self.cntry["population"].min()
        self.cntry["population"] = (self.cntry["population"] - mini) / (maxi - mini)

    def save(self):
        """
        save the finale file
        :return: None
        """

        # To focus on the country
        base = self.world[self.world["iso_a3"] == self.iso_a3].plot(alpha=0)
        # Plotting the cities proportionaly to their population
        self.cntry.plot(ax=base, markersize=self.cntry["population"] * 1000, color="red", zorder=3, alpha=0.8)
        for i in tqdm(range(0, 30)):
            for j in range(i + 1, 30):
                # plot the flows
                base.plot([self.coord[i][1], self.coord[j][1]], [self.coord[i][0], self.coord[j][0]],
                          zorder=1, color="black", linewidth=(self.T[i, j]*500) ** 0.7, alpha=1)

        if self.country == "France":
            self.traffic.plot(ax=base, zorder=2, linewidth=self.traffic["tmja"] / 10000)

        ctx.add_basemap(base)
        plt.savefig("ressources/GravLawModel_{}.png".format(self.country), bbox_inches='tight')
