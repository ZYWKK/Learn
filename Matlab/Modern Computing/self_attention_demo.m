% SELF_ATTENTION_DEMO Explain causal scaled dot-product attention.

rng(7);

tokens = {'learn', 'modern', 'ai', 'safely'};
embeddings = [
    1.0, 0.2, 0.1, 0.0;
    0.1, 1.0, 0.3, 0.2;
    0.0, 0.4, 1.0, 0.8;
    0.3, 0.1, 0.5, 1.0
];

embeddingDimension = size(embeddings, 2);
queryWeight = randn(embeddingDimension) / sqrt(embeddingDimension);
keyWeight = randn(embeddingDimension) / sqrt(embeddingDimension);
valueWeight = randn(embeddingDimension) / sqrt(embeddingDimension);

queries = embeddings * queryWeight;
keys = embeddings * keyWeight;
values = embeddings * valueWeight;

scoreMatrix = queries * keys' / sqrt(embeddingDimension);
causalMask = triu(true(size(scoreMatrix)), 1);
scoreMatrix(causalMask) = -Inf;

stableScores = scoreMatrix - max(scoreMatrix, [], 2);
unnormalizedWeights = exp(stableScores);
attentionWeights = unnormalizedWeights ./ sum(unnormalizedWeights, 2);
contextVectors = attentionWeights * values;

disp('Causal attention weights:');
disp(array2table(attentionWeights, ...
    'VariableNames', tokens, ...
    'RowNames', tokens));

disp('Each row should sum to one:');
disp(sum(attentionWeights, 2));

disp('Context-aware output vectors:');
disp(contextVectors);

figure('Name', 'Causal self-attention');
heatmap(tokens, tokens, attentionWeights, ...
    'Title', 'Causal scaled dot-product attention', ...
    'XLabel', 'Key token', ...
    'YLabel', 'Query token');
