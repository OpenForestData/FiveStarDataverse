import json


class DataverseClientResponse:
    """
    Class responsible for creating all responses from dataverse api
    """

    def __init__(self, success: bool = False, data=None):
        self.__is_success = success
        self.__dataverse_data = data

    @property
    def is_success(self):
        return self.__is_success

    @property
    def data(self):
        return self.__dataverse_data

    def get_data(self):
        try:
            data = json.loads(self.data.text)['data']
        except Exception as ex:
            # TODO: add exception handler
            data = {}
            print(ex)
        return data


class DataverseMetricResponse(DataverseClientResponse):
    """
    Class responsible for wrapping dataverse metrics api response
    """
