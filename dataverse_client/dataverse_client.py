import requests
from pyDataverse.api import Api
import pysolr
from rest_framework import status

from fivestar.settings.common import DATAVERSE_URL, METRICS_DATAVERSE_TYPES
from dataverse_client.dataverse_repository_response import DataverseClientResponse, \
    DataverseClientSearchResponse, DataverseDetailDatasetClientResponse, \
    DataverseDataFileMetadataResponse, DataverseMetricResponse
from dataverse_client.exceptions import DataverseClientConnectionException


# TODO add loggers


class DataverseClient:
    """
    Repository pattern class to get each data from single dataverse instance
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

    def get_dataset_details(self, dataset_id: str) -> DataverseDetailDatasetClientResponse:
        """
        Method responsible for getting datased base on oid
        """
        return self.__get_dataset_details(dataset_id)

    def __get_dataset_details(self, identifier: str) -> DataverseDetailDatasetClientResponse:
        """
        Protected method responsible for obtaining dataset data
        based on identifier
        """
        response_from_dataverse = self.__dataverse_client.get_dataset(identifier)
        success = True if response_from_dataverse.status_code == requests.codes.ok else False
        return DataverseDetailDatasetClientResponse(success, response_from_dataverse.content)

    def __create_search_params(self, params: dict = None) -> dict:
        """
        Creates search params based on given dict with lists of strings as values
        Always basic search params should be provided as follow
        """
        search_query = {
            "fq": ["publicationStatus:Published"],
            'facet': ['on'],
            "facet.limit": ["-1"],
            "sort": []
        }

        if params:
            # TODO: Optimalization required
            for key, search_params in params.items():
                if key not in search_query:
                    search_query[key] = []
                if isinstance(search_params, list):
                    for search_param_value in search_params:
                        search_query[key].append(search_param_value)
        return search_query

    def search(self, phrase="*", params=None) -> DataverseClientSearchResponse:
        """
        Protected method responsible for obtaining searching results
        """
        try:
            response_from_dataverse = self.__solr_client.search(phrase, **self.__create_search_params(params))
            response = DataverseClientSearchResponse(True, response_from_dataverse)
        except Exception as ex:
            print(ex)
            response = DataverseClientSearchResponse(False)
        return response

    def get_metadata_blocks(self) -> DataverseClientResponse:
        """
        Method responsible for obtaining dataverse
        metadata fields collections
        """
        try:
            response_from_dataverse = self.__dataverse_client.get_metadatablocks()
            response = DataverseClientResponse(True, response_from_dataverse)
        except Exception as ex:
            print(ex)
            response = DataverseClientResponse(False)
        return response

    def get_metadata_details_for_block(self, identifier: str) -> DataverseClientResponse:
        """
        Method to get details metadata attributes for block,
        based on name
        """
        try:
            response_from_dataverse = self.__dataverse_client.get_metadatablock(identifier)
            response = DataverseClientResponse(True, response_from_dataverse)
        except Exception:
            # TODO: handle exception
            response = DataverseClientResponse(False)
        return response

    @staticmethod
    def get_datafile_metadata(datafile_id: str) -> DataverseDataFileMetadataResponse:
        """
        Method responsible for obtaining data about datafile based
        on it's id.
        """
        dataverse_response = requests.get(DATAVERSE_URL + f'/api/files/{datafile_id}/metadata')
        if dataverse_response.status_code != 200:
            return DataverseDataFileMetadataResponse(False)
        return DataverseDataFileMetadataResponse(True, dataverse_response)

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
