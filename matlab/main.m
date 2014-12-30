cd ../data/text
files = ls('./');
textimgs = {};
for i = 3:size(files,1)
    img = imread(files(i,:));
    x = randsample(9:size(img,1)-8,10);
    y = randsample(9:size(img,2)-8,10);
    for j = 1:numel(x)
        textimgs{end+1} = img(x(j)-8:x(j)+8,y(j)-8:y(j)+8);
    end
end
cd ../nontext
files = ls('./');
nontextimgs = {};
for i =3:size(files,1)
    img = imread(files(i,:));
    img = imresize(img,240/size(img,1));
    x = randsample(9:size(img,1)-8,10);
    y = randsample(9:size(img,2)-8,10);
    for j = 1:numel(x)
        nontextimgs{end+1} = img(x(j)-8:x(j)+8,y(j)-8:y(j)+8);
    end
end
cd ../../matlab
addpath ../libsvm-3.20/matlab
features = zeros(numel(textimgs)+numel(nontextimgs),17*17);
labels = zeros(size(features,1),1);
for i = 1:numel(labels)
    if i <= numel(textimgs)
        img = textimgs{i};
        if size(img,3) == 3
            img = rgb2gray(img);
        end
        features(i,:) = reshape(img,1,numel(img));
        labels(i) = 1;
    else
        img = nontextimgs{i-numel(textimgs)};
        if size(img,3) == 3
            img = rgb2gray(img);
        end
        features(i,:) = reshape(img,1,numel(img));
        labels(i) = -1;
    end
end
features = features/256;
model = gridSearch(labels,features);
img = imread('../images.jpg');
%img2 = impyramid(img,'reduce');
probMap = textClassify(img,model);