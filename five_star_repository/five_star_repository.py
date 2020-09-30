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
        self.__five_star_manager = FiveStarDataManager(pysolr.Solr(SOLR_COLLECTION_URL))

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
        cumulative_metrics_by_subject = self.get_cumulative_metrics_by_subject(date_range)
        five_star_metrics = self.get_five_star_metrics()
        metrics_by_dataverse = self.get_metrics_by_category_of_dataverses()
        return {
            'months': month_metrics,
            'total': total,
            'months_percent': {month: "%.2f" % (current / total) for month, current in month_metrics.items()},
            'by_subject': cumulative_metrics_by_subject,
            'by_dataverse': metrics_by_dataverse,
            'five_star_metrics': five_star_metrics
        }

    def get_five_star_metrics(self) -> dict:
        ratings = [
            {"star": 1, "amount": self.get_star_amount_for_rate(1)},
            {"star": 2, "amount": self.get_star_amount_for_rate(2)},
            {"star": 3, "amount": self.get_star_amount_for_rate(3)},
            {"star": 4, "amount": self.get_star_amount_for_rate(4)},
            {"star": 5, "amount": self.get_star_amount_for_rate(5)}
        ]
        all_files_amount = sum([rate["amount"] for rate in ratings])
        if all_files_amount != 0:
            percent_ratings = [{rate["star"]: "%.2f" % (rate["amount"] / all_files_amount)} for rate in ratings]
        else:
            percent_ratings = [{rate["star"]: "%.2f" % 0} for rate in ratings]
        return {"ratings": ratings, "percent_ratings": percent_ratings}

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

    @cached
    def get_star_amount_for_rate(self, rate: int):
        return self.__five_star_manager.get_files_amount_with_rating(rate)

    def rate_files(self):
        self.__five_star_manager.rate_files()
        return True
