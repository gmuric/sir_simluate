import networkx as nx
import random

def sir_iterate(G, p, r):
    # iterate through suscepted and calculate the prob of infection

    for n in G.nodes():
        rand = random.uniform(0,1)
        if G.nodes[n]['state']=='S':
            k = [G.nodes[c]['state'] for c in G.neighbors(n)].count('I')        
            if 1-(1-p)**k >= rand:
                G.nodes[n]['next_state']='I'
            else:
                G.nodes[n]['next_state']='S'

    # update state
    for n in G.nodes():
        if G.nodes[n]['state']=='S':
            G.nodes[n]['state'] = G.nodes[n]['next_state']
            G.nodes[n]['next_state'] = ''

        if G.nodes[n]['state'] == 'I':
            if G.nodes[n]['counter'] > r:
                G.nodes[n]['state'] = 'R'
                G.nodes[n]['counter'] = ''
            else:
                G.nodes[n]['counter'] = G.nodes[n]['counter']+1
    return(G)

def sir_simulate(G, p, r, initially_infected, protected_nodes=False):
    
    nx.set_node_attributes(G, 'S', name='state')
    nx.set_node_attributes(G, 0, name='counter')
        
    st = [{'state':'I'}]*len(initially_infected)
    attrs = dict(zip(initially_infected, st))
    nx.set_node_attributes(G, attrs)
    
    if protected_nodes:
        st = [{'state':'R'}]*len(protected_nodes)
        attrs = dict(zip(protected_nodes, st))
        nx.set_node_attributes(G, attrs)
    
    inf = 1
    infected = []
    while inf>0:
        G = sir_iterate(G,p,r)
        inf = len([x for x,y in G.nodes(data=True) if y['state']=='I'])
        infected.append(inf)
    return(infected)