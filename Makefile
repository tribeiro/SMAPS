
incdir = /home/tiago/Downloads/Healpix_2.20a/include/
libdir = /home/tiago/Downloads/Healpix_2.20a/lib/

visibility : %: %.c _skysub.c
	gcc -o visibility  $@.c -I$(incdir) -lm -lchealpix -lcfitsio _skysub.o 

skysub :
	gcc -c _skysub.c