from fetch_data import FetchData

bound = '([-10425171.940, -10423171.940], [5164494.710, 5166494.710])'
region = 'AK_NorthSlope_B10_2018/'
fetch_data = FetchData(bound, region)
pipelines = fetch_data.creat_pipeline()
print(pipelines)
fetch_data.run_pipeline()
