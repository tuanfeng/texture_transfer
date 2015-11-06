img_name = 'img_6.png';
img_o=imread(img_name);
%figure,imshow(img_o);
vl_setup;
img_g = rgb2gray(img_o);
img = single(img_g);
[f,d] = vl_sift(img);% 'PeakThresh', 'edgethresh'
dd = double(d([20,50],:));

bandwidth = 3;
tic
[clustCent,point2cluster,clustMembsCell] = MeanShiftCluster(dd,bandwidth);
toc

if 1>2
    
    figure,imshow(img_g);
    h1 = vl_plotframe(f(:,clustMembsCell{1,1})) ;
    h2 = vl_plotframe(f(:,clustMembsCell{1,1})) ;
    set(h1,'color','k','linewidth',3) ;
    set(h2,'color','y','linewidth',2) ;
     
end