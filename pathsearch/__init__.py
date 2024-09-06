from .pathsearch_functions import (
    detail_path,
    bidirectional_bfs
)
from rdflib import Namespace
from rdflib.namespace import GEO
from rdflib.plugins.sparql.operators import register_custom_function

__version__ = "0.1"

register_custom_function(GEO.detail_path, detail_path) # type: ignore
register_custom_function(GEO.bidirectional_bfs, bidirectional_bfs) # type: ignore
