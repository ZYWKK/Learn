(* Build a data loss and an ODE residual with symbolic calculus. *)

ClearAll[t, rate, candidate];

candidate[t_] := Exp[-rate t];
odeResidual = FullSimplify[D[candidate[t], t] + candidate[t]];
physicsLoss = FullSimplify[
    Integrate[odeResidual^2, {t, 0, 3}],
    Assumptions -> rate > 0
];

measurements = {
    {0.0, 1.0},
    {0.6, 0.6288},
    {1.4, 0.3066},
    {2.2, 0.1508},
    {3.0, 0.0798}
};

dataLoss = Mean[
    (candidate[#[[1]]] - #[[2]])^2 & /@ measurements
];
physicsWeight = 0.4;
combinedLoss = dataLoss + physicsWeight physicsLoss;

dataOnlyResult = NMinimize[
    {dataLoss, 0.5 <= rate <= 1.4},
    rate
];
physicsAwareResult = NMinimize[
    {combinedLoss, 0.5 <= rate <= 1.4},
    rate
];

dataOnlyRate = rate /. Last[dataOnlyResult];
physicsAwareRate = rate /. Last[physicsAwareResult];

Print["Symbolic ODE residual: ", odeResidual];
Print["Symbolic physics loss: ", physicsLoss];
Print["Data-only rate: ", N[dataOnlyRate, 5]];
Print["Physics-aware rate: ", N[physicsAwareRate, 5]];

lossPlot = Plot[
    Evaluate[{dataLoss, physicsWeight physicsLoss, combinedLoss}],
    {rate, 0.5, 1.4},
    PlotLegends -> {"Data loss", "Weighted physics loss", "Combined loss"},
    AxesLabel -> {"rate", "loss"},
    PlotLabel -> "Data evidence and physics constraint",
    ImageSize -> Large
];

lossPlot
