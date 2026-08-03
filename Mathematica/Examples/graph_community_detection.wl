(* Detect communities in a small graph with two dense groups. *)

ClearAll[withinGroupEdges];

withinGroupEdges[group_List] := UndirectedEdge @@@ Subsets[group, {2}];

firstGroup = Range[1, 5];
secondGroup = Range[6, 10];
bridgeEdges = {3 <-> 7, 5 <-> 6};

graph = Graph[
    Join[
        withinGroupEdges[firstGroup],
        withinGroupEdges[secondGroup],
        bridgeEdges
    ],
    VertexLabels -> "Name",
    GraphLayout -> "SpringElectricalEmbedding",
    ImageSize -> Large
];

communities = FindGraphCommunities[graph];

Print["Detected communities: ", communities];
Print["Community sizes: ", Length /@ communities];

communityPlot = CommunityGraphPlot[
    graph,
    communities,
    VertexLabels -> "Name",
    ImageSize -> Large,
    PlotLabel -> "Detected graph communities"
];

communityPlot
