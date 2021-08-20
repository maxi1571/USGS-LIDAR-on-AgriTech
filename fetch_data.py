import json
import pdal
from script.region_selector import dataset_path
from script.edit_pipeline import edit_pipeline

class FetchData():
    def __init__(self, bound, region:str):
        self.bound = bound
        self.region = region

    def creat_pipeline(self):
        full_dataset_path, tif_path, laz_path = dataset_path(self.region)
        if type(full_dataset_path) == str:
            edited_json = edit_pipeline(full_dataset_path, laz_path, tif_path, self.bound)
            print(edited_json)
            pipeline = pdal.Pipeline(json.dumps(edited_json))
            return pipeline
        else:
            pipeline_list = []
            for i in range(len(tif_path)):
                edit_json = edit_pipeline(full_dataset_path[i], laz_path[i], tif_path[i], self.bound)
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
            pipelines.execute()
            metadata = pipelines.metadata
            log = pipelines.log

