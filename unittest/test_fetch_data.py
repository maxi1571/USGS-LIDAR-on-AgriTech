import unittest
from fetch_data import FetchData
from shapely.geometry import Polygon, Point

class Test_region_selector(unittest.TestCase):

    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.756055, 41.918115]
    polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
    bound = '([-10425171.940, -10423171.940], [5164494.710, 5166494.710])'
    region = 'AK_NorthSlope_B10_2018'
    def run_pipeline(self):
        MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.756055, 41.918115]
        polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
        #bound = '([-10425171.940, -10423171.940], [5164494.710, 5166494.710])'
        region = 'AK_NorthSlope_B10_2018'
        fetch_data = FetchData(polygon, region)
        fetch_data.run_pipeline()
        self.assertEqual(fetch_data, "IA_FullState")