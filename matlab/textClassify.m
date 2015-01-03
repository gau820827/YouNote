function probMap = textClassify(img,model)
if size(img,3) == 3
    img = rgb2gray(img);
end
tmpImg = [zeros(17-1+size(img,1),8),[zeros(8,size(img,2));img;zeros(8,size(img,2))],zeros(17-1+size(img,1),8)];
regions = zeros(size(img,1)*size(img,2),17*17);
for i = 1:size(img,1)
    for j = 1:size(img,2)
        block = double(tmpImg((i+8)-8:i+8+8,j+8-8:j+8+8));
        if(i+(j-1)*size(img,1) > size(regions,1))
            fprintf('error size = %d i = %d j = %d i*(j-1)*size(img,1) = %d\n',size(regions,1),i,j,i+(j-1)*size(img,1));
        end
        regions(i+(j-1)*size(img,1),:) = reshape(block,1,numel(block));
    end
end
[predictedLabels, acc, probMap] = svmpredict(zeros(size(regions,1),1),regions,model);
probMap = reshape(probMap,size(img,1),size(img,2));