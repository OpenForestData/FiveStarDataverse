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


class DataverseClientSearchResponse(DataverseClientResponse):
    """
    Basic solr response search class, responsible for handling
    proper formatting of solr search response
    """

    def get_facets(self) -> dict:
        """
        Shows all facets from solr response
        """
        try:
            return self.data.facets
        except Exception:
            return {}

    def get_facet_fields_values(self) -> dict:
        """
        Property to return proper format of facet fields
        """
        facet_values_dict = {}
        facets = self.get_facets()
        if 'facet_fields' in facets:
            for field_name, list_of_values in facets['facet_fields'].items():
                facet_values_dict[field_name] = {
                    'attributes': [{
                        'name': list_of_values[0::2][i],
                        'amount': list_of_values[1::2][i]
                    } for i in range(0, len(list_of_values[0::2]))]
                }
        return facet_values_dict

    def get_result(self) -> list:
        """
        Show results of solr search request
        """
        try:
            return self.data.docs
        except Exception:
            return []

    def get_number_of_results(self) -> int:
        """
        Gets full amount of objects
        """
        try:
            return self.data.raw_response['response']['numFound']
        except Exception:
            return 0


class DataverseDetailDatasetClientResponse(DataverseClientResponse):
    """
    Class responsible for handling dataverse dataset details format
    proper handling
    """

    def get_json_data(self):
        try:
            return json.loads(self.data)['data']
        except Exception:
            return {}

    def prepare_format(self):
        data_basic_format = self.get_json_data()
        data_basic_format['alternativeURL'] = ""
        data_basic_format['providers'] = []
        try:
            fields = {key['typeName']: key for key in
                      data_basic_format['latestVersion']['metadataBlocks']
                      ['citation']['fields']}
        except AttributeError:
            fields = None
        keys = fields.keys()
        if 'alternativeURL' in keys:
            data_basic_format['alternativeURL'] = fields['alternativeURL']['value']
        if 'author' in keys:
            try:
                data_basic_format['providers'] = fields['author']['value']
            except AttributeError:
                pass
        return data_basic_format


class DataverseDataFileMetadataResponse(DataverseClientResponse):
    """
    Class responsible for handling dataverse details response
    """

    def get_data(self):
        try:
            return json.loads(self.data.text)
        except Exception:
            return {}


class DataverseMetricResponse(DataverseClientResponse):
    """
    Class responsible for wrapping dataverse metrics api response
    """
