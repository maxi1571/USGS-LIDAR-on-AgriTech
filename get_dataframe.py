from fetch_data import FetchData
from shapely.geometry import Polygon, Point
import geopandas as gpd
import matplotlib.pyplot as plt

class GetDataframe:
    def __init__(self, polygon:Polygon, region) -> None:

        self.polygon = polygon
        self.region = region

    def get_dataframe(self):
        
        data_fetcher = FetchData(self.polygon, self.region)
        data = data_fetcher.run_pipeline()
        df = data_fetcher.get_elevation(data)

        return df
    
    def visualize (self, df: gpd.GeoDataFrame, cmap="terrain") -> None:

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        df.plot(column='elevation', ax=ax, legend=True, cmap=cmap)
        plt.show()
