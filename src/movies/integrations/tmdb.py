# TMBD specific code will go here
import requests, json

class TmdbIntegration:
    def __init__(self, api_key: str, access_token: str):
        self.auth_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        self.root_url = "https://api.themoviedb.org/3/"

    def __call_api(self, endpoint: str, **query_args):
        """
        Actually call the API

        Takes an endpoint and named arguments as query args

        Returns parsed JSON response
        """
        query_args_to_join = []
        for name, value in query_args.items():
            escaped_value = requests.utils.quote(value, safe='')
            query_args_to_join.append('='.join([name, escaped_value]))
        query_args_str = '&'.join(query_args_to_join)
        print("--- 🐞👀 DEBUG Query string", query_args_str)
        url = self.root_url + endpoint + '?' + query_args_str
        print("--- 🐞👀 DEBUG URL", url)
        response = requests.get(url, headers=self.auth_headers)
        print("--- 🐞👀 DEBUG API", response.text)
        loaded_response = json.loads(response.text)
        return loaded_response

    def search_movies(self, query_string: str, **api_args):
        """
        Get movie search results from TMDB

        There are many arguments to the TMDB API, so **api_args is a shortcut to
        make them accessible for now.
        TODO: Make the params that we'll accept explicit

        Returns dict from JSON results
        """
        endpoint = "search/movie"
        api_args['query'] = query_string
        results = self.__call_api(endpoint, **api_args)
        return results

    def get_poster_image_url(self, poster_path):
        image_url = ('https://media.themoviedb.org/'
                     't/p/w300_and_h450_bestv2') + poster_path
        return image_url
