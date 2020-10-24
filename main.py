from alpha_vantage.timeseries import TimeSeries
import os
import json


class DataSource:
    def __init__(self, data_dir: str):
        self.data_dir = os.path.expanduser(data_dir)
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
            print("Created data dir.")

    def get_data(
        self,
        instrument: str,
        interval: str,
        fmt: str = None,
        refresh: bool = False,
        **kwargs,
    ):
        data_file = os.path.join(self.data_dir, f"{instrument}_{interval}.dat")
        if not refresh and os.path.exists(data_file):
            with open(data_file) as f:
                data = f.readlines()
            print("Read data from file.")
        else:
            data = self._get_data(instrument=instrument, interval=interval, **kwargs)
            print("Read data from client.")
            self.__save(data=data, data_file=data_file)

        data = self.format(data=data, fmt=fmt, **kwargs)
        return data

    def __save(self, data, data_file: str):
        with open(data_file, "w") as f:
            f.write(data)

    def format(self, data, fmt: str, **kwargs):
        raise NotImplementedError()

    def _get_data(self, instrument: str, interval: str, **kwargs):
        raise NotImplementedError()


class AlphaVantage(DataSource):
    def __init__(self, api_key: str, indexing_type: str = "date"):
        super().__init__(data_dir="~/alpha-vantage-data")
        self.api_key = api_key
        self.output_fmt = "json"
        self.indexing_type = indexing_type
        self.ts = TimeSeries(
            key=self.api_key, indexing_type=indexing_type, output_format=self.output_fmt
        )

    def _get_data(self, instrument: str, interval: str, **kwargs):
        output_size = kwargs.get("output_size", "full")
        data, meta_data = self.ts.get_intraday(
            instrument, interval=interval, outputsize=output_size
        )
        return json.dumps(data)

    def format(self, data, fmt: str, **kwargs):
        return data


def main():
    API_KEY = ""
    av = AlphaVantage(api_key=API_KEY, indexing_type="date")
    data = av.get_data(
        instrument="SQ",
        interval="1min",
        refresh=False,
        output_size="full",
    )
    print(data)


main()
