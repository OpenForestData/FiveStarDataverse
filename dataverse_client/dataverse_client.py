import pysolr
import requests
from pyDataverse.api import Api
from rest_framework import status

from dataverse_client.dataverse_repository_response import DataverseMetricResponse
from dataverse_client.exceptions import DataverseClientConnectionException
from fivestar.settings.common import DATAVERSE_URL, METRICS_DATAVERSE_TYPES


# TODO add loggers


class DataverseClient:
    """
    Class responsible for getting dataverse metrics informations
    """

    def __init__(self, client: Api, solr_client: pysolr.Solr):
        self.__dataverse_client = client
        self.__solr_client = solr_client
        self.check_connections()

    def check_connections(self) -> bool:
        """
        Checks connection of dataverse nad solr clients
        """
        if not self.__check_connections():
            raise DataverseClientConnectionException('Could not connect to Dataverse')
        return True

    def __check_connections(self) -> bool:
        """
        Method responsible for checking connection of each client used in repository
        """
        return True if self.__dataverse_client.status == 'OK' and self.__solr_client.verify else False

    @staticmethod
    def get_metrics(data_type: str, to_month=None) -> DataverseMetricResponse:
        """
        Static method responsible for getting metrics total data of dataverse
        """
        if data_type not in METRICS_DATAVERSE_TYPES:
            data_type = 'dataverses'
        # if past_days:
        #     dataverse_response = requests.get(DATAVERSE_URL + f'/api/info/metrics/{data_type}/pastDays/{past_days}')
        if to_month:
            dataverse_response = requests.get(DATAVERSE_URL + f'/api/info/metrics/{data_type}/toMonth/{to_month}')
        else:
            dataverse_response = requests.get(DATAVERSE_URL + f'/api/info/metrics/{data_type}')
        if dataverse_response.status_code != status.HTTP_200_OK:
            return DataverseMetricResponse(False)
        return DataverseMetricResponse(True, dataverse_response)

    @staticmethod
    def get_metrics_by_category_of_dataverses() -> DataverseMetricResponse:
        """
        Static method responsible for getting category of dataverses metrics
        """
        dataverse_response = requests.get(DATAVERSE_URL + '/api/info/metrics/dataverses/byCategory')
        if dataverse_response.status_code != status.HTTP_200_OK:
            return DataverseMetricResponse(False)
        return DataverseMetricResponse(True, dataverse_response)

    @staticmethod
    def get_metrics_by_subject_of_datasets(to_month: str = None) -> DataverseMetricResponse:
        """
        Static method responsible for getting subject of datasets metrics
        """
        if to_month:
            dataverse_response = requests.get(
                DATAVERSE_URL + f'/api/info/metrics/datasets/bySubject/toMonth/{to_month}')
        else:
            dataverse_response = requests.get(
                DATAVERSE_URL + '/api/info/metrics/datasets/bySubject')
        if dataverse_response.status_code != status.HTTP_200_OK:
            return DataverseMetricResponse(False)
        return DataverseMetricResponse(True, dataverse_response)
