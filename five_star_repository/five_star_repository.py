import pysolr
from pyDataverse.api import Api

from cache_manager.cache_manager import cached
from dataverse_client.dataverse_client import DataverseClient
from five_star_data_manager.five_star_data_manager import FiveStarDataManager
from fivestar.settings.common import DATAVERSE_URL, SOLR_COLLECTION_URL


class FiveStarRepository:
    """
    Class responsible for preparing, joining and
    modifying data from repository and prepare them for each view
    """

    def __init__(self):
        self.__client = DataverseClient(Api(DATAVERSE_URL),
                                        pysolr.Solr(SOLR_COLLECTION_URL))
        self.__five_star_manager = FiveStarDataManager(
            Api("https://dataverse.whiteaster.com", api_token="9c9d2213-482d-405d-9490-96b984b96898"),
            pysolr.Solr("http://192.168.1.241:8985/solr/collection1/"))

    @cached
    def get_metrics(self, data_type: str, date_range: list):
        """
        Obtain metrics for each month and data type for each month
        :param data_type: dataverses, files, datasets, downloads
        :param date_range: list of dates in string format: YYYY-MM
        :return: dict with metrics per each month
        """
        cumulative_metrics = self.get_cumulative_metrics(data_type, date_range)
        dates = [date_cumulative_metric for date_cumulative_metric, _ in cumulative_metrics.items()]
        cumulative_metrics_values = [value for _, value in cumulative_metrics.items()]
        metrics_per_month = [y['count'] - x['count'] for x, y in
                             zip(cumulative_metrics_values, cumulative_metrics_values[1:]) if
                             'count' in x and 'count' in y]
        month_metrics = dict(zip(dates[1:], metrics_per_month))
        total = sum([value for _, value in month_metrics.items()])

        # dataset by subject
        cumulative_metrics_by_subject = self.get_cumulative_metrics_by_subject(date_range)
        # values_for_subject_in_month = {}
        #         # for _, list_of_subjects in cumulative_metrics_by_subject.items():
        #         #     for subject in list_of_subjects:
        #         #         if subject['subject'] not in values_for_subject_in_month:
        #         #             values_for_subject_in_month[subject['subject']] = []
        #         #         values_for_subject_in_month[subject['subject']].append(subject['count'])
        #         # olo = values_for_subject_in_month

        # metrics by dataverse
        metrics_by_dataverse = self.get_metrics_by_category_of_dataverses()
        return {
            'months': month_metrics,
            'total': total,
            'months_percent': {month: "%.2f" % (current / total) for month, current in month_metrics.items()},
            'by_subject': cumulative_metrics_by_subject,
            'by_dataverse': metrics_by_dataverse,
            'five_star_metrics': five_star_metrics
        }

    @staticmethod
    def get_five_star_metrics(self) -> dict:
        return {}

    def get_cumulative_metrics(self, data_type: str, date_range: list) -> dict:
        cumulative_metrics = {}
        for date in date_range:
            cumulative_metrics[date] = self.__client.get_metrics(data_type, date).get_data()
        return cumulative_metrics

    def get_cumulative_metrics_by_subject(self, date_range: list) -> dict:
        cumulative_metrics = {}
        for date in date_range:
            cumulative_metrics[date] = self.__client.get_metrics_by_subject_of_datasets(date).get_data()
        return cumulative_metrics

    def get_metrics_by_category_of_dataverses(self) -> dict:
        return self.__client.get_metrics_by_category_of_dataverses().get_data()

    def rate_files(self):
        self.__five_star_manager.change_file_rating("3", 1)
