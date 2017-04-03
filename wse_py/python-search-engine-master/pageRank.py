def compute_ranks(graph):
    ranks = {}
    d = 0.85
    numLoops = 10
    npages = len(graph)

    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numLoops):
        newRanks = {}
        for page in graph:
            newRank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newRank = newRank + d * (ranks[node] / len(graph[node]))
            newRanks[page] = newRank
        ranks = newRanks
    return ranks
