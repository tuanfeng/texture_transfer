function [ ] = polygon_mask( im_name,mask_name,flag,iter )

Im = imread(im_name);
dsp = Im;
imshow(dsp)
new=Im;
mask=Im;
for i=1:size(Im,1)
    for j=1:size(Im,2)
            new(i,j,:)=[255 0 0];
            mask(i,j,:)=[0 0 0];
    end
end

for it = 1:iter

x=[];y=[];
i=1;
while (1);
    [x(i),y(i)]=ginput(1);
    if y(i)<0 || x(i)<0 ; break; else
        if y(i)>size(Im,1)
            y(i)=size(Im,1);
        end
        if x(i)>size(Im,2)
            x(i)=size(Im,2);
        end
            
        for p=-3:3
            for q=-3:3
        dsp(fix(y(i)+p),fix(x(i)+q),:)=[0 255 0];
            end
        end
        imshow(dsp)
        i=i+1;
    end;
end;

BW = roipoly(Im,x(1:i-1),y(1:i-1));

for i=1:size(Im,1)
    for j=1:size(Im,2)
        if BW(i,j)==flag 
            new(i,j,:)=Im(i,j,:);
            mask(i,j,:)=[255 255 255];
       
        end
    end
end

end
subplot(1,2,1), imshow(new)
subplot(1,2,2), imshow(mask);
imwrite(mask,mask_name);
%imwrite(mask,mask_name);

end

