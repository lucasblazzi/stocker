from api import API
from db import Database


class Sector:
    def load_sectors():
        composed_sectors = list()
        _req_sector = {"endpoint": "sectors"}
        sectors_response = API(_req_sector).get()
        #
        # _req_perf = {"endpoint": "sectors_performance"}
        # performance_response = API(_req_perf).get()
        #
        # for sector in sectors_response:
        #     try:
        #         _sector = next(filter(lambda x: x.get("name") == sector.get("name"), performance_response))
        #         sector["performance"] = _sector["performance"]
        #         sector["updatedAt"] = _sector["lastUpdated"]
        #
        #         composed_sectors.append(_sector)
        #     except StopIteration:
        #         pass

        return sectors_response


def loader():
    sectors = Sector().load_sectors()
    return sectors
