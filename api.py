import requests


class Api:
    """Wrapper for the Skyscanner API on RapidAPI"""

    def __init__(self, api_key):
        """
        Initialise with your api key
        :param api_key: your RapidAPI key
        """
        self.api_key = api_key
        self.rapid_api_host = "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        self.headers = {
            'x-rapidapi-host': self.rapid_api_host,
            'x-rapidapi-key': self.api_key
        }
        self.base_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices"

    def fetch_quotes(self, country, currency, locale, origin, destination, outbound_partial_date,
                     inbound_partial_date=""):
        """
        Fetches cheapest cached quotes for a given trip
        :param country: market country the user is in
        :param currency: currency for returned prices
        :param locale: ISO locale for results
        :param origin: origin place
        :param destination: destination
        :param outbound_partial_date: outbound date, can be YYYY-MM-DD, YYYY-MM, or "anytime"
        :param inbound_partial_date: return date, can be YYYY-MM-DD, YYYY-MM, or "anytime". defaults to empty string for one way
        :return: json object of the results
        """
        url = f"/browsequotes/v1.0/{country}/{currency}/{locale}/{origin}/{destination}/{outbound_partial_date}"
        query = {"inboundpartialdate": inbound_partial_date}

        response = requests.get(self.base_url + url, headers=self.headers, params=query)
        return response.json()

    def create_live_search_session(self, country, currency, locale, origin, destination, outbound_date, adults=1):
        """
        Creates a live search session, allowing for real time prices to be retrieved
        :param country: market country the user is in
        :param currency: currency for returned prices
        :param locale: ISO locale for results
        :param origin: origin place
        :param destination: destination
        :param outbound_date: outbound date, in format YYYY-MM-DD
        :param adults: number of adults to search for, defaults to 1
        :return: search session key
        """
        url = "/pricing/v1.0"
        payload = f"country={country}&currency={currency}&locale={locale}&originPlace={origin}" \
                  f"&destinationPlace={destination}&outboundDate={outbound_date}&adults={adults}"
        headers = self.headers
        headers['content-type'] = "application/x-www-form-urlencoded"
        response = requests.post(self.base_url + url, data=payload, headers=headers)
        session_key = response.headers['location'].rsplit('/', 1)[1]
        return session_key

    def poll_live_search_results(self, session_key, page_index=0, page_size=10):
        """
        Polls the live search session to get fresh prices
        :param session_key: session key for the search, retrieved using create_live_search_session
        :param page_index: desired page number, defaults to 0
        :param page_size: number of results to fetch, defaults to 10
        :return:
        """
        url = f"/pricing/uk2/v1.0/{session_key}"
        query = {"pageIndex": page_index, "pageSize": page_size}

        response = requests.get(self.base_url + url, headers=self.headers, params=query)
        return response.json()
