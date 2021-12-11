from wikidata.model.Query import Query

ANSWER_FORMAT: str = 'json'  # (query and) answer format

def build_action_wb_get_entities(qid: str, props: str = 'claims') -> Query:
    """"""
    return Query({
        "action": "wbgetentities",
        "ids": qid,
        "sites": "enwiki",
        "languages": "en",
        "sitefilter": "enwiki",
        "props": props,
        "format": ANSWER_FORMAT,
    })


def build_query_fetch_qid(page_title: str) -> Query:
    """"""
    return Query({
        "action": "wbsearchentities",
        "search": page_title,
        "language": "en",
        "format": ANSWER_FORMAT,
        "uselang": "user",
        "errorformat": "bc",
    })
