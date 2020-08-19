import pysolr
import requests
from rest_framework import status

from dataverse_client.exceptions import DataverseClientConnectionException
from fivestar.settings.common import DATAVERSE_URL, DATAVERSE_KEY


class FiveStarDataManager:
    """
    Class responsible for populating five star to files data in dataverse
    """

    def __init__(self, solr_client: pysolr.Solr):
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
        return self.__solr_client.verify

    def change_files_rating(self, files_identifiers: list, rate: int):
        for file_identifier in files_identifiers:
            self.__class__.change_file_rating(file_identifier['identifier'], rate)
            self.__class__.publish_dataset(file_identifier['parentIdentifier'])

    @staticmethod
    def publish_dataset(dataset_identifier: str):
        url = DATAVERSE_URL + f'/api/datasets/:persistentId/actions/:publish?' \
                              f'persistentId={dataset_identifier}&type=updatecurrent'
        headers = {
            'X-Dataverse-key': DATAVERSE_KEY,
        }
        response = requests.post(url, headers=headers)
        if response.status_code == status.HTTP_200_OK:
            return True
        return False

    @staticmethod
    def change_file_rating(persistent_file_id: str, rate: int) -> bool:
        url = DATAVERSE_URL + f'/api/files/{persistent_file_id}/metadata'
        headers = {
            'X-Dataverse-key': DATAVERSE_KEY,
        }

        files = {
            'jsonData': (None, '{"restrict":false, "categories":' + f'["{rate}"]' + '}'),
        }
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == status.HTTP_200_OK:
            return True
        return False

    def get_files_amount_with_rating(self, rating: int):
        response = self.__solr_client.search("*", **{
            'fq': ['dvObjectType:files', 'publicationStatus:Published', f'fileTags:{rating}']})
        return response.raw_response.get('response', {}).get('numFound', '0')

    # @cached
    def rate_files(self):
        # TODO: Run as celery task each 15 minutes
        one_star_files_ids = self.find_files_for_one_star_rate()
        self.change_files_rating(one_star_files_ids, 1)
        two_star_files_ids = self.find_file_for_two_star_rate()
        self.change_files_rating(two_star_files_ids, 2)
        three_star_files_ids = self.find_file_for_three_star_rate()
        self.change_files_rating(three_star_files_ids, 3)
        four_star_files_ids = self.find_file_for_four_star_rate()
        self.change_files_rating(four_star_files_ids, 4)
        # five_star_files_ids = self.find_file_for_five_star_rate()
        # self.change_files_rating(five_star_files_ids, 5)
        return True

    def find_files_for_one_star_rate(self):
        response = self.__solr_client.search("*", **{
            'fq': ['publicationStatus:Published',
                   '{!join from=identifier to=parentIdentifier}dwctestLicense:(CC0 OR CC-BY OR CC-BY-SA)',
                   'fileTags:0',
                   ], 'fl': ['identifier', 'parentIdentifier']})
        return [{'identifier': doc['identifier'], 'parentIdentifier': doc['parentIdentifier']} for doc in response.docs]

    def find_file_for_two_star_rate(self):
        response = self.__solr_client.search("*", **{
            'fq': ['publicationStatus:Published',
                   '-name:(*txt OR *tsv OR *tab OR *csv OR *ods OR *odf OR *odt OR *ott OR *odm OR *ots OR *odg \
                   OR *otg OR *odp OR *otp OR *odf OR *odc OR *odb OR *cdf OR *nc OR *hdf OR *h5 OR *xml OR *json\
                    OR *html OR *jpg OR *jp2 OR *png OR *svg OR *tiff OR *tif OR *wav OR *aiff OR *flac OR *mp3 OR\
                     *mp4 OR *mj2 OR *shp OR *shx OR *dbf OR *kml OR *gml OR *wkt OR *gpkg OR *geojson OR *tex OR\
                      *odt OR *epub OR *zip OR *gzip OR *tar OR *gz OR *css OR *djvu OR *gpx OR *yaml OR *obj)',
                   'fileTags:0',
                   'dvObjectType:files'
                   ], 'fl': ['identifier', 'parentIdentifier']})
        return [{'identifier': doc['identifier'],
                 'parentIdentifier': doc['parentIdentifier'] if 'parentIdentifier' in doc else ""} for doc in
                response.docs]

    def find_file_for_three_star_rate(self):
        response = self.__solr_client.search("*", **{
            'fq': ['publicationStatus:Published',
                   'name:(*txt OR *tsv OR *tab OR *csv OR *ods OR *odf OR *odt OR *ott OR *odm OR *ots OR *odg OR\
                    *otg OR *odp OR *otp OR *odf OR *odc OR *odb OR *cdf OR *nc OR *hdf OR *h5 OR *xml OR *json OR \
                    *html OR *jpg OR *jp2 OR *png OR *svg OR *tiff OR *tif OR *wav OR *aiff OR *flac OR *mp3 OR *mp4\
                     OR *mj2 OR *shp OR *shx OR *dbf OR *kml OR *gml OR *wkt OR *gpkg OR *geojson OR *tex OR *odt OR\
                      *epub OR *zip OR *gzip OR *tar OR *gz OR *css OR *djvu OR *gpx OR *yaml OR *obj)',
                   'fileTags:0',
                   'dvObjectType:files'
                   ], 'fl': ['identifier', 'parentIdentifier']})
        return [{'identifier': doc['identifier'], 'parentIdentifier': doc['parentIdentifier']} for doc in response.docs]

    def find_file_for_four_star_rate(self):
        response = self.__solr_client.search("*", **{
            'fq': ['publicationStatus:Published',
                   'parentIdentifier:*doi*',
                   'fileTags:0',
                   'dvObjectType:files'
                   ], 'fl': ['identifier', 'parentIdentifier']})
        return [{'identifier': doc['identifier'], 'parentIdentifier': doc['parentIdentifier']} for doc in response.docs]

    def find_file_for_five_star_rate(self):
        response = self.__solr_client.search("*", **{
            'fq': ['publicationStatus:Published',
                   'parentIdentifier:*doi*',
                   'fileTags:0',
                   'dvObjectType:files'
                   ], 'fl': ['identifier', 'parentIdentifier']})
        return [{'identifier': doc['identifier'], 'parentIdentifier': doc['parentIdentifier']} for doc in response.docs]
