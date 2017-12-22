from py2neo import Graph
from textblob import TextBlob
from rake_nltk import Rake
import operator
from gensim import corpora, models, similarities

from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import Search

from django.conf import settings

from capitolzen.proposals.models import Bill, Legislator
from capitolzen.proposals.utils import tf, tfidf, idf
from capitolzen.proposals.documents import BillDocument

class BasicGraph(object):
    graph = Graph(**settings.GRAPH_DATABASE)
    instance = None
    instance_class = None

    def __init__(self, identifier):
        self.instance = self.instance_class.objects.get(id=identifier)

    def merge(self):
        raise NotImplementedError()

    def run(self):
        self.merge()


class BillGraph(BasicGraph):
    instance_class = Bill

    def merge(self):
        query = """
            MERGE (bill:Bill {uuid: $uuid})
            ON CREATE SET bill.created = $created, 
                bill.modified = $modified, bill.state_id = $state_id, 
                bill.remote_id = $remote_id, bill.title = $title
            ON MATCH SET bill.modified = $modified,
                bill.title = $title
            RETURN bill
            """
        self.graph.data(query, parameters={
            "uuid": str(self.instance.id),
            "created": self.instance.created.isoformat(),
            "modified": self.instance.modified.isoformat(),
            "state_id": self.instance.state_id,
            "remote_id": self.instance.remote_id,
            "title": self.instance.title,
        })

    def link_to_sponsors(self):
        from capitolzen.proposals.managers import LegislatorManager
        query = """
        MATCH (bill:Bill {uuid: $bill_uuid}), 
            (legislator:Legislator {remote_id: $remote_id})
        MERGE (bill)<-[r:SPONSOR {
            type: $type
            human_weight: $human_weight
        }]-(legislator)
        RETURN bill, legislator
        """
        for sponsor in self.instance.sponsors:
            # Verify Legislator exists and is updated
            response = LegislatorManager(
                state=self.instance.state.capitalize()
            ).update(None, sponsor.get('leg_id'), None)

            if response:
                # Now that we know that they exist link them to the bill
                if sponsor.get('type') == "primary":
                    human_weight = 2
                else:
                    human_weight = 1
                self.graph.data(query, parameters={
                    "remote_id": sponsor.get('leg_id'),
                    "bill_uuid": str(self.instance.id),
                    "type": sponsor.get('type'),
                    "human_weight": human_weight
                })

    def generate_similarity_score(self):
        # Find words of most interest / value in bill
        # TODO: Might be able to simplify / improve results by using ES's
        # aggregation & significant_terms capabilities.
        es_client = Elasticsearch(
            hosts=settings.ELASTICSEARCH_DSL['default']['hosts'],
            connection_class=RequestsHttpConnection
        )
        r = Rake()
        r.extract_keywords_from_text(self.instance.content)
        key_phrases = [keyphrase[1] for keyphrase in r.get_ranked_phrases()[:3]]
        for phrase in key_phrases:
            s = Search().using(es_client).query('match', content=phrase)
            s.doc_type(BillDocument)
            response = s.execute()
            for hit in response:
                print(hit.id)
        doc_list = []
        scores = {word: tfidf(
            word, self.instance.content, doc_list
        ) for word in self.instance.content.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:3]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

        # Search for other bills with similar keywords

        # Determine the similarity of the given documents

        # Plot scores on relationships between bills
        query = """
        MATCH (bill:Bill) 
        """

    def run(self):
        self.merge()
        self.link_to_sponsors()


class LegislatorGraph(BasicGraph):
    instance_class = Legislator

    def merge(self):
        query = """
        MERGE (legislator:Legislator {uuid: $uuid})
        ON CREATE SET legislator.created = $created, 
            legislator.remote_id = $remote_id,
            legislator.state = $state,
            legislator.active = $active,
            legislator.chamber = $chamber,
            legislator.party = $party,
            legislator.district = $district,
            legislator.email = $email,
            legislator.first_name = $first_name,
            legislator.last_name = $last_name,
            legislator.updated_at = $updated_at,
            legislator.created_at = $created_at
        ON MATCH SET legislator.modified = $modified,
            legislator.active = $active,
            legislator.chamber = $chamber,
            legislator.party = $party,
            legislator.district = $district,
            legislator.email = $email,
            legislator.last_name = $last_name,
            legislator.updated_at = $updated_at
        RETURN legislator
        """
        self.graph.data(query, parameters={
            "uuid": str(self.instance.id),  # index
            "created": self.instance.created.isoformat(),
            "modified": self.instance.modified.isoformat(),
            "remote_id": self.instance.remote_id,  # index
            "state": self.instance.state,
            "active": self.instance.active,
            "chamber": self.instance.chamber,
            "party": self.instance.party,
            "district": self.instance.district,
            "email": self.instance.email,
            "first_name": self.instance.first_name,
            "last_name": self.instance.last_name,
            "updated_at": self.instance.updated_at.isoformat(),
            "created_at": self.instance.created_at.isoformat()
        })
