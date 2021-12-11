class Query:
    """
    Class that represents a network query
    Attributes:
      - params: dict[str, str]
            Payload of the query (dictionary representation of json object)
      - url: str
            The URL to which the query should be sent
    """

    WIKIDATA_BASE_URL = 'https://www.wikidata.org/w/api.php'

    def __init__(self, params: dict, url: str = WIKIDATA_BASE_URL):
        self.params = params
        self.url = url
