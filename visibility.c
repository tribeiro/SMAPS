//
//  visibility.c
//  SMAPs
//
//  Created by Tiago Ribeiro de Souza on 29/07/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//gcc -c _skysub.c
//gcc _skysub.o  visibility.c

#include <stdio.h>
#include <stdlib.h>
#include "skysub.h"
#include "chealpix.h"

struct params {
	double ra;
	double dec;
	double glat;
	double glong;
	double epoch;
	double sitelat;
	double sitelong;
	double jdstart;
	double jdend;
};

struct inputPar {
	long nside;
	char* fileout;
	double jdstart;
	double days;
};

void readInput(int,char**,void*);
void printHelpPage(void);
void testArg(char*);

int main(int argc, char** argv)
{
	int i,j,len;
	char *outname;
	long Npix;
	double *vis_3, *vis_2, *vis_15;
	float *tot_vis_3,*tot_vis_2,*tot_vis_15;
	struct params fvisPar;
	struct inputPar inpar; 
	
	readInput(argc,argv,&inpar);
	
	/* Number of pixels in the map */
	Npix = nside2npix(inpar.nside);

	/* Start and end time of calculations */
	fvisPar.sitelat = -30.228;
	fvisPar.sitelong = 4.715;
	fvisPar.jdstart = inpar.jdstart;
	fvisPar.jdend = inpar.jdstart + inpar.days;
	
	/* Size of simulation is number of days. Only integer part matters. */
	len = (int)(fvisPar.jdend-fvisPar.jdstart);
	
	/* Allocating memory for visibility calculation and result */
	vis_3 = (double *)malloc(len*sizeof(double)); /* Temporary alocator for season time for each pixel in coordinates */
	vis_2 = (double *)malloc(len*sizeof(double)); /* Temporary alocator for season time for each pixel in coordinates */
	vis_15 = (double *)malloc(len*sizeof(double)); /* Temporary alocator for season time for each pixel in coordinates */
	tot_vis_3  = (float *)malloc(Npix*sizeof(float));
	tot_vis_2  = (float *)malloc(Npix*sizeof(float));
	tot_vis_15 = (float *)malloc(Npix*sizeof(float));
	
	/* For each pixel, calculate visibility on entire season and store sum to tot_vis. */
	for (i = 0 ; i < Npix ; ++i){
		pix2ang_ring(inpar.nside,i,&fvisPar.glat,&fvisPar.glong);
		fvisPar.glat *= -180./M_PI;
		fvisPar.glat += 90.;
		fvisPar.glong *= 180./M_PI;
		gal2radec(fvisPar.glong,fvisPar.glat,2000.,&fvisPar.ra,&fvisPar.dec);
		field_visibility(fvisPar.ra,fvisPar.dec,fvisPar.epoch,fvisPar.sitelat,fvisPar.sitelong,fvisPar.jdstart,fvisPar.jdend,vis_3,vis_2,vis_15);
		*tot_vis_3  = 0.;
		*tot_vis_2  = 0.;
		*tot_vis_15 = 0.;
		for ( j = 0; j < len ; ++j ){
			*tot_vis_3  += *(vis_3 + j);
			*tot_vis_2  += *(vis_2 + j);
			*tot_vis_15 += *(vis_15+ j);
		}
		++tot_vis_3;
		++tot_vis_2;
		++tot_vis_15;
	}
	tot_vis_3 -=Npix;
	tot_vis_2 -=Npix;
	tot_vis_15-=Npix;
	
	if(inpar.fileout != NULL){
		if ( ( outname = (char *)malloc((strlen(inpar.fileout)+1+8)*sizeof(char) ) ) == NULL){
			printf("ERROR: Could not allocate memory ...");
			return -1;
		}
		
		i = sprintf(outname,"%s_%i.fits",inpar.fileout,3);
		printf("# - Writing output map to %s ...\n",outname);
		write_healpix_map( tot_vis_3, inpar.nside, outname, 0, "G");
		
		i = sprintf(outname,"%s_%i.fits",inpar.fileout,2);
		printf("# - Writing output map to %s ...\n",outname);
		write_healpix_map( tot_vis_2, inpar.nside, outname, 0, "G");
		
		i = sprintf(outname,"%s_%i.fits",inpar.fileout,15);
		printf("# - Writing output map to %s ...\n",outname);
		write_healpix_map( tot_vis_15, inpar.nside, outname, 0, "G");
		
		free(outname);
	}
	else{
		printf("# - Map calculated but no output file given. Storing to \"map.fits\" ...\n");
	}

	free(tot_vis_3 );
	free(tot_vis_2 );
	free(tot_vis_15);
	
	return 0;
	
}

void readInput(int argc, char **argv, void *store)
{
	struct inputPar *data = (struct inputPar *)store;
	int i, inpos[4] = {1,3,5,7}, inflag[4] = { -1 , -1 , -1 , -1 };
		
	if (argc == 1){
		printHelpPage();
	}
	if (argc > 1){
		testArg(argv[1]);
	}

	for (i = 0 ; i < argc/2; ++i){
		
		switch (argv[inpos[i]][1]){
		case 'n':
			data->nside = atoi(argv[inpos[i]+1]);
			inflag[0] = 0;
			break;
		case 'f':
			data->fileout = (char *)malloc(( strlen(argv[inpos[i]+1])+1)*sizeof(char));
			strcpy(data->fileout, argv[inpos[i]+1]);
			inflag[1] = 0;
			break;
		case 't':
			data->jdstart = atof(argv[inpos[i]+1]);
			inflag[2] = 0;
			break;
		case 'd':
			data->days = atof(argv[inpos[i]+1]);
			inflag[3] = 0;
			break;
			
		}
	}
	
	if(inflag[0] < 0) data->nside = 16;
	if(inflag[1] < 0){
		data->fileout = (char *)malloc(5*sizeof(char));
		strcpy(data->fileout, "map");
	}
	if(inflag[2] < 0) data->jdstart = 2456139.;
	if(inflag[3] < 0) data->days = 365.;
	
	
}

void printHelpPage(void){
	printf("Usage: [visibility] -n [nside:=16] -f [filename:=map] -t [hjd_stard:=2456139.] -d [days:=365.]\n");
	exit(0);
}

void testArg(char *arg){
	if ( strcmp(arg, "-h") == 0) printHelpPage();
}
