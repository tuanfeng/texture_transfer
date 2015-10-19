//////////////////////////////////////////////////////////////////////////////
// Example illustrating the use of GCoptimization.cpp
//   complie g++ mystart.cpp GCoptimization.cpp LinkedBlockList.cpp -o main
/////////////////////////////////////////////////////////////////////////////
//
//  Optimization problem:
//  is a set of sites (pixels) of width 10 and hight 5. Thus number of pixels is 50
//  grid neighborhood: each pixel has its left, right, up, and bottom pixels as neighbors
//  7 labels
//  Data costs: D(pixel,label) = 0 if pixel < 25 and label = 0
//            : D(pixel,label) = 10 if pixel < 25 and label is not  0
//            : D(pixel,label) = 0 if pixel >= 25 and label = 5
//            : D(pixel,label) = 10 if pixel >= 25 and label is not  5
// Smoothness costs: V(p1,p2,l1,l2) = min( (l1-l2)*(l1-l2) , 4 )
// Below in the main program, we illustrate different ways of setting data and smoothness costs
// that our interface allow and solve this optimizaiton problem

// For most of the examples, we use no spatially varying pixel dependent terms. 
// For some examples, to demonstrate spatially varying terms we use
// V(p1,p2,l1,l2) = w_{p1,p2}*[min((l1-l2)*(l1-l2),4)], with 
// w_{p1,p2} = p1+p2 if |p1-p2| == 1 and w_{p1,p2} = p1*p2 if |p1-p2| is not 1

#include <iostream>
#include <fstream>

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <vector>
#include <math.h>

#include "GCoptimization.h"

int dim_x,dim_y,num_l,num_p;
struct pix_struct{
	int r,g,b,l,p;
};
struct p2d{
	int x,y;
};

std::vector<std::vector<pix_struct> > img;
std::vector<p2d> offset;
std::vector<p2d> neighs;
std::vector<p2d> pixs;


struct ForDataFn{
	int numLab;
	int *data;
};

int inf_ = 200000;

int smoothFn(int p1, int p2, int l1, int l2)
{
	//if ( (l1-l2)*(l1-l2) <= 4 ) return((l1-l2)*(l1-l2));
	//else return(4);

	int loc_1x=pixs[p1].x;
	int loc_1y=pixs[p1].y;
	int loc_2x=pixs[p2].x;
	int loc_2y=pixs[p2].y;
	int off_1x=offset[l1].x;
	int off_1y=offset[l1].y;
	int off_2x=offset[l2].x;
	int off_2y=offset[l2].y;

	int r11,g11,b11,r12,g12,b12,r21,g21,b21,r22,g22,b22;
	int tr = 0;

	if ((loc_1x+off_1x<0) || (loc_1x+off_1x>=dim_x) || (loc_1y+off_1y<0) || (loc_1y+off_1y>=dim_y)){
		r11=tr;
		g11=tr;
		b11=tr;
	} else {
		r11=img[loc_1x+off_1x][loc_1y+off_1y].r;
		g11=img[loc_1x+off_1x][loc_1y+off_1y].g;
		b11=img[loc_1x+off_1x][loc_1y+off_1y].b;
	}


	if ((loc_1x+off_2x<0) || (loc_1x+off_2x>=dim_x) || (loc_1y+off_2y<0) || (loc_1y+off_2y>=dim_y)){
		r12=tr;
		g12=tr;
		b12=tr;
	} else {
		r12=img[loc_1x+off_2x][loc_1y+off_2y].r;
		g12=img[loc_1x+off_2x][loc_1y+off_2y].g;
		b12=img[loc_1x+off_2x][loc_1y+off_2y].b;
	}
	if ((loc_2x+off_1x<0) || (loc_2x+off_1x>=dim_x) ||  (loc_2y+off_1y<0) || (loc_2y+off_1y>=dim_y)){
		r21=tr;
		g21=tr;
		b21=tr;
	} else {
		r21=img[loc_2x+off_1x][loc_2y+off_1y].r;
		g21=img[loc_2x+off_1x][loc_2y+off_1y].g;
		b21=img[loc_2x+off_1x][loc_2y+off_1y].b;
	}

	if ((loc_2x+off_2x<0) || (loc_2x+off_2x>=dim_x) || (loc_2y+off_2y<0) || (loc_2y+off_2y>=dim_y)){
		r22=tr;
		g22=tr;
		b22=tr;
	} else {
		r22=img[loc_2x+off_2x][loc_2y+off_2y].r;
		g22=img[loc_2x+off_2x][loc_2y+off_2y].g;
		b22=img[loc_2x+off_2x][loc_2y+off_2y].b;
	}


	int t1=0;
	t1 += abs(r11-r12);//*(r11-r12);
	t1 += abs(g11-g12);//*(g11-g12);
	t1 += abs(b11-b12);//*(b11-b12);
	int t2=0;
	t2 += abs(r21-r22);//*(r21-r22);
	t2 += abs(g21-g22);//*(g21-g22);
	t2 += abs(b21-b22);//*(b21-b22);

/*
	std::cout<<"-----"<<p1<<' '<<p2<<' '<<l1<<' '<<l2<<'\n';
	std::cout<<r11<<' '<<r12<<' '<<r21<<' '<<r22<<'\n';
	std::cout<<g11<<' '<<g12<<' '<<g21<<' '<<g22<<'\n';
	std::cout<<b11<<' '<<b12<<' '<<b21<<' '<<b22<<'\n';
	std::cout<<t1<<' '<<t2<<' '<<t1+t2<<'\n';
*/

	return t1+t2;//int(sqrt(double(t1))+sqrt(double(t2)));

}


////////////////////////////////////////////////////////////////////////////////
// in this version, set data and smoothness terms using arrays
// grid neighborhood is set up "manually"
//
void GeneralGraph_DArraySArray(int num_pixels,int num_labels)
{



	int *result = new int[num_pixels];   // stores result of optimization

	// first set up the array for data costs
	int *data = new int[num_pixels*num_labels];
	int pcot = 0;
	//std::cout<<offset[num_labels-1].x<<' '<<offset[num_labels-1].x<<'\n';
	for ( int i = 0; i < num_pixels; i++ ){
		int flag = 0;
		for (int l = 0; l < num_labels; l++ ){
			int loc_1=pixs[i].x;
			int loc_2=pixs[i].y;
			int off_1=offset[l].x;
			int off_2=offset[l].y;
			if ((loc_1+off_1<0) || (loc_1+off_1>=dim_x) || (loc_2+off_2<0) || (loc_2+off_2>=dim_y)){
				data[i*num_labels+l] = inf_;
			} else{
				int loc_n1=loc_1+off_1;
				int loc_n2=loc_2+off_2;
				int regl = img[loc_n1][loc_n2].l;
				int regl_ = img[loc_1][loc_2].l;
				if (regl_==1) {
					if (l==num_labels-1) {
						data[i*num_labels+l] = 0;
						flag = 1;
					} else {
						data[i*num_labels+l] = inf_;
					}
				} else {
					if ((regl == 0) || (regl == 1)){
						data[i*num_labels+l] = 0;
						flag = 1;
					} else {
						data[i*num_labels+l] = inf_;
					}
				}
			}
		}
		if (flag == 0) {pcot += 1;}
	}

	std::cout<<num_pixels<<' '<<pcot<<'\n';
		
	// next set up the array for smooth costs
	//int *smooth = new int[num_labels*num_labels];
	//for ( int l1 = 0; l1 < num_labels; l1++ )
	//	for (int l2 = 0; l2 < num_labels; l2++ )
	//		smooth[l1+l2*num_labels] = (l1-l2)*(l1-l2) <= 4  ? (l1-l2)*(l1-l2):4;


	try{
		GCoptimizationGeneralGraph *gc = new GCoptimizationGeneralGraph(num_pixels,num_labels);
		gc->setDataCost(data);
		gc->setSmoothCost(&smoothFn);

		// now set up a grid neighborhood system
		// first set up horizontal neighbors

		for (int i=0;i<neighs.size();i++){
			//printf("-- %d -- %d -- %d\n",num_pixels,neighs[i].x,neighs[i].y);
			gc->setNeighbors(neighs[i].x,neighs[i].y);
		}

		//for (int y = 0; y < height; y++ )
		//	for (int  x = 1; x < width; x++ )
		//		gc->setNeighbors(x+y*width,x-1+y*width);

		// next set up vertical neighbors
		//for (int y = 1; y < height; y++ )
		//	for (int  x = 0; x < width; x++ )
		//		gc->setNeighbors(x+y*width,x+(y-1)*width);

		printf("\nBefore optimization energy is %d",gc->compute_energy());
		gc->expansion(40);// run expansion for 2 iterations. For swap use gc->swap(num_iterations);
		printf("\nAfter optimization energy is %d",gc->compute_energy());

		for ( int  i = 0; i < num_pixels; i++ )
			result[i] = gc->whatLabel(i);


		std::ofstream fou;
		fou.open("./tmp_2");

		for (int i=0; i<num_pixels;i++){
			fou<<pixs[i].x<<' '<<pixs[i].y<<' '<<offset[result[i]].x<<' '<<offset[result[i]].y<<'\n';
		}

		fou.close();


		delete gc;
	}
	catch (GCException e){
		e.Report();
	}

	delete [] result;
	//delete [] smooth;
	delete [] data;

}

int main(int argc, char **argv)
{

	std::ifstream fin;
	fin.open("./tmp_1");
	fin >> dim_x >> dim_y >> num_l;

	img.clear();
	pixs.clear();
	offset.clear();
	neighs.clear();
	
	num_p=0;

	for (int i=0;i<dim_x;i++){
		std::vector<pix_struct> tmpix;
		tmpix.clear();
		for (int j=0;j<dim_y;j++){
			pix_struct tp;
			fin>>tp.r>>tp.g>>tp.b>>tp.l;
			if ((tp.l == 1) || (tp.l == 2)){
				tp.p = num_p;
				p2d tmpp;
				tmpp.x=i;
				tmpp.y=j;
				pixs.push_back(tmpp);
				num_p += 1;				
				if ((j>0) && ((tmpix[j-1].l == 1) || (tmpix[j-1].l ==2))) {
					p2d tmpoff;
					tmpoff.x=tmpix[j-1].p;
					tmpoff.y=tp.p;
					neighs.push_back(tmpoff);
				}
				if ((i>0) && ((img[i-1][j].l == 1) || (img[i-1][j].l ==2))) {
					p2d tmpoff;
					tmpoff.x=img[i-1][j].p;
					tmpoff.y=tp.p;
					neighs.push_back(tmpoff);
				}
				//if (neighs.size() == 1){
				//	std::cout<<i<<' '<<j<<' '<<tmpix[232].p<<'\n';
				//}
			} else {
				tp.p = -1;
			}
			tmpix.push_back(tp);
		}
		img.push_back(tmpix);
	}

	for (int i=0;i<num_l;i++){
		p2d tmpoff;
		fin>>tmpoff.x>>tmpoff.y;
		offset.push_back(tmpoff);
	}

	num_l += 1;

	p2d tmpoff;
	tmpoff.x=0;tmpoff.y=0;
	offset.push_back(tmpoff);

	fin.close();


	GeneralGraph_DArraySArray(num_p,num_l);
	
	printf("\n  Finished %d (%d) clock per sec %d\n",clock()/CLOCKS_PER_SEC,clock(),CLOCKS_PER_SEC);

	return 0;
}

/////////////////////////////////////////////////////////////////////////////////

