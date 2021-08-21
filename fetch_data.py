import json
import pdal
import geopandas as gpd
from shapely.geometry import Polygon, Point
from script.region_selector import dataset_path
from script.edit_pipeline import edit_pipeline
#from logger import Logger

#logger = Logger()
#logger = logger.get_logger('FetchData')

class FetchData():
    def __init__(self, polygon, region:str, input_epsg=3857, output_epsg=4326):

        self.polygon = polygon
        self.region = region
        self.input_epsg = input_epsg
        self.output_epsg = output_epsg

    def get_polygon_boundaries(self, polygon: Polygon):
        polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])

        polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.input_epsg)
        minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds

        polygon_input = 'POLYGON(('
        xcords, ycords = polygon_df['geometry'][0].exterior.coords.xy
        for x, y in zip(list(xcords), list(ycords)):
            polygon_input += f'{x} {y}, '
        polygon_input = polygon_input[:-2]
        polygon_input += '))'
        #print(polygon_input)
        #print(f"({[minx, maxx]},{[miny,maxy]})")
        return f"({[minx, maxx]},{[miny,maxy]})", polygon_input


    def creat_pipeline(self):
        bound, polygon_input = self.get_polygon_boundaries(self.polygon)
        full_dataset_path, tif_path, laz_path = dataset_path(self.region)
        print(full_dataset_path)
        if type(full_dataset_path) == str:
            edited_json = edit_pipeline(full_dataset_path, laz_path, tif_path, self.output_epsg, bound, polygon_input)
            #print(edited_json)
            pipeline = pdal.Pipeline(json.dumps(edited_json))
            return pipeline
        else:
            pipeline_list = []
            for i in range(len(tif_path)):
                edit_json = edit_pipeline(full_dataset_path[i], laz_path[i], tif_path[i], bound)
                pipelines = pdal.Pipeline(json.dumps(edit_json))
                pipeline_list.append(pipelines)
            return pipeline_list



    def run_pipeline(self):
        pipelines = self.creat_pipeline()
        if type(pipelines)==list:
            metadata_list = []
            log_list = []
            for pipeline in pipelines:
                try:
                    pipeline.execute()
                    metadata = pipeline.metadata
                    log = pipeline.log
                    metadata_list.append(metadata)
                    log_list.append(log)
                except RuntimeError as e:
                    print(e)
                    continue
        else:
            print("I am here")
            pipelines.execute()
            metadata = pipelines.metadata
            log = pipelines.log

if(__name__ == '__main__'):
    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.756055, 41.918115]
    polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
    region = "IA_FullState"
    data_fetcher = FetchData(polygon, region)
    pipeline_list = data_fetcher.creat_pipeline()
    data_fetcher.run_pipeline()


