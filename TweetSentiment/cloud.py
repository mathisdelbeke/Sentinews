import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from flightsql import FlightSQLClient

class DataLayer:
    def __init__(self):
        self.org = "Embedded Linux"
        self.bucket = "Tweets"
        self.token = "DL4yeZwTRh5EW9NtRcIF7EaYVjCfa_wloV8V-eToZFeIvki24M5n0SJy4_HavpgoEB_-DEcEgq-ZdveTaxpt6Q=="

    def write_test(self):
        url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
        write_client = influxdb_client.InfluxDBClient(url=url, token=self.token, org=self.org)
        write_api = write_client.write_api(write_options=SYNCHRONOUS)
        data = {
            "point1": {
                "sentiment": "positive",
                "tweet": "Ik ben super blij",
            },
            "point2": {
                "sentiment": "neutral",
                "tweet": "Ik eet appels",
            },
            "point3": {
                "sentiment": "negative",
                "tweet": "Ik haat mijn leven",
            }
        }
        for key in data:    
            point = (       
                Point("Tweets")
                .field(data[key]["sentiment"], data[key]["tweet"])
            )
            write_api.write(bucket=self.bucket, org=self.org, record=point)
            time.sleep(1) # separate points by 1 second
        print("Complete. Return to the InfluxDB UI.")
    
    def read_test(self):
        query = """SELECT *
        FROM 'Tweets'
        WHERE time >= now() - interval '24 hours'"""

        # Define the query client
        query_client = FlightSQLClient(
        host = "eu-central-1-1.aws.cloud2.influxdata.com",
        token = self.token,
        metadata={"bucket-name": "Tweets"})

        # Execute the query
        info = query_client.execute(query)
        reader = query_client.do_get(info.endpoints[0].ticket)

        # Convert to dataframe
        data = reader.read_all()
        df = data.to_pandas()
        print(df)

test = DataLayer()
test.write_test()
test.read_test()
