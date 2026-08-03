(* Train a small high-level neural classifier on concentric 2D points. *)

SeedRandom[42];

innerPoints = Table[
    0.8 {Cos[angle], Sin[angle]} + RandomReal[{-0.08, 0.08}, 2],
    {angle, 0, 2 Pi - 2 Pi/24, 2 Pi/24}
];
outerPoints = Table[
    2.0 {Cos[angle], Sin[angle]} + RandomReal[{-0.12, 0.12}, 2],
    {angle, 0, 2 Pi - 2 Pi/36, 2 Pi/36}
];

trainingData = Join[
    (# -> "Inner") & /@ innerPoints,
    (# -> "Outer") & /@ outerPoints
];

classifier = Classify[
    trainingData,
    Method -> "NeuralNetwork"
];

testPoints = {
    {0.2, 0.3},
    {1.8, 0.2},
    {-0.4, -0.5},
    {-1.6, 1.1}
};

Print["Predicted classes: ", classifier /@ testPoints];
Print[
    "Prediction probabilities: ",
    classifier[#, "Probabilities"] & /@ testPoints
];

featurePlot = FeatureSpacePlot[
    trainingData,
    PlotTheme -> "Detailed",
    PlotLabel -> "Concentric training examples",
    ImageSize -> Large
];

featurePlot
