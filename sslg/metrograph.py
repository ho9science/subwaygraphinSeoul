import csv
import io
import collections

import matplotlib.pyplot as plt
import networkx as nx


def readSeoulMetro():
    samdasu = {}
    with io.open('../data/seoulmetro.csv', mode='r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar=',')
        next(spamreader)
        for row in spamreader:
            str = "\" ".join(row)
            str = str.replace('\"','')
            obj = str.rstrip().split(',')

            li = []
            li.append(obj[1])
            li.append(obj[2])
            samdasu[obj[3]] = li
        
    od = collections.OrderedDict(sorted(samdasu.items()))
    return od

def makeTransferList(od):
    transfer = {}
    temp_name = ""
    for k, v in od.items():

        if not temp_name :        
            pass
        else:
            for fr, name_line in od.items():
                transfer.setdefault(name_line[0], set()).add(fr)

        temp_name=v[0]
    return transfer

def makeTransferNameList(od):
    transfer = makeTransferList(od)
    return [key for key, values in transfer.items() if len(values) > 1]

def makeTransferFrList(od):
    transfer = makeTransferList(od)
    return [values for key, values in transfer.items() if len(values) > 1]

def makeTransferStationSameFr(transfer_list, od):
    transfer_station = {}
    for station in transfer_list:
        line_list = []
        for fr, v in od.items():
            if station == v[0]:
                line_list.append(fr)
        transfer_station[station]=line_list
    
    return transfer_station

def makeSeoulMetroGraph():
    od = readSeoulMetro()
    G = nx.Graph()
    tempEdge = ""
    tempBranch = ""
    for fr,values in od.items():
        G.add_node(fr,station=values[0])

        if not tempEdge :
            pass
        else:
            if fr[0] == tempEdge[0] and len(fr) >= len(tempEdge):
                G.add_edge(tempEdge,fr,weight=2)
            else:
                G.add_edge(tempBranch,fr,weight=2)

            if len(fr)>len(tempEdge):
                tempBranch = tempEdge

        tempEdge = fr
    
    transfer_list = makeTransferNameList(od)
    #transfer_fr_list = [values for key, values in transfer.items() if len(values) > 1]

    transfer_station = makeTransferStationSameFr(transfer_list, od)
   
    for key, value in transfer_station.items():
        temp_value = ""
        for i in value:
            if not temp_value :        
                pass
            else:
                G.add_edge(temp_value,i,weight=4)
            temp_value = i
    
    return G


G = makeSeoulMetroGraph()
print(nx.shortest_path(G,source="410",target="220"))
# print(nx.shortest_path(G,source="138",target="234-4"))
# print(nx.shortest_path_length(G,source="138",target="234-4"))