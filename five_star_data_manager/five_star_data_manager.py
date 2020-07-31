import json
import pysolr
import requests
from pyDataverse.api import Api
from rest_framework import status

from dataverse_client.exceptions import DataverseClientConnectionException


class FiveStarDataManager:
    """
    Class responsible for populating five star to files data in dataverse
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

    def change_file_rating(self, persistent_file_id: str, rate: int) -> bool:
        url = 'https://dataverse.whiteaster.com/api/files/3/metadata'
        data = {"description": "adawwdad"}
        headers = {'X-Dataverse-key': "9c9d2213-482d-405d-9490-96b984b96898"}

        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code == status.HTTP_200_OK:
            return True
        return False
