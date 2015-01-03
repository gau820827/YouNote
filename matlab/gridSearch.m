function model = gridSearch(labels, features)
c = -5:5;
g = -5:5;
r = 0;
maxAcc = -inf;
y = randsample(size(features,1),round(size(features,1)*0.7));
trainFeatures = features(y,:);
trainLabels = labels(y);
testFeatures = features(setdiff(1:size(features,1),y),:);
testLabels = labels(setdiff(1:size(features,1),y));
for i = 1:numel(c)
    for j = 1:numel(g)
        for k = 1:numel(r)
            options = ['-t 1 -q -v 5 -c ' num2str(10^c(i)) ' -g ' num2str(10^g(j)) ' -r ' num2str(r(k))];
            tic
            acc = svmtrain(trainLabels,trainFeatures,options);
            toc
            if acc > maxAcc
                maxAcc = acc;
                ind = [i,j,k];
            end
        end
    end
end
options = ['-t 1 -q -c ' num2str(10^c(ind(1))) ' -g ' num2str(10^g(ind(2))) ' -r ' num2str(r(ind(3)))];
model = svmtrain(trainLabels,trainFeatures,options);
[predictedLabels, acc, decisionValue] = svmpredict(testLabels,testFeatures,model,'-q');