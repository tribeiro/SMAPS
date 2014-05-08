c--ZONA SUR
        PARAMETER(N=189) !ancho
        PARAMETER(M=119) !alto
        integer O(N,M) !decide qué píxeles son parte o no
        double precision alfabeta(N,M,2), radec(N,M,3)
        double precision alfa, beta, ra, dec, rot, ancho, chi, a0          !
        double precision raN, decN

        icentro=95
        jcentro=60
        ancho=1.454 !ancho en grados entre 2 apuntados
        chi=25.
        a0=105.
        raN=195
        decN=65


C-- Primera parte: generar el array

        do j=1,M        !reseteo todo
          do i=1,N
            O(i,j)=1
          end do
        end do
c--------------------------------------------------------------------|
        do j=1,M
        do i=1,N
            alfa=(icentro-i)*ancho
            beta=(jcentro-j)*ancho
            alfabeta(i,j,1)=alfa
            alfabeta(i,j,2)=beta
            ra=MOD(180.+a0+(ATAN2((COS(beta*3.141592654/180.)
     &*SIN((alfa+90.)*3.141592654/180.)*COS(chi*3.141592654/180.)
     &-SIN(beta*3.141592654/180.)*SIN(chi*3.141592654/180.)),
     &(COS(beta*3.141592654/180.)*COS((alfa+90.)*3.141592654/180.))))
     &*180./3.141592654,360.)
            dec=ASIN((COS(beta*3.141592654/180.)*SIN((alfa+90.)
     &*3.141592654/180.)*SIN(chi*3.141592654/180.)) +
     &(SIN(beta*3.141592654/180.)*COS(chi*3.141592654/180.)))
     &*180./3.141592654
            rot=180.*(ATAN((2.*COS(decN*3.141592654/180.))
     &/((TAN(((raN-ra)/2.)*3.141592654/180.)*SIN((decN+dec)
     &*3.141592654/180.))+((1./TAN(((raN-ra)/2.)*3.141592654/180.))
     &*SIN((decN-dec)*3.141592654/180.)))))/3.141592654
            radec(i,j,1)=ra
            radec(i,j,2)=dec
            radec(i,j,3)=rot
          IF(ra.gt.180.) then
            if((dec.gt.35.).or.
     &(dec.lt.10.)) then
              O(i,j)=-1
            endif
            if(ra.lt.330.) then
              O(i,j)=-1
            endif
          else
            if((dec.gt.46.).or.
     &(dec.lt.-1.25)) then
              O(i,j)=-1
            endif
            if(ra.gt.42.) then
              O(i,j)=-1
            endif
            if((ra.gt.33.).and.
     &(dec.gt.8.).and.
     &(dec.lt.28.))  then
              O(i,j)=-1
            endif
          endif
          
        end do
        end do

c--calculo límites
        imax=0
        imin=N+1
        jmax=0
        jmin=M+1
        do j=1,M
        do i=1,N
            if(O(i,j).eq.1) then
                if(i.gt.imax) imax=i
                if(i.lt.imin) imin=i
                if(j.gt.jmax) jmax=j
                if(j.lt.jmin) jmin=j
            endif
        end do
        end do
        print*,'limites',imin,imax,jmin,jmax
        print*,'limites corregidos',imax-imin+1,' x',jmax-jmin+1
        print*,'centro',icentro-imin+1,' x',jcentro-jmin+1
        
        open(11,file='surpointT80.dat')
        do j=1,M
        do i=1,N
         if(O(i,j).eq.1) then
          write(11,*) i-imin+1,j-jmin+1,
     &alfabeta(i,j,1),alfabeta(i,j,2),
     &radec(i,j,1),radec(i,j,2),radec(i,j,3)
         end if
        end do
        end do
        close(11)

        end
