from rdflib import OWL, RDF, Dataset, Graph, URIRef

from pathsearch.pathsearch_functions import bidirectional_bfs,detail_path

dataset = Dataset()

kennedyGraph = dataset.graph('C:/Users/peter/git/PathSearch/PathSearch/tests/resources/schemakennedys.ttl')
kennedyGraph.parse('C:/Users/peter/git/PathSearch/PathSearch/tests/resources/schemakennedys.ttl')

northwindGraph = dataset.graph('C:/Users/peter/git/PathSearch/PathSearch/tests/resources/northwind.data.v3.rdf')
northwindGraph.parse('C:/Users/peter/git/PathSearch/PathSearch/tests/resources/northwind.data.v3.rdf')

Product_1 = URIRef('http://northwind.com/Product-1')
Employee_1 = URIRef('http://northwind.com/Employee-1')

ArnoldSchwarzenegger = URIRef('http://topbraid.org/examples/kennedys#ArnoldSchwarzenegger')
RosemontCollege = URIRef('http://topbraid.org/examples/kennedys#RosemontCollege')

reconArnoldPerson1=URIRef('http:recon//Arnold/Person_1')

JeanKennedy= URIRef('http://topbraid.org/examples/kennedys#JeanKennedy')
RoseFitzgerald = URIRef('http://topbraid.org/examples/kennedys#RoseFitzgerald')
Harvard = URIRef('http://topbraid.org/examples/kennedys#Harvard')
ManhattanvilleCollege = URIRef('http://topbraid.org/examples/kennedys#ManhattanvilleCollege')

 
Unknown1 = URIRef('http://topbraid.org/examples/kennedys#Unknown1')
Unknown2 = URIRef('http://topbraid.org/examples/kennedys#Unknown2')
Disconnected = URIRef('http://datashapes.org/schema')

dataset.default_context.add((reconArnoldPerson1 ,OWL.sameAs,Employee_1))
dataset.default_context.add((reconArnoldPerson1 ,OWL.sameAs,ArnoldSchwarzenegger))

def test_arnold_rosemont():
    path =bidirectional_bfs(dataset,[ArnoldSchwarzenegger],[RosemontCollege],[RDF.type,OWL.sameAs])
    assert(str(path)=="[rdflib.term.URIRef('http://topbraid.org/examples/kennedys#ArnoldSchwarzenegger'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#MariaShriver'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#EuniceKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#JosephKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#PatriciaKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#RosemontCollege')]")
def test_product_1_employee_1():
    path =bidirectional_bfs(dataset,[Product_1],[Employee_1],[RDF.type,OWL.sameAs])
    assert(str(path)=="[rdflib.term.URIRef('http://northwind.com/Product-1'), rdflib.term.URIRef('http://northwind.com/OrderDetail-10285-1'), rdflib.term.URIRef('http://northwind.com/Order-10285'), rdflib.term.URIRef('http://northwind.com/Employee-1')]")
def test_product_1_arnold():
    path =bidirectional_bfs(dataset,[Product_1],[ArnoldSchwarzenegger],[RDF.type,OWL.sameAs])
    assert(str(path)=="[rdflib.term.URIRef('http://northwind.com/Product-1'), rdflib.term.URIRef('http://northwind.com/OrderDetail-10285-1'), rdflib.term.URIRef('http://northwind.com/Order-10285'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#ArnoldSchwarzenegger')]")
def test_product_1_rosemount():
    path =bidirectional_bfs(dataset,[Product_1],[RosemontCollege],[RDF.type,OWL.sameAs])
    assert(str(path)=="[rdflib.term.URIRef('http://northwind.com/Product-1'), rdflib.term.URIRef('http://northwind.com/OrderDetail-10285-1'), rdflib.term.URIRef('http://northwind.com/Order-10285'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#ArnoldSchwarzenegger'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#MariaShriver'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#EuniceKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#JosephKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#PatriciaKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#RosemontCollege')]")
def test_same():
    path =bidirectional_bfs(dataset,[ArnoldSchwarzenegger],[ArnoldSchwarzenegger],[RDF.type,OWL.sameAs])
    assert(str(path)=="[rdflib.term.URIRef('http://topbraid.org/examples/kennedys#ArnoldSchwarzenegger'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#MariaShriver'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#EuniceKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#JosephKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#PatriciaKennedy'), rdflib.term.URIRef('http://topbraid.org/examples/kennedys#PatriciaKennedy')]")   