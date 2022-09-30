#define PI 3.14159f


/// kernel for copying an image
/// This kernel may be modified in order to get filter coefficients. Do not forget to modify the
/// calling function and specify the parameters
///
/// imageInput:  pointer to image data
/// imageOutput: pointer to image result
/// width:       dimension of image
/// height:      dimension of image



int index(int x, int y,int width)
{
	int rowOffset = y * width * 4;
	int index = rowOffset + x * 4;
	return index;
}



kernel void copy_image(__global const unsigned char *imageInput,
		       __global       unsigned char *imageOutput, __global const float*coef,
		       int width, int height, int F) 
{
  // Get the index of the current element to be processed
  int2 coord = (int2)(get_global_id(0), get_global_id(1));
  float a = PI;

  // associate a pixel of the image with a work-item: this is done with the computation of index
  // pay attention : RGBa data is stored, this implies the use of 4 uchar variables by pixel

  if (coord.x < width && coord.y < height)
    {
	imageOutput[index(coord.x,coord.y,width)] += imageInput[index(coord.x,coord.y,width)];
	imageOutput[index(coord.x,coord.y,width)+1] += imageInput[index(coord.x,coord.y,width)+1];
	imageOutput[index(coord.x,coord.y,width)+2] += imageInput[index(coord.x,coord.y,width)+2];
	imageOutput[index(coord.x,coord.y,width)+3] += imageInput[index(coord.x,coord.y,width)+3];     
    }
}

/*
kernel void mean_convo(__global const uchar4 *imageInput,
		       __global       uchar4 *imageOutput,
		       int width, int height) {
	int voisinage = 3/2;
	// Get the index of the current element to be processed
	int2 coord = (int2)(get_global_id(0), get_global_id(1));

	if (coord.x > voisinage && coord.x < width - voisinage && coord.y > voisinage && coord.y < height - voisinage){
		float4 sum = (float4)0.0;
		for (int i = -voisinage; i<=voisinage ;i++){
			for(int j = -voisinage; j<=voisinage; j++){
				sum += convert_float4(imageInput[index(coord.x+i,coord.y+j,width)]);
			}
        }
        float4 mean =  sum / (voisinage*2+1)*(voisinage*2+1);
		imageOutput[index(coord.x,coord.y,width)] = convert_uchar4(mean);
	}
}
*/
kernel void filtermean(__global const unsigned char *imageInput,
		       __global unsigned char *imageOutput, __global const float*coef,
		       int width, int height, int F) 
{
 	// Get the index of the current element to be processed
 	int2 coord = (int2)(get_global_id(0), get_global_id(1));

  	// associate a pixel of the image with a work-item: this is done with the computation of index
 	// pay attention : RGBa data is stored, this implies the use of 4 uchar variables by pixel
  	int rowOffsetmi = (coord.y) * 4*width;
 	int indexmi = rowOffsetmi + 4*coord.x;
  	//Initializing mean with the centra value of the window/box
  	float mean0 = 0.0;
  	float mean1 = 0.0; 
  	float mean2 = 0.0; 
  	float mean3 = 0.0; 

  	if (coord.x > 4*F && coord.x < width - 4*F && coord.y > 4*F && coord.y < height - 4*F){
		for (int i = -F; i <= F; i++){ 
			for (int j = -F; j <= F; j++){
				//on récupère la valeur des pixels autour 
				int rowOffset = (coord.y + j) * 4*width;
 				int index = rowOffset + 4*(coord.x + i);
 				mean0 += convert_float(imageInput[index]);
 				mean1 += convert_float(imageInput[index+1]);
 				mean2 += convert_float(imageInput[index+2]);
 				mean3 += convert_float(imageInput[index+3]);
					
			}
		}
		mean0/=(4*F*F + 4*F +1);
		mean1/=(4*F*F + 4*F +1);
		mean2/=(4*F*F + 4*F +1);
		mean3/=(4*F*F + 4*F +1); 
		imageOutput[indexmi] = convert_char(mean0);
		imageOutput[indexmi + 1] = convert_char(mean1);
		imageOutput[indexmi + 2] = convert_char(mean2);
		imageOutput[indexmi + 3] = convert_char(mean3); 			

	}
	else{
		imageOutput[indexmi] = imageInput[indexmi];
		imageOutput[indexmi + 1] = imageInput[indexmi + 1]; 
		imageOutput[indexmi + 2] = imageInput[indexmi + 2]; 
		imageOutput[indexmi + 3] = imageInput[indexmi + 3]; 
	}			

}


kernel void filtermeanimproved(__global const uchar4 *imageInput,
		       __global       uchar4 *imageOutput,__global const float*coef,
		       int width, int height, int F) 
{
 	// Get the index of the current element to be processed
 	int2 coord = (int2)(get_global_id(0), get_global_id(1));
  	float a = PI;

  	// associate a pixel of the image with a work-item: this is done with the computation of index
 	// pay attention : RGBa data is stored, this implies the use of 4 uchar variables by pixel
  	int rowOffsetmi = (coord.y) * width;
 	int indexmi = rowOffsetmi + coord.x;
  	//Initializing mean with the centra value of the window/box
  	float4 mean = (float4)0.0; 

  	if (coord.x > F && coord.x < width - F && coord.y > F && coord.y < height - F){
		for (int i = -F; i <= F; i++){ //jusque height - 2 inclu
			for (int j = -F; j <= F; j++){
				//on récupère la valeur des pixels autour 
				int rowOffset = (coord.y + j) * width;
 				int index = rowOffset + (coord.x + i);
 				mean += convert_float4(imageInput[index]);
					
			}
		}
		mean/=(4*F*F + 4*F +1); 
		imageOutput[indexmi] = convert_uchar4(mean); 			

	}
	else{
		imageOutput[indexmi] = imageInput[indexmi]; 
	}			

}

/*
kernel void filtergaussianEr(__global const uchar4 *imageInput,
		       __global       uchar4 *imageOutput,
		       int width, int height) 
{
	int taille = 1;
 	// Get the index of the current element to be processed
 	int2 coord = (int2)(get_global_id(0), get_global_id(1));
  	float a = PI;
  	float sigma = 1;
  	float preExp = 1/sqrt(2*a*sigma);
  	float coef;

	int voisin;
	int indexvar;

  	// associate a pixel of the image with a work-item: this is done with the computation of index
 	// pay attention : RGBa data is stored, this implies the use of 4 uchar variables by pixel
 	indexvar = index(coord.x,coord.y,width);
  	//Initializing mean with the centra value of the window/box
  	float4 sum = (float4)0.0; 
  	float4 norm = (float4)0.0;

  	if (coord.x > taille && coord.x < width - taille && coord.y > taille && coord.y < height - taille){
		for (int i = -taille; i <= taille; i++){ //jusque height - 2 inclu
			for (int j = -taille; j <= taille; j++){
				//on récupère la valeur des pixels autour 
				coef = preExp * exp(-(i*i+j*j)/(2*sigma*sigma));
				voisin = index(coord.x+i,coord.y+j,width);
 				sum += coef * convert_float4(imageInput[voisin]);
 				norm += coef;
			}
		}
	sum = convert_float4(sum/norm);
	imageOutput[indexvar] = convert_uchar4(sum); 			

	}
	else{
	imageOutput[indexvar] = imageInput[indexvar]; 
	}			

}

*/
kernel void filtergaussian(__global const uchar4 *imageInput,
		       __global       uchar4 *imageOutput,__global const float*coef,
		       int width, int height, int F) 
{	
	float sigma = 3*F; 
 	// Get the index of the current element to be processed
 	int2 coord = (int2)(get_global_id(0), get_global_id(1));
  	float a = PI;

  	// associate a pixel of the image with a work-item: this is done with the computation of index
 	// pay attention : RGBa data is stored, this implies the use of 4 uchar variables by pixel
  	int rowOffsetmi = (coord.y) * width;
 	int indexmi = rowOffsetmi + coord.x;
  	//Initializing mean with the centra value of the window/box
  	float4 gaussian = (float4)0.0; 
  	float normalization = 0.0; 

  	if (coord.x > F && coord.x < width - F && coord.y > F && coord.y < height - F){
		for (int i = -F; i <= F; i++){ //jusque height - 2 inclu
			for (int j = -F; j <= F; j++){
				//on récupère la valeur des pixels autour 
				int rowOffset = (coord.y + j) * width;//j+m
 				int index = rowOffset + (coord.x + i);//i+l
 				//gaussian factor 
 				gaussian += (1/sqrt(2*a*sigma*sigma))*exp(-(i*i+j*j)/(2*sigma*sigma))*convert_float4(imageInput[index]);
				normalization += (1/sqrt(2*a*sigma*sigma))*exp(-(i*i+j*j)/(2*sigma*sigma)); 
			}
		}
		gaussian/=normalization; 
		imageOutput[indexmi] = convert_uchar4(gaussian); 			

	}
	else{
	imageOutput[indexmi] = imageInput[indexmi]; 
	}			

}

kernel void filtergaussianimproved(__global const uchar4 *imageInput,
		       __global       uchar4 *imageOutput, __global const float*coef,int width, int height, int F) 
{
 	// Get the index of the current element to be processed
 	int2 coord = (int2)(get_global_id(0), get_global_id(1));
  	float a = PI;

  	// associate a pixel of the image with a work-item: this is done with the computation of index
 	// pay attention : RGBa data is stored, this implies the use of 4 uchar variables by pixel
  	int rowOffsetmi = (coord.y) * width;
 	int indexmi = rowOffsetmi + coord.x;
  	
  	float4 gaussian = (float4)0.0;  
  	float test = 0.0;

  	if (coord.x > F && coord.x < width - F && coord.y > F && coord.y < height - F){
		for (int i = -F; i <= F; i++){ //jusque height - 2 inclu
			for (int j = -F; j <= F; j++){
				//on récupère la valeur des pixels autour 
				int rowOffset = (coord.y + j) * width;//j+m
 				int index = rowOffset + (coord.x + i);//i+l
 				//gaussian factor 
 				gaussian += coef[abs(i)]*coef[abs(j)]*convert_float4(imageInput[index]); 
			}
		}  
		imageOutput[indexmi] = convert_uchar4(gaussian); 			
	}
	else{
		imageOutput[indexmi] = imageInput[indexmi]; 
	}			

}







