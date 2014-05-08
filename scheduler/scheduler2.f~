        INTEGER PN(242,123,4), PS(132,89,4)  !Sky pointings, 4 trays
        INTEGER FN(242,123), FS(132,89)      !Forbidden zones
        INTEGER CHUNGOS(2929)                !meteo: cloudy days for 8 years (8 years=2920 days; ~101 lunar cycles of 29 days = 2929)
        INTEGER BN(242,123), BS(132,89)      !Label for used trays 
        INTEGER RADECN(242,123,2), RADECS(132,89,2)  !Equivalence between matrix coordinate i,j and sky coordinate RA,dec
        DOUBLE PRECISION TWILIGHT(2929,2)    !Twilight start and end; measured from midday
        DOUBLE PRECISION TIEMPO, TEXP, texptot, tnoexpo, tnoexptot
        DOUBLE PRECISION latitud, HA, horasid, dia
        DOUBLE PRECISION altura, horasid2, radec2
        
c-- Output files
        open(12,file='timelost.dat')
        open(13,file='alturas.dat')
        open(16,file='areaobs.dat')
                
c-- Initializing variables
        do i=1,242
        do j=1,123
          do ib=1,4
            PN(i,j,ib)=0   !North field
          end do
          FN(i,j)=-1
        end do
        end do

        do i=1,132
        do j=1,89
          do k=1,4
            PS(i,j,k)=0   !South field
          end do
          FS(i,j)=-1
        end do
        end do
        do i=1,2929
            chungos(i)=0
        end do
        
        latitud=40.04


C--READING CONFIGURATION FILES

c-- Reading cloudy days

        open(11,file='meteo.dat')   !reading 8 years of meteorology
91          read(11,*,END=90) ichungo
            chungos(ichungo)=1
        goto 91
90      continue
        close(11)

c--Reading equivalence between matrix i,j coordinate and sky equatorial coordinate
c--Note: It only assigns values to observable zones! For i,j values in forbidden zones
c--matrix RADEC has no value; there, it has assigned -1 in FN and FS (forbidden zones)
c--Note: adummy, bdummy and rot are not used in the program.

        open(11,file='norpoint.dat')
81          read(11,*,END=80) ii,ij,adummy,bdummy,alfa,delta,rot
            RADECN(ii,ij,1)=alfa   !RA
            RADECN(ii,ij,2)=delta  !Dec
            FN(ii,ij)=0
        goto 81
80      continue
        close(11)

        open(11,file='surpoint.dat')
71          read(11,*,END=70) ii,ij,adummy,bdummy,alfa,delta,rot
            RADECS(ii,ij,1)=alfa
            RADECS(ii,ij,2)=delta
            FS(ii,ij)=0
        goto 71
70      continue
        close(11)

c-- Reading start and end of twilight. Note: Measured from midday!! In hours.
c-- It is a mean value for a year; it does not take into account leap years. 

        open(11,file='twilight.dat')
        do idia=1,365   !twilight first year
            read(11,*) ii,a1,a2
            twilight(idia,1)=a1
            twilight(idia,2)=a2
        end do
        do iyear=1,7  !I clone it cyclically for the other 7 years
        do idia=1,365
            twilight(idia+365*iyear,1)=twilight(idia,1)
            twilight(idia+365*iyear,2)=twilight(idia,2)
        end do
        end do
        do idia=1,9  !To take into account that there are still 9 days in the last lunar cycle that are in the 9th year
            twilight(idia+2920,1)=twilight(idia,1)
            twilight(idia+2920,2)=twilight(idia,2)
        end do

C--END OF FILE READING


c-- Starting the loop of days. Suppose that we start 2 days before full moon (why not?)

        dia=0.  !real; fractions of day (the "hour")
        idia=0  !integer; the current day
        tnoexptot=0.
        texptot=0.
        
C-- Loop of lunar cycles: in 8 years there are 101 cycles of 29 days.

        do imoon=1,101

         do iciclo=1,29  !29 days in a cycle (it is an approximation)
          idia=idia+1
          tnoexpo=0.
          almax=0.
          almin=90.

          if(chungos(idia).eq.0) then               !If there aren't cloud, let's work!
          if((iciclo.ne.3).and.(iciclo.ne.4)) then  !If it is not full moon, let's work!
          
            if(iciclo.le.7) iban=1
            if((iciclo.ge.8).and.(iciclo.le.12)) iban=2
            if((iciclo.ge.13).and.(iciclo.le.24)) iban=4
            if(iciclo.ge.25) iban=3                       !selecting the tray to work with
                        
            if((iciclo.eq.1).or.(iciclo.eq.8).or.(iciclo.eq.13) 
     &.or.(iciclo.eq.25)) then
     
             do i=1,242         !reseting BN and BS every time we change the tray
             do j=1,123
               BN(i,j)=0
             end do
             end do

            do i=1,132
            do j=1,89
               BS(i,j)=0
             end do
             end do     
     
            end if

            if(iban.eq.4) then     !exposure time according to the tray, in seconds
                texp=469./3.
            else
                texp=222./3.
            endif        
        
            do tiempo=twilight(idia,1),twilight(idia,2),(texp/3600.)  !exposure loop in a night
            
              dia=(1.*idia - 1.) + tiempo/24.   !current day and fraction, to calculate the siderean time; starting at midday.
            
              horasid=(MOD( 274.37083333     !siderean time in degrees; it is approximated.
     &+ 360.98564736629 * mod(dia,365) , 360.))

              alturamax=0.
              ifield=0
              imax=0
              jmax=0
c-- Elección del campo a observar:     

c--Primero repaso el campo 1
                ifieldo=1
C--------------------------------------------------------------------|  anchura fortran     
        do i=1,242  !disminuyo el sangrado porque si no me quedaré sin espacio, por la coña de los 72 caracteres del fortran.
        do j=1,123
          if((BN(i,j).lt.2).and.(FN(i,j).eq.0)
     &.and.(PN(i,j,iban).lt.3)) then    
            HA = horasid-RADECN(i,j,1)
            altura=180*(ASIN(SIN(RADECN(i,j,2)*3.141592654/180)
     &*SIN(latitud*3.141592654/180)+COS(RADECN(i,j,2)*3.141592654/180)
     &*COS(latitud*3.141592654/180)*COS(HA*3.141592654/180)))
     &/3.141592654
            if(altura.ge.40.) then  !Con este IF y el anterior, selecciono los que son observables, en principio.
            
                  if(altura.gt.alturamax) then
                    alturamax=altura
                    imax=i
                    jmax=j
                    ifield=ifieldo
                  endif
              
            endif
          endif    
        end do
        end do
C--------------------------------------------------------------------|  anchura fortran
  
c--luego el campo 2
                ifieldo=2              
C--------------------------------------------------------------------|  anchura fortran   
        do i=1,132  !disminuyo el sangrado porque si no me quedaré sin espacio, por la coña de los 72 caracteres del fortran.
        do j=1,89
          if((BS(i,j).lt.2).and.(FS(i,j).eq.0)
     &.and.(PS(i,j,iban).lt.3)) then    
            HA = horasid-RADECS(i,j,1)
            altura=180*(ASIN(SIN(RADECS(i,j,2)*3.141592654/180)
     &*SIN(latitud*3.141592654/180)+COS(RADECS(i,j,2)*3.141592654/180)
     &*COS(latitud*3.141592654/180)*COS(HA*3.141592654/180)))
     &/3.141592654
            if(altura.ge.40.) then  !Con este IF y el anterior, selecciono los que son observables, en principio.

                  if(altura.gt.alturamax) then
                    alturamax=altura
                    imax=i
                    jmax=j
                    ifield=ifieldo
                  endif
            
            endif
          endif    
        end do
        end do
C--------------------------------------------------------------------|  anchura fortran              
              
                ! Tras esto tengo elegido un campo (ifield), y el punto a observar (imax,jmax), que maximiza la altura
                ! siguiendo nuestros criterios de visibilidad, en esta exposición. Ahora lo observo:
              
              if(imax.gt.0) then   !si siguiera siendo 0 es porque no se ha encontrado ningún punto donde mirar
               texptot=texptot+texp/(3600.)
               if(ifield.eq.1) then
                PN(imax,jmax,iban)=PN(imax,jmax,iban)+1   !hasta un máximo de 3
                BN(imax,jmax)=BN(imax,jmax)+1             !hasta un máximo de 2
               else
                PS(imax,jmax,iban)=PS(imax,jmax,iban)+1   
                BS(imax,jmax)=BS(imax,jmax)+1             
               endif
              else
               tnoexpo=tnoexpo+texp  !para ver cuánto no he observado ese día
              endif
              
              if(alturamax.gt.almax) almax=alturamax  !hacemos esto para guardar registro de la altura máxima y mínima OBSERVADAS a lo largo de este día
              if(alturamax.lt.almin) almin=alturamax
                          
            end do   !fin del bucle de exposiciones en el día en curso.

            if (tnoexpo.gt.0.) write(12,*) 
     &'Tiempo perdido en el dia',idia,' = ',tnoexpo,' segundos.'
            if (almax.gt.0.) write(13,*) 'dia ',idia,
     &' altura maxima observada ',almax,
     &' altura minima observada ',almin
            tnoexptot=tnoexptot+tnoexpo/(3600.)

          endif !fin del IF sobre si estamos en luna llena
          endif !fin del IF sobre si hay nubes

         call imagen(PN,PS,FN,FS,idia) 
                   
         end do !fin loop de días en un ciclo
        
c--     Veo CADA MES el total de area observada con TODAS las bandejas:

        areatotal=0.   !en grados cuadrados

        do i=1,242
        do j=1,123
          if((PN(i,j,1).eq.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).eq.3)) then
           areasub=0.573*0.573*cos(((62.-j)*0.573)*3.141592654/180.)
           areatotal=areatotal+areasub
          endif
        end do
        end do
        do i=1,132
        do j=1,89
          if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).eq.3)) then
           areasub=0.573*0.573*cos(((42.-j)*0.573)*3.141592654/180.)
           areatotal=areatotal+areasub
          endif
        end do
        end do
        write(16,*) 'ciclo lunar ',imoon,' area completada ',areatotal
        
        end do !fin loop periodos lunares
    
        close(12)
        close(13)
        close(16)
        
c--     Veo AL FINAL el total de area observada con TODAS las bandejas:

        areatotal=0.   !en grados cuadrados

        do i=1,242
        do j=1,123
          if((PN(i,j,1).eq.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).eq.3)) then
           areasub=0.573*0.573*cos(((62.-j)*0.573)*3.141592654/180.)
           areatotal=areatotal+areasub
          endif
        end do
        end do
        do i=1,132
        do j=1,89
          if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).eq.3)) then
           areasub=0.573*0.573*cos(((42.-j)*0.573)*3.141592654/180.)
           areatotal=areatotal+areasub
          endif
        end do
        end do
        
        print*,'Area total observada: ',areatotal,' grados cuadrados'
        print*,'Tiempo total observado: ',texptot,' horas'
        print*,'Tiempo perdido: ',tnoexptot,' horas'

        END



        subroutine imagen(pn,ps,fn,fs,label)
        INTEGER PN(242,123,4), PS(132,89,4)  !Apuntados celestes, para 4 bandejas
        INTEGER FN(242,123), FS(132,89)  !Zonas prohibidas
        integer label
        character*1 rgb(3,376,124) ! RGB image array
        character*1 rgbud(3,376,124) ! RGB image array, upside down


        do i=1,376   
        do j=1,124
           rgb(1,i,j)=char(100)  !fondo gris
           rgb(2,i,j)=char(100)
           rgb(3,i,j)=char(100)
        end do
        end do

        do i=1,242
        do j=1,123
            if(FN(i,j).eq.0) then
             rgb(1,i,j)=char(0)  !campo negro
             rgb(2,i,j)=char(0)
             rgb(3,i,j)=char(0)
            end if
        end do
        end do

        do i=1,132
        do j=1,89
            if(FS(i,j).eq.0) then
             rgb(1,i+242,j)=char(0)  !campo negro
             rgb(2,i+242,j)=char(0)
             rgb(3,i+242,j)=char(0)
            end if
        end do
        end do


        do i=1,242
        do j=1,123

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(255)
         rgb(2,i,j)=char(0)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(255)
         rgb(2,i,j)=char(255)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(0)
         rgb(2,i,j)=char(196)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(0)
         rgb(2,i,j)=char(0)
         rgb(3,i,j)=char(255)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(255)
         rgb(2,i,j)=char(128)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(165)
         rgb(2,i,j)=char(83)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(128)
         rgb(2,i,j)=char(0)
         rgb(3,i,j)=char(128)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(128)
         rgb(2,i,j)=char(255)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(128)
         rgb(2,i,j)=char(128)
         rgb(3,i,j)=char(128)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(0)
         rgb(2,i,j)=char(220)
         rgb(3,i,j)=char(220)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).ne.3)) then
         rgb(1,i,j)=char(204)
         rgb(2,i,j)=char(160)
         rgb(3,i,j)=char(0)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).ne.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(204)
         rgb(2,i,j)=char(114)
         rgb(3,i,j)=char(94)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).ne.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(153)
         rgb(2,i,j)=char(153)
         rgb(3,i,j)=char(153)
        endif

        if((PN(i,j,4).ne.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(98)
         rgb(2,i,j)=char(178)
         rgb(3,i,j)=char(128)
        endif

        if((PN(i,j,4).eq.3)
     &.and.(PN(i,j,3).eq.3)
     &.and.(PN(i,j,2).eq.3)
     &.and.(PN(i,j,1).eq.3)) then
         rgb(1,i,j)=char(255)
         rgb(2,i,j)=char(255)
         rgb(3,i,j)=char(255)
        endif

        end do
        end do

        do i=1,132
        do j=1,89

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(255)
         rgb(2,i+242,j)=char(0)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(255)
         rgb(2,i+242,j)=char(255)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(0)
         rgb(2,i+242,j)=char(196)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(0)
         rgb(2,i+242,j)=char(0)
         rgb(3,i+242,j)=char(255)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(255)
         rgb(2,i+242,j)=char(128)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(165)
         rgb(2,i+242,j)=char(83)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(128)
         rgb(2,i+242,j)=char(0)
         rgb(3,i+242,j)=char(128)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(128)
         rgb(2,i+242,j)=char(255)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(128)
         rgb(2,i+242,j)=char(128)
         rgb(3,i+242,j)=char(128)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(0)
         rgb(2,i+242,j)=char(220)
         rgb(3,i+242,j)=char(220)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).ne.3)) then
         rgb(1,i+242,j)=char(204)
         rgb(2,i+242,j)=char(160)
         rgb(3,i+242,j)=char(0)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).ne.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(204)
         rgb(2,i+242,j)=char(114)
         rgb(3,i+242,j)=char(94)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).ne.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(153)
         rgb(2,i+242,j)=char(153)
         rgb(3,i+242,j)=char(153)
        endif

        if((PS(i,j,4).ne.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(98)
         rgb(2,i+242,j)=char(178)
         rgb(3,i+242,j)=char(128)
        endif

        if((PS(i,j,4).eq.3)
     &.and.(PS(i,j,3).eq.3)
     &.and.(PS(i,j,2).eq.3)
     &.and.(PS(i,j,1).eq.3)) then
         rgb(1,i+242,j)=char(255)
         rgb(2,i+242,j)=char(255)
         rgb(3,i+242,j)=char(255)
        endif

        end do
        end do


        do i=1,376   
        do j=1,124
           rgbud(1,i,j)=rgb(1,i,125-j)
           rgbud(2,i,j)=rgb(2,i,125-j)
           rgbud(3,i,j)=rgb(3,i,125-j)
        end do
        end do

         call pixmap(rgbud,label) 


       end 


* --------------------------------------------
*
* Notes
* o With a parameter ipixout set at 1, 2 or others,
*   this subroutine will generate PPM-P6(binary), PPM-P3(text),
*   or BMP(24bit depth without color table).
*
* o Some parts follow DEC-FORTRAN convention that had been defacto-standard long ago.
*   Some compilers today may not accept if "ipixout" is set other than 2.
*
* o g77 (ver. 3.3.3) works for all three choices.
* o Intel compiler (ver. 9 or later) works for all three choices.
*
* --------------------------------------------
*
       subroutine pixmap(rgb,nframe)
       implicit none
* interface arg.
       integer ihpixf, jvpixf
       parameter(ihpixf = 376, jvpixf = 124) ! pixel size, eacg must be multiple of 4, if BMP is chosen as output format.
       character*1 rgb(3,ihpixf,jvpixf)      ! RGB data array
       integer nframe
* local
       character*12 fnameout
       integer i, j, k
       integer itmp, icnt
       character*14 frmtstr
       character*54 headmsw
       character*4  byt4
       character*2  byt2
* choices
       integer ipixout
       parameter(ipixout = 3) ! 1 / 2 / other= PPM6, PPM3, BMP(24bit)

       if (ipixout .EQ. 1) then

* PPM P6

         write(fnameout,'(''map_'',i4.4,''.ppm'')') nframe ! name of PPM file
         open(unit=2,file=fnameout,status='unknown')
         write(*,*) 'Now writing PPM (P6) file : ', fnameout
* header
         write(2,'(''P6'', 2(1x,i4),'' 255 '',$)')         ! some compiler may not accept this line.
     &     ihpixf, jvpixf
* image data
         itmp = ihpixf * jvpixf * 3
         write(frmtstr,'(''('',i8.8,''A,$)'')') itmp     ! make output "format"
         write(2,fmt=frmtstr)                              ! some compiler may not accept this line.
     &     (((rgb(k,i,j),k=1,3),i=1,ihpixf),j=jvpixf,1,-1) ! here, j (vertical address) runs from top to bottom.
         close(2)

       else if (ipixout .EQ. 2) then

* PPM P3 ! rather "safer" choice for many Fortran compiler(s).

         write(fnameout,'(''map_'',i4.4,''.ppm'')') nframe ! name of PPM file
         open(unit=2,file=fnameout,status='unknown')
         write(*,*) 'Now writing PPM (P3) file : ', fnameout
* header
         write(2,'(A)') 'P3'
         write(2,'(2(1x,i4),'' 255 '')')  ihpixf, jvpixf
         icnt = 0
* image data
         do j = jvpixf, 1, -1                              ! here, j (vertical address) runs from top to bottom.
         do i = 1, ihpixf, 1
         do k = 1, 3
           itmp = ichar(rgb(k,i,j))
           icnt = icnt + 4
           if (icnt .LT. 60) then
             write(2,fmt='(1x,i3,$)') itmp                 ! "$" is not standard.
           else
             write(2,fmt='(1x,i3)') itmp
             icnt = 0
           endif
         enddo
         enddo
         enddo
         write(2,'(A)') ' '
         close(2)

       else

* BMP (24bit depth)... this part works only when width is multiple of 4.

         itmp = mod(ihpixf, 4)
         if (itmp .NE. 0) then
           write(*,*) 'width must be multiple of 4'
           stop
         endif

         write(fnameout,'(''map_'',i4.4,''.bmp'')') nframe ! name of BMP file
         open(unit=2,file=fnameout,status='unknown')
         write(*,*) 'Now writing BMP(24bit) file : ', fnameout
* header 1 (file header ; 1--14 byte)
         headmsw( 1: 2) = 'BM'             ! declaring this is BMP file
         itmp = 54 + ihpixf * jvpixf * 3 ! total file size = header + data
         call num2bit4(itmp,byt4)
         headmsw( 3: 6) = byt4(1:4)
         itmp = 0                        ! may be 0
         call num2bit2(itmp,byt2)
         headmsw( 7: 8) = byt2(1:2)
         itmp = 0                        ! may be 0
         call num2bit2(itmp,byt2)
         headmsw( 9:10) = byt2(1:2)
         itmp = 54                       ! must be 54 : total length of header
         call num2bit4(itmp,byt4)
         headmsw(11:14) = byt4(1:4)
* header 2 (bit-map header ; 13--54 byte)
         itmp = 40                       ! must be 40 : length of bit-map header
         call num2bit4(itmp,byt4)
         headmsw(15:18) = byt4(1:4)
         itmp = ihpixf                   ! width
         call num2bit4(itmp,byt4)
         headmsw(19:22) = byt4(1:4)
         itmp = jvpixf                   ! height
         call num2bit4(itmp,byt4)
         headmsw(23:26) = byt4(1:4)
         itmp = 1                        ! must be 1
         call num2bit2(itmp,byt2)
         headmsw(27:28) = byt2(1:2)
         itmp = 24                       ! must be 24 : color depth in bit.
         call num2bit2(itmp,byt2)
         headmsw(29:30) = byt2(1:2)
         itmp = 0                        ! may be 0 : compression method index
         call num2bit4(itmp,byt4)
         headmsw(31:34) = byt4(1:4)
         itmp = 0                        ! may be 0 : file size if compressed
         call num2bit4(itmp,byt4)
         headmsw(35:38) = byt4(1:4)
         itmp = 0                        ! arbit. : pixel per meter, horizontal
         call num2bit4(itmp,byt4)
         headmsw(39:42) = byt4(1:4)
         itmp = 0                        ! arbit. : pixel per meter, vertical
         call num2bit4(itmp,byt4)
         headmsw(43:46) = byt4(1:4)
         itmp = 0                        ! may be 0 here : num. of color used
         call num2bit4(itmp,byt4)
         headmsw(47:50) = byt4(1:4)
         itmp = 0                        ! may be 0 here : num. of important color
         call num2bit4(itmp,byt4)
         headmsw(51:54) = byt4(1:4)

* writing header part
         write(2,'(a54,$)') headmsw(1:54)
* image data
         itmp = ihpixf * jvpixf * 3
         write(frmtstr,'(''('',i8.8,''A,$)'')') itmp
         write(2,fmt=frmtstr)
     &     (((rgb(k,i,j),k=3,1,-1),i=1,ihpixf),j=1,jvpixf) ! writing in BGR order, not RGB.
         close(2)

       endif

       return
       end 

* --------------------------------------
* convert integer values to 4 8-bit characters
* --------------------------------------

       subroutine num2bit4(inum,byt4)
       implicit none
       integer inum
       character*4 byt4
       integer itmp1, itmp2
       itmp1 = inum
       itmp2 = itmp1 / 256**3
       byt4(4:4) = char(itmp2)
       itmp1 =-itmp2 * 256**3 +itmp1
       itmp2 = itmp1 / 256**2
       byt4(3:3) = char(itmp2)
       itmp1 =-itmp2 * 256**2 +itmp1
       itmp2 = itmp1 / 256
       byt4(2:2) = char(itmp2)
       itmp1 =-itmp2 * 256    +itmp1
       byt4(1:1) = char(itmp1)
       return
       end subroutine num2bit4

* --------------------------------------
* convert integer values to 2 8-bit characters
* --------------------------------------

       subroutine num2bit2(inum,byt2)
       implicit none
       integer inum
       character*2 byt2
       integer itmp1, itmp2
       itmp1 = inum
       itmp2 = itmp1 / 256
       byt2(2:2) = char(itmp2)
       itmp1 =-itmp2 * 256 + itmp1
       byt2(1:1) = char(itmp1)
       return
       end subroutine num2bit2
