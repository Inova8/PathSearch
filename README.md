# PathSearch

Bidirectional BFS algorithm applied to RDF graph

# Bidirectional BFS algorithm

Uses BFS to find the shortest path(s) that visits every node provided.

[https://medium.com/@zdf2424/discovering-the-power-of-bidirectional-bfs-a-more-efficient-pathfinding-algorithm-72566f07d1bd]()

This would be used as follows:

* Use vectorIndex to find most important senetences that match question posed by user.
  * "How is Arnold Swarzzenged connected to Rosemount University"
  * => sentence#n, sentence#m ...
* Use the entityReconciliationGraph to find a list of entities to which these sentences refer
  * Put another way, all of the entities that were derived from the matching sentences
  * entity#x rdfs:seeAlso sentence#1, entity#y rdfs:seeAlso sentence#2, ...
* Find all shortest paths that connect these entities
  * entity#x->entity#a->entity#b->entity#y
* Find all of the sentences referred to by the entities in these paths
  * sentence#1, sentence#2, ...
* Concatenate all of the sentences to use as the context for the question when it is submitted to the LLM
