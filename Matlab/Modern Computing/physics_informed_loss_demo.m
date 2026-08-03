% PHYSICS_INFORMED_LOSS_DEMO Balance data evidence and an ODE residual.

time = linspace(0, 3, 151)';
measurementTime = [0; 0.6; 1.4; 2.2; 3.0];
trueRate = 1.0;
trueSolution = exp(-trueRate * time);
measurementNoise = [0; 0.08; 0.06; 0.04; 0.03];
measurements = exp(-trueRate * measurementTime) + measurementNoise;

candidateRates = linspace(0.5, 1.4, 181)';
dataLosses = zeros(size(candidateRates));
physicsLosses = zeros(size(candidateRates));

for index = 1:numel(candidateRates)
    rate = candidateRates(index);
    predictedMeasurements = exp(-rate * measurementTime);
    prediction = exp(-rate * time);
    predictionDerivative = -rate * prediction;
    odeResidual = predictionDerivative + prediction;

    dataLosses(index) = mean((predictedMeasurements - measurements).^2);
    physicsLosses(index) = mean(odeResidual.^2);
end

physicsWeight = 0.4;
combinedLosses = dataLosses + physicsWeight * physicsLosses;

[~, dataOnlyIndex] = min(dataLosses);
[~, combinedIndex] = min(combinedLosses);
dataOnlyRate = candidateRates(dataOnlyIndex);
physicsAwareRate = candidateRates(combinedIndex);

fprintf('True rate:              %.3f\n', trueRate);
fprintf('Data-only estimate:     %.3f\n', dataOnlyRate);
fprintf('Physics-aware estimate: %.3f\n', physicsAwareRate);

dataOnlyPrediction = exp(-dataOnlyRate * time);
physicsAwarePrediction = exp(-physicsAwareRate * time);

figure('Name', 'Physics-informed loss intuition');
subplot(1, 2, 1);
plot(time, trueSolution, 'k-', 'LineWidth', 2);
hold on;
plot(measurementTime, measurements, 'o', ...
    'MarkerSize', 7, ...
    'MarkerFaceColor', [0.73, 0.31, 0.24]);
plot(time, dataOnlyPrediction, '--', 'LineWidth', 1.6);
plot(time, physicsAwarePrediction, '-.', 'LineWidth', 1.6);
hold off;
grid on;
xlabel('Time');
ylabel('u(t)');
title('Candidate solutions');
legend('True solution', 'Noisy data', 'Data only', ...
    'Data + physics', 'Location', 'northeast');

subplot(1, 2, 2);
plot(candidateRates, dataLosses, 'LineWidth', 1.6);
hold on;
plot(candidateRates, physicsWeight * physicsLosses, 'LineWidth', 1.6);
plot(candidateRates, combinedLosses, 'k-', 'LineWidth', 2);
xline(trueRate, ':', 'True rate', 'LineWidth', 1.4);
hold off;
grid on;
xlabel('Candidate rate');
ylabel('Loss');
title('Data and physics losses');
legend('Data loss', 'Weighted physics loss', ...
    'Combined loss', 'Location', 'northwest');
