#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <math.h>
#include <vector>
#include <random>
#include <ctime>

#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

int main( int argc, char** argv )
{
    std::clock_t time_start;
    time_start = std::clock();

    Mat src, src_gray;
    Mat dst, detected_edges;

//    int edgeThresh = 1;
    int lowThreshold;
    int ratio = 3;
    int kernel_size = 3;

    /// Load an image
    src = imread( argv[1] );
    std::string file_string = argv[1];

    Size tmp_size(400,400);
    resize(src,src,tmp_size);//resize image

    if( !src.data )
    { return -1; }

    /// Create a matrix of the same type and size as src (for dst)
    //dst.create( src.size(), src.type() );

    /// Convert the image to grayscale
    cvtColor( src, src_gray, CV_BGR2GRAY );

    blur( src_gray, detected_edges, Size(3,3) );

    lowThreshold = 30;

    /// Canny detector
    Canny( detected_edges, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size );

    /// Using Canny's output as a mask, we display our result

    imwrite(file_string.substr(0,file_string.length()-4)+"_output_1.png",detected_edges);

    Mat out2;
    out2.create( src.size(), detected_edges.type());

    detected_edges.copyTo(out2);

    int radius = 2;
    for (int i=0; i<detected_edges.size().height; i++){
        for (int j=0; j<detected_edges.size().width; j++){
            if (detected_edges.at<uchar>(i,j) == 255) {
                for (int pi=-radius; pi<=radius; pi++){
                    for (int pj=-radius; pj<=radius; pj++){
                        float dis = sqrt(pi*pi+pj*pj);
                        if ((dis<=radius) && (i+pi>=0) && (i+pi<detected_edges.size().height) && (j+pj>=0) && (j+pj<detected_edges.size().width)) {
                            uchar pv=(uchar)(255-dis/(float)(radius+1)*255);
                            if (pv>out2.at<uchar>(i+pi,j+pj)) {
                                out2.at<uchar>(i+pi,j+pj) = pv;
                            }
                        }
                    }
                }
            }
        }
    }
    imwrite(file_string.substr(0,file_string.length()-4)+"_output_2.png",out2);

    Mat out3(out2.size(), CV_32S, Scalar::all(0));

    int patch_dx = 80;
    int patch_dy = 80;
    int patch_locx,patch_locy;

    //check
    if (1>0) {

        Mat out_tmp(src.size(),src.type());
        Mat out_t2(src.size(),CV_32S, Scalar::all(10000));


        int patch_locx = 200;
        int patch_locy = 200;

        double minerr = 100000000;

        Mat target_patch = out2.colRange(patch_locx,patch_locx+patch_dx).rowRange(patch_locy,patch_locy+patch_dy);

        for (int i=0; i<out2.size().width-patch_dx; i+=1){
            for (int j=0; j<out2.size().height-patch_dy; j+=1){
                if ((i-patch_locx)*(i-patch_locx)+(j-patch_locy)*(j-patch_locy)>=50) {
                    Mat current_patch = out2.colRange(i,i+patch_dx).rowRange(j,j+patch_dy);
                    Mat diff = target_patch-current_patch;
                    double diff_norm = norm(diff);
                    //if (diff_norm<1500) {
                    //    std::cout<<'*';
                    //    out_tmp.at<Vec3b>(j,i)[0] = 0;
                    //    out_tmp.at<Vec3b>(j,i)[1] = 0;
                    //    out_tmp.at<Vec3b>(j,i)[2] = 255;
                    //}
                    if (diff_norm < minerr) {
                        minerr = diff_norm;
                    }
                    out_t2.at<int>(j,i) = diff_norm;
                    if (out_t2.at<int>(j,i) > 10000) {
                        out_t2.at<int>(j,i) = 10000;
                    }

                }

            }
        }

        normalize(out_t2,out_t2,0,255,NORM_MINMAX);

        for (int i=0; i<out2.size().width; i+=1){
            for (int j=0; j<out2.size().height; j+=1){
                out_tmp.at<Vec3b>(i,j)[0] = 0;
                out_tmp.at<Vec3b>(i,j)[1] = 0;
                out_tmp.at<Vec3b>(i,j)[2] = 255-out_t2.at<int>(i,j);
            }
        }

        for (int i=-2; i<3; i++){
            for (int j=-2; j<3; j++){
                out_tmp.at<Vec3b>(patch_locx+i,patch_locy+j)[0]=0;
                out_tmp.at<Vec3b>(patch_locx+i,patch_locy+j)[1]=255;
                out_tmp.at<Vec3b>(patch_locx+i,patch_locy+j)[2]=0;

            }
        }


        std::cout<<minerr<<" check done\n";

        imwrite(file_string.substr(0,file_string.length()-4)+"_output_check.png",out_tmp);

    }
    //checkend///////////




    Mat mark_patch (patch_dx,patch_dy,CV_32S,Scalar::all(1));

    //Mat gre_patch (5,5,src.type(),Scalar(0, 255, 0));
    //Mat red_patch (5,5,src.type(),Scalar(0, 0, 255));

    std::vector<Point2i> patch_candi;
    patch_candi.clear();

    //std::cout<<'*'<<int(src.at<Vec3b>(0,0)[0])<<' '<<int(src.at<Vec3b>(0,0)[1])<<' '<<int(src.at<Vec3b>(0,0)[2])<<'\n';

    for (int i=0; i<out2.size().width-patch_dx; i+=1){
        for (int j=0; j<out2.size().height-patch_dy; j+=1){
            Point2i tmp_loc;
            tmp_loc.y=i;
            tmp_loc.x=j;
            bool flag = true;
            for (int pi=0; pi<patch_dx; pi+=20){
                for (int pj=0; pj<patch_dy; pj+=20){
                    if (((src.at<Vec3b>(i+pi,j+pj)[1] == 255) && (src.at<Vec3b>(i+pi,j+pj)[2] == 0) && (src.at<Vec3b>(i+pi,j+pj)[0] == 0))
                            || ((src.at<Vec3b>(i+pi,j+pj)[1] == 0) && (src.at<Vec3b>(i+pi,j+pj)[2] == 255) && (src.at<Vec3b>(i+pi,j+pj)[0] == 0))){
                        flag = false;
                        break;
                    }
                }
                if (!flag) {
                    break;
                }
            }
            if (flag) {
                patch_candi.push_back(tmp_loc);
                //src.at<Vec3b>(i,j)[0]=255;
                //src.at<Vec3b>(i,j)[1]=255;
                //src.at<Vec3b>(i,j)[2]=255;

            }
        }
    }

    //imwrite(file_string.substr(0,file_string.length()-4)+"_output_tmp.png",src);

    std::vector<Point2i> patch_list;
    patch_list.clear();

    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);
    std::uniform_real_distribution<double> distribution(0.0,1.0);
    double ratio_select = double(5000)/double(patch_candi.size());

    std::cout<<"patch candidates size: "<<patch_candi.size()<<'\n';

    for (int i=0; i<patch_candi.size(); i+=1){
        double number = distribution(generator);
        if (number<=ratio_select){
            patch_list.push_back(patch_candi[i]);
            Point2i tmp;
            tmp = patch_list.back();
            src.at<Vec3b>(tmp.y+patch_dy/2,tmp.x+patch_dx/2)[0]=255;
            src.at<Vec3b>(tmp.y+patch_dy/2,tmp.x+patch_dx/2)[1]=255;
            src.at<Vec3b>(tmp.y+patch_dy/2,tmp.x+patch_dx/2)[2]=255;
        }
    }
    imwrite(file_string.substr(0,file_string.length()-4)+"_output_tmp.png",src);

    //std::cout<<patch_list[0].x<<' '<<patch_list[0].y<<'\n';

    std::cout<<"patch list size: "<<patch_list.size()<<'\n';
    int count = 0;
    for (int idx1=0;idx1<patch_list.size()-1; idx1++){
        patch_locx = patch_list[idx1].x;
        patch_locy = patch_list[idx1].y;
        Mat target_patch = out2.colRange(patch_locx,patch_locx+patch_dx).rowRange(patch_locy,patch_locy+patch_dy);
        Mat target_patch_3 = out3.colRange(patch_locx,patch_locx+patch_dx).rowRange(patch_locy,patch_locy+patch_dy);

        for (int idx2=idx1+1; idx2<patch_list.size(); idx2++){
            int i = patch_list[idx2].x;
            int j = patch_list[idx2].y;
            Mat current_patch = out2.colRange(i,i+patch_dx).rowRange(j,j+patch_dy);
            Mat diff = target_patch-current_patch;
            double diff_norm = norm(diff);
            if ((diff_norm<2000) && ((i-patch_locx)*(i-patch_locx)+(j-patch_locy)*(j-patch_locy)>50)) {
                count++;
                //std::cout<<idx1<<' '<<idx2<<' '<<i<<' '<<j<<' '<<patch_locx<<' '<<patch_locy<<'\n';
                Mat current_patch_3 = out3.colRange(i,i+patch_dx).rowRange(j,j+patch_dy);
                Mat new_current_patch_3 = current_patch_3 + mark_patch;
                new_current_patch_3.copyTo(current_patch_3);
                Mat new_target_patch_3 = target_patch_3 + mark_patch;
                new_target_patch_3.copyTo(target_patch_3);
                //Mat out_tmp;
                //out3.convertTo(out_tmp, CV_8U);
                //imwrite(file_string.substr(0,file_string.length()-4)+"_output_3.png",out_tmp);
                //if (count%100 == 0)  {std::cin.ignore();}
            }
        }
    }
    std::cout<<count<<'\n';
    double minval,maxval;
    Point2i minLoc,maxLoc;
    cv::minMaxLoc(out3,&minval,&maxval, &minLoc, &maxLoc );
    std::cout<<minval<<' '<<maxval<<'\n';
    normalize(out3,out3,0,255,NORM_MINMAX);

    out3.convertTo(out3, CV_8U);
    imwrite(file_string.substr(0,file_string.length()-4)+"_output_3.png",out3);

    for (int i=0; i<out3.size().height; i+=1){
        for (int j=0; j<out3.size().width; j+=1){
            if (out3.at<uchar>(i,j)<100) {
                out3.at<uchar>(i,j) = 0;
            } else {
                out3.at<uchar>(i,j) = 255;
            }
        }
    }
    imwrite(file_string.substr(0,file_string.length()-4)+"_output_4.png",out3);

    std::cout << "Time: " << (std::clock() - time_start) / (double)(CLOCKS_PER_SEC) << " s" << std::endl;

    return 0;
}

