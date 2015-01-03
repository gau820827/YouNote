function out = myNormalize(in)

mu = sum(sum(in))/numel(in);
temp = (in-mu).^2;
sigma = sqrt(sum(sum(temp))/numel(in));
out = (in-mu)./sigma;