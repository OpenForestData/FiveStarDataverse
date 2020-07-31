import datetime
from datetime import datetime as dt

import pandas
from django.http import JsonResponse
from rest_framework.views import APIView

from five_star_repository.five_star_repository import FiveStarRepository


class FiveStarStats(APIView):
    """
    Basic view for getting five star stats
    """
    permission_classes = ()

    def get(self, request):
        five_star_repository = FiveStarRepository().rate_files()
        response = {'test': five_star_repository}
        return JsonResponse(response, safe=False)


class Metrics(APIView):
    """
    Class responsible for getting metrics from dataverse
    to query params: to-month : RRRR-MM, pst-days: 12
    """

    def get(self, request):
        data_type = request.query_params.get('data-type', 'downloads')
        from_date_string = request.query_params.get('from', "2020-01")
        to_date_string = request.query_params.get('to', "2020-07")
        from_date = dt.strptime(from_date_string, '%Y-%m').replace(day=1)
        first_month_in_ragne = from_date - datetime.timedelta(days=1)
        to_date = dt.strptime(to_date_string, '%Y-%m')
        months = pandas.date_range(first_month_in_ragne.strftime("%Y-%m"),
                                   to_date.strftime("%Y-%m"),
                                   freq='MS').strftime("%Y-%m").tolist()
        metrics_for_date_range = FiveStarRepository().get_metrics(data_type,
                                                                  date_range=months)

        return JsonResponse(metrics_for_date_range, safe=False)
