import requests
import datetime

from typing import List, Dict

from wikidata.model import Query, Queries
from wikidata.model.JsonObject import JsonObject

import wikidata.model.Cache as cache


Qid = str


def _process_qid_answer(json_answer: JsonObject) -> str:
    """Extract QID from a JsonObject fetch qid answer"""
    try:
        # check that the answer is not empty
        searches = json_answer.json['search']

        if not searches:
            return ''

        return searches[0]['title']

    # in case we get an unexpected json answer (e.g. invalid fields)
    except Exception as e:
        print("_process_qid_answer encountered an unknown error: " + e.__str__())
        return ''


class QueryManager:
    """
    """

    class __QueryManager:
        """Inner class used to implement the singleton design pattern"""

        def __init__(self):
            # TODO remove
            self.got_online = 0
            self.got_cache = 0


            self.session = requests.Session()
            self.country_map = dict()
            self.tendency_map = dict()
            self.politician_map = cache.Cache(1)

    __instance = None  # Singleton QueryManager object

    def __init__(self):
        if not QueryManager.__instance:
            QueryManager.__instance = QueryManager.__QueryManager()

    def __getattr__(self, item):
        return getattr(self.__instance, item)


    def stats_TODO_remove(self):
        print(f"  - gotten from online: {self.got_online} vs gotten from cache {self.got_cache}")

    def fetch_qid_information(self, qid: Qid, pids: List[str] = None) -> Dict[Qid, List]:
        """

        :param qid:
        :param pids:
        :return:

        :example: self.fetch_qid_information('Q22686', ['P102'])  # returns all parties Donald Trump was/is part of
        """
        def claim_to_value(claim):
            if claim['mainsnak']['snaktype'] == 'novalue':
                return ''
            return claim['mainsnak']['datavalue']['value']['id']

        # fetch the content of the page with the corresponding qid
        query = Queries.build_action_wb_get_entities(qid)
        json_answer = self.send_get_query(query)

        if 'error' in json_answer.json.keys() or 'warning' in json_answer.json.keys():
            print(f'Encountered an error/warning when fetching information for qid = {qid}')
            json_answer.prettyPrint()
            return {}

        entity = json_answer.json['entities'][qid]

        if pids is None:
            return entity

        result: Dict[Qid, List] = dict()
        for pid in pids:
            try:
                value = map(claim_to_value, entity['claims'][pid])
                result.update({pid: [q for q in list(value) if q]})
            except:
                result.update({pid: list()})

        return result

    def search_party_information(self, party: str, is_qid: bool = False, human_readable: bool = True) -> Dict[Qid, List[str]]:
        qid: Qid = party

        if not is_qid:
            query: Query = Queries.build_query_fetch_qid(party)
            json_answer = self.send_get_query(query)
            qid = _process_qid_answer(json_answer)

            if not qid:
                print(f'Could not fetch a qid for party name \'party\', is \'is_qid\' set to \'False\'?')
                return dict()

        party_information: Dict[Qid, List[Qid]] = self.fetch_qid_information(qid, ['P17', 'P1387'])

        if not human_readable:
            return party_information


        # Translate the country / tendency qids into human-readable strings
        country_qid = party_information.get('P17')[0] if len(party_information.get('P17')) != 0 else None
        tendency_qid = party_information.get('P1387')[0] if len(party_information.get('P1387')) != 0 else None

        # extract the value of the country from its country_qid
        if country_qid is not None:
            if country_qid in self.country_map:
                country_value = self.country_map.get(country_qid)
            else:
                query = Queries.build_action_wb_get_entities(country_qid, props = 'labels')
                json_answer = self.send_get_query(query)
                country_value = json_answer.json['entities'][country_qid]['labels']['en']['value']

                # add the newly found country_qid -> country_value tuple in the cache
                self.country_map.update({country_qid: country_value})

            party_information.update({'P17': [country_value]})


        # extract the value of the tendency from its tendency_qid
        if tendency_qid is not None:
            if tendency_qid in self.tendency_map:
                tendency_value = self.tendency_map.get(tendency_qid)
            else:
                query = Queries.build_action_wb_get_entities(tendency_qid, props = 'labels')
                json_answer = self.send_get_query(query)
                tendency_value = json_answer.json['entities'][tendency_qid]['labels']['en']['value']

                # add the newly found tendency_qid -> tendency_value tuple in the cache
                self.tendency_map.update({tendency_qid: tendency_value})

            party_information.update({'P1387': [tendency_value]})


        return party_information

    def search_politician_party(self, politician_qid: Qid, date_str: str = None) -> Qid:
        """
        Retrieve the party the politician with qid <politician_qid> was in at the time [date]
        If no date is specified, the current party is returned

        :param politician_qid: the qid of the politician we want the party
        :param date_str: the date of the request party membership (format: 'yyyy-mm')
        :return: the party (qid) the politician was in at [date]

        :example:
          - self.fetch_politician_party('Q22686') # fetches Donald Trump's current party
          - self.fetch_politician_party('Q22686', '2008-04') # fetches Donald Trump's party he was during 2008-04
        """

        def wiki_date_to_time_date(date_ws: str) -> datetime.date:
            """Turns a wikidata date (str) into a datetime.date"""
            time_list: List[str] = date_ws[1:].split('-')

            year: str = time_list[0] if int(time_list[0]) >= 0 else '0'
            month: str = time_list[1] if int(time_list[1]) in range(1, 13) else '01'

            return datetime.date(int(year), int(month), 1)


        parties = list()
        cached = self.politician_map.get(politician_qid)

        if cached is not None:
            parties = cached
            self.got_cache += 1
        else:
            try:
                parties = self.fetch_qid_information(politician_qid)['claims']['P102']
                # self.politician_map[politician_qid] = parties
                self.politician_map.add(politician_qid, parties)
                self.got_online += 1
            except Exception:
                pass

        if len(parties) == 0:
            return ''

        if date_str is None:
            return parties[-1]['mainsnak']['datavalue']['value']['id']


        date_list = list(map(lambda x: int(x), date_str.split('-')))
        date = datetime.date(*date_list, 1)

        # first pass: try to see if we have parties that would tie with the date
        for party in reversed(parties):
            if party['mainsnak']['snaktype'] != 'novalue':
                if 'qualifiers' not in party:
                    continue

                if 'P582' in party['qualifiers']:  # if there's a "end time" for the party membership
                    end_date = wiki_date_to_time_date(party['qualifiers']['P582'][0]['datavalue']['value']['time'])
                    if date > end_date:
                        return ''

                if 'P580' in party['qualifiers']:  # if there's a "start time" for the party membership
                    start_date = wiki_date_to_time_date(party['qualifiers']['P580'][0]['datavalue']['value']['time'])
                    if date >= start_date:
                        return party['mainsnak']['datavalue']['value']['id']

        # second pass: return the last known party, because wikidata decides to sometimes omit the "start_time" and "end_time"
        for party in reversed(parties):
            if party['mainsnak']['snaktype'] != 'novalue':
                return party['mainsnak']['datavalue']['value']['id']

        return ''

    def send_get_query(self, query: Query):
        answer = self.session.get(url=query.url, params=query.params)
        return JsonObject(answer.json())


def main():
    manager = QueryManager()

    for party in ["Republican Party", "Democratic Party"]:
        res = manager.search_party_information(party)
        print(f'Information for party \'{party}\': {res}')

    for date in [None, '2012-02']:
        res = manager.search_politician_party('Q22686', date)  # trump
        print(f'Information on Trump\'s parties after \'{date}\': \'{res}\'')


    res = manager.search_politician_party('Q529090', '2008-10')  # Bill Pascrell
    print(f'Information on Bill\'s party after \'2008-10\': \'{res}\'')

    for date in [None, '2010-10', '1989-10', '1900-01']:
        res = manager.search_politician_party('Q567', date)  # Angela Merkel
        print(f'Information on Angela\'s party after \'{date}\': \'{res}\'')

    for date in [None, '1984-02']:
        res = manager.search_politician_party('Q260464', date)  # Ed Balls
        print(f'Information on Ed\'s party after \'{date}\': \'{res}\'')


if __name__ == '__main__':
    main()
