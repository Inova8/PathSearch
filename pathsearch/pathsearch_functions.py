from rdflib.paths import Path
from rdflib import Graph,URIRef
from rdflib.namespace import RDF, SDO, OWL, RDFS,Namespace,NamespaceManager

from collections import deque

def bidirectional_bfs(graph, startEntities, goalEntities,excludedProperties=[]):#-(RDF.type | OWL.sameAs)):   # type: ignore
    def getSameAsEntities(node,graph):
        sameAsEntities=[node]
        for reconciledEntity in graph.subjects(object=node, predicate = OWL.sameAs, unique=True ):
            for sameAsNode in graph.objects(subject=reconciledEntity, predicate = OWL.sameAs, unique=True ):
                if sameAsNode not in sameAsEntities:
                    sameAsEntities.append(sameAsNode)
        return sameAsEntities

    def getNeighbors(entity, direction, graph,  excludedProperties=[]):    
        """
        Get neighbors of a node from the graph. `direction` is either 'forward' for outbound links
        or 'backward' for inbound links.
        """

        if direction == 'forward':
            nextEntities=[]
            sameAsEntities=getSameAsEntities(entity, graph)
            for sameAsEntity in sameAsEntities:
                #for nextNode in  graph.objects(subject=sameAsNode, predicate=predicate, unique=True):   # type: ignore
                for (_,propertyNode,nextNode,_) in graph.quads((sameAsEntity,   None ,None,None)):   
                    if (type(nextNode) == URIRef)  and  (nextNode not in nextEntities) and (propertyNode not in excludedProperties): 
                        nextEntities.append(nextNode) 
                #for priorNode in graph.subjects(object=sameAsNode, predicate=predicate, unique=True):   # type: ignore
                for (priorNode,propertyNode,_,_) in graph.quads((None, None,  sameAsEntity,None )):   
                    if (priorNode not in nextEntities) or (propertyNode not in excludedProperties):
                        nextEntities.append(priorNode) 
            return nextEntities
        else:
            priorEntities=[]
            sameAsEntities=getSameAsEntities(entity, graph)
            for sameAsEntity in sameAsEntities:
                    #for nextNode in  graph.objects(subject=sameAsNode, predicate=predicate, unique=True):   # type: ignore
                    for (_,propertyNode,nextNode,_) in graph.quads((sameAsEntity,  None ,None,None)): 
                        if (type(nextNode) == URIRef)  and  (nextNode not in priorEntities) and (propertyNode not in excludedProperties):
                            priorEntities.append(nextNode)
                    #for priorNode in graph.subjects(object=sameAsNode, predicate=predicate, unique=True):   # type: ignore
                    for (priorNode,propertyNode,_,_) in graph.quads((None,  None,  sameAsEntity,None )):
                        if  (priorNode not in priorEntities) and (propertyNode not in excludedProperties): 
                            priorEntities.append(priorNode) 
            return priorEntities

    # Initialize queues, visited nodes, and parent pointers for both searches   
    queue_from_start = deque([(entity, [entity]) for entity in startEntities])
    queue_from_goal = deque([(entity, [entity]) for entity in goalEntities])
    visited_from_start = set(startEntities)
    visited_from_goal = set(goalEntities)
    parents_from_start = {entity: None for entity in startEntities}
    parents_from_goal = {entity: None for entity in goalEntities}
    pathLength =0
    while queue_from_start and queue_from_goal:
        # BFS from start
        if queue_from_start:
            currentEntity, path = queue_from_start.popleft()
            if currentEntity in visited_from_goal:
                if parents_from_goal[currentEntity]:
                    connectedPath= path +  parents_from_goal[currentEntity][::-1]# type: ignore
                    return connectedPath 
                else:
                    return path
            neighbors= getNeighbors(currentEntity, 'forward', graph, excludedProperties)
            for neighbor in neighbors:
                if neighbor not in visited_from_start:
                    queue_from_start.append((neighbor, path + [neighbor]))
                    visited_from_start.add(neighbor)
                    parents_from_start[neighbor] = path # type: ignore
            pathLength+=1

        # BFS from goal
        if queue_from_goal:
            currentEntity, path = queue_from_goal.popleft()
            if currentEntity in visited_from_start:
                if parents_from_start[currentEntity]:
                    connectedPath=   path[::-1]# type: ignore
                    return connectedPath # type: ignore #[1:]
                else:
                    connectedPath= parents_from_start[currentEntity] +   path[::-1]# type: ignore
                    return connectedPath # type: ignore #[1:]
            neighbors= getNeighbors(currentEntity, 'backward', graph,excludedProperties)
            for neighbor in neighbors:
                if neighbor not in visited_from_goal:
                    queue_from_goal.append((neighbor, path + [neighbor]))
                    visited_from_goal.add(neighbor)
                    parents_from_goal[neighbor] = path # type: ignore
            pathLength+=1
    return None # No path found


def detail_path(graph, path):
  detailedPath=[]
  for step in path:
    name = graph.value(subject=step,predicate=((RDFS.label|URIRef('http://schema.org/name') | URIRef('http://schema.org/familyName') | URIRef('http://schema.org/givenName'))) )# type: ignore
    sameAsNodes= get_sameAsNodes(step,graph)
    detailedPathStep={'iri':step,'sameAsnodes':sameAsNodes, 'name':name}
    detailedPath.append(detailedPathStep)
  return detailedPath