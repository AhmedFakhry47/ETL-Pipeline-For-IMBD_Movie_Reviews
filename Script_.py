from Sentiment_ import *
from ETL_ import *



meta = {'mongoDB_url':"mongodb+srv://enihcam:12345@cluster0.irbss.mongodb.net/<Movie_Review>?retryWrites=true&w=majority",
		'extension'  :"csv"}

test_pipeline = ETL_pipeline(meta)
test_pipeline.operate()

