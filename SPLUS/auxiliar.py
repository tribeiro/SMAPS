
import numpy as np
import math
#from vec3d import *

###########################################################################

Rad = np.pi/180.0
Deg = 180.0/np.pi
Hour = 12./np.pi
Arcs = 3600.0*180.0/np.pi
MJD_J2000 = 51544.5
JD_J2000 = 2451545.0
T_J2000 = 0. #JD_J2000
GM_Sol = 0.01720209895**2 # AU^3/d^2

###########################################################################

def Frac(val):
	'''
	Returna a parte fracional de val.
	'''
	
	return val-np.floor(val)

###########################################################################

def Modulo(x,y):
	'''
	Retorna o modulo de x em relacao a y
	'''
	return y * Frac(x/y)

###########################################################################

def Arange(x,y):
	'''
	Retorna o numero entre o limite 0 - y
	'''

	return x - np.floor(x/y)*y

###########################################################################

def Hhh(H,M,S):
	'''
	Hhh: Converte de horas, minutos e segundos para um numero descimal.
	'''

	sinal = 1.0
	if H < 0 or M < 0 or S < 0:
		sinal = -1.0

	return sinal * float(np.abs(H)) * float(np.abs(M)) * float(np.abs(S))


###########################################################################

def mjd(ano,mes,dia,hora=0,min=0,seg=0.0):
	'''
Retorna a hora juliana modificada (MJD) a partir de uma data e hora.
	
Parametros:
		Ano: Inteiro especificando o ano
		Mes: Inteiro especificando o mes (1 a 12)
		Dia: Inteiro especificando o dia
Parametros opcionais:
		Hora: Inteiro especificando a hora
		Min: Inteiro especificando os minutos
		Sec: Ponto Flutuante especificando os segundos
	'''

	b = 0
	if mes <= 2:
		mes +=12
		ano -=1
	if ( 10000.*ano+100.*mes+dia) <= 15821004.:
		b = int(-2 + ((ano+4716)/4) - 1179) # Calendario Juliano
	else:
		b = (ano/400)-(ano/100)+(ano/4) # Calendario Gregoriano

	MjdMeiaNoite = 365.*ano - 679004. + b + int(30.6001*(mes+1)) + dia
	FracDeDia = Hhh(hora,min,seg) / 24.0

	return MjdMeiaNoite + FracDeDia

###########################################################################

def NDays(y,m,d,h=11):
	return (367*(y)-((7*((y)+(((m)+9)/12)))/4)+((275*(m))/9)+(d)-730530)

###########################################################################

def Rad2Hour(ang):
	'''
	Convert from Radians to Hours angle
	'''

	return ang*12./np.pi

###########################################################################

def Hour2Rad(ang):
	'''
	Convert from Radians to Hours angle
	'''

	return ang*np.pi/12.

###########################################################################

def Deg2Hour(ang):
	'''
	Convert from Radians to Hours angle
	'''

	return ang*12./180.

###########################################################################

def R_x(phi):

	'''
	Rotation over x matrix.
	'''

	return np.array(	[	[1 ,        0 ,        0      ] ,
							[0 ,  np.cos(phi),  np.sin(phi)] ,
							[0 , -np.sin(phi),  np.cos(phi)] ] )

###########################################################################

def R_y(phi):

	'''
	Rotation over y matrix.
	'''

	raise NotImplemented

###########################################################################

def R_z(phi):

	'''
	Rotation over z matrix.
	'''

	return np.array(	[	[ np.cos(phi),  np.sin(phi),	0] ,
							[-np.sin(phi),  np.cos(phi),	0] ,
							[0 ,        0 ,        1     ] ] )


###########################################################################

def Equ2EclMatrix(T):
	'''
Equ2EclMatrix: Transformacao de coordenadas equatoriais para eclipticas
	Entrada:
		T Tempo em seculos julianos desde J2000
	Retorna
		Matriz de transformacao
	'''

	eps = ( 23.43929111-(46.8150+(0.00059-0.001813*T)*T)*T/3600.0 ) * Rad

	return R_x(eps)

###########################################################################

def Ecl2EquMatrix(T):
	'''
Ecl2EquMatrix: Transformacao de coordenadas eclipticas para equatoriais
	Entrada:
		T Tempo em seculos julianos desde J2000
	Retorna
		Matriz de transformacao
	'''

	return Equ2EclMatrix(T).T

###########################################################################

def sind(val):

	return np.sin(val*Rad)

###########################################################################

def cosd(val):

	return np.cos(val*Rad)

###########################################################################

def atan2d(val1,val2):

	return np.arctan2(val1,val2)*Deg

###########################################################################

def Hms(hour):
	hh = np.floor(hour)
	mm = (hour - hh)*60.
	rmm = np.floor(mm)
	ss = (mm - rmm)*60.

	return '%02.0f:%02.0f:%05.2f'%(hh,rmm,ss)

###########################################################################

def Dms(hour):
	signal = hour/np.abs(hour)
	hh = np.floor(np.abs(hour))
	mm = (np.abs(hour) - hh)*60.
	rmm = np.floor(mm)
	ss = (mm - rmm)*60.

	return '%+03.0f:%02.0f:%05.2f'%(signal*hh,rmm,ss)

###########################################################################

def PrecMatrix_Ecl(T1, T2):
	'''
PrecMatrix_Ecl: Prececao das coordenadas eclipticas
	
	Entrada:
		T1	-	Epoca desejada
		T2	-	Epoca a ser precesionada
	Saida:
		Matriz de precessao
Nota:
	T1 e T2 em seculo julianos desde J2000
	'''
	
	dT = T2-T1
	
	Pi = 174.876383889*Rad + \
		 ( ((3289.4789+0.60622*T1)*T1) + \
			   ((-869.8089-0.50491*T1) + 0.03536*dT)*dT )/Arcs

	pi = ( ( 47.0029-(0.06603-0.000598*T1)*T1)+ \
			    ((-0.03302+0.000598*T1)+0.000060*dT)*dT )*dT/Arcs
	
	p_a = ( (5029.0966+(2.22226-0.000042*T1)*T1)+\
			    ((1.11113-0.000042*T1)-0.000006*dT)*dT )*dT/Arcs

	return np.dot(R_z(-(Pi+p_a)),np.dot(R_x(pi),R_z(Pi)))

###########################################################################

def GaussVec(Omega,inc,omega):
	'''
	GaussVec:	Calcula as matrizes de transformacao de coordenadas no
				plano orbital para o sistem ecliptico.

		Entrada:
			Omega	-	Longitude do nodo ascendente [rad]
			i		-	Inclinacao da orbita [rad]
			omega	-	Argumento do perihelio [rad]
			
		Saida:
			Matriz de transformacao contendo os vetores gaussianos P,Q,R
	'''

	return np.dot(R_z(-Omega),np.dot(R_x(-inc),R_z(-omega)))

###########################################################################

def PosSol(T):
	'''
 PosSol: Calcula a posicao do Sol em coordenadas eclipticas utilizando uma
         serie analitica.
	Entrada:
		T	-	Tempo em seculos julianos desde J2000
	Saida:
		Vetor com coordenadas eclipticas do sol (em AU)
	'''

	raise NotImplementedError('PosSol nao implementado. Use minisun.')

	# Anomalias medias 

###########################################################################

def EccAnom(M,e):
	'''
EccAnom: Calcula ecentricidade anomola para orbitas elipticas.

	Entrada:
		M	Anomalia media [rad]
		e	Ecentricidade [0,1)
	Retorna:
		Anomalia ecentrica [rad]
	'''

	MAXINT = 15 # numero maximo de iteracoes
	eps = 1e-12

	M = Modulo(M,2.0*np.pi)
	E = M
	if e > 0.8:
		E = np.pi

	# setup interactive pross
	i = 0
	f = E - e*np.sin(E) - M
	nE = E - f/(1.0-e*np.cos(E))
	diff = np.abs(E-nE)
	E=nE
	
	while (diff > eps):
		f = E - e*np.sin(E) - M
		nE = E - f/(1.0-e*np.cos(E))
		diff = np.abs(E-nE)
		E=nE
		i+=1
		if (i > MAXINT):
			raise StopIteration('Problemas de convergencia em EccAnom.')

	return E

###########################################################################

def Ellip(GM,M,a,e):
	'''
Ellip: Calcula vetores de posicao e velocidade para orbitas elipticas.

	Entrada:
		GM	Produto da constante gravitacional e a massa central [AU^3/d^2]
		M	Anomalia media [rad]
		a	Semi-eixo maior da orbita em AU
		e	Ecentricidade da orbita (<1)
	Retorna:
		r	Posicao em relacao ao plano orbital [AU]
		v	Velocidade em relacao ao plano orbital [AU/d]
	'''

	k = np.sqrt(GM/a)
	E = EccAnom(M,e)
	cosE = np.cos(E)
	sinE = np.sin(E)
	fac = np.sqrt( (1.0-e) * (1.0+e) )
	rho = 1.0 - e*cosE
	
	#rVec = vec3(a*(cosE-e),a*fac*sinE, 0.0)
	#vVec = vec3(-k*sinE/rho,k*fac*cosE/rho, 0.0)
	#r = rVec.get_spherical()
	#v = vVec.get_spherical()
	return [a*(cosE-e),a*fac*sinE, 0.0],[-k*sinE/rho,k*fac*cosE/rho, 0.0]

###########################################################################

def Kepler(GM, t0,t,q,e,PQR):
	'''
Kepler: Calcula os vetores posicao e velocidade para orbitas keplerianas
		em orbita eclipticas
		
	Entrada:
		GM	Produto da constante gravitacional e a massa central [AU^3/d^2]
		t0	Tempo de passagem pelo perihelio
		t	Tempo a ser considerado
		q	Distancia ao perihelio [AU]
		e	Ecentricidade da orbita
		PQR	Matriz de transformacao, plano orbital -> ecliptica (Vetores Gaussianos)
	Retorna:
		r	Posicao ecliptica em coord. heliocentricas [AU]
		v	Velocidade ecliptica em coord. heliocentricas [AU/d]
Nota: t0 e t devem ser dados em seculos julianos desde J2000
	'''
	
	M0 = 0.1
	eps = 0.01
	
	delta = np.abs(1-e)
	invax = delta/q
	tau = np.sqrt(GM)*(t-t0)
	M = tau * np.sqrt(invax*invax*invax)
	
	if delta < eps:
		r_orb,v_orb = Parab(GM,t0,t,q,e)
	elif e < 1.0:
		r_orb,v_orb = Ellip(GM,M,1.0/invax,e)
	else:
		r_orb,v_orb = Hiperb(GM,t0,t,1.0/invax,e)

	r = np.dot(PQR,r_orb)
	v = np.dot(PQR,v_orb)
	return r,v
###########################################################################

def Elementos(GM,r,v):
	'''
Elements:	Calcula os elementos de uma orbita eliptica atravez dos vetores
			de posicao e velocidade.

Entrada:
	GM	-	Produto entre a constante gravitacional e a massa
			central [AU^3/d^2]
	r	-	Posicao heliocentrica em coord. eclipticas [AU]
	v	-	Velocidade heliocentrica em coord. eclipticas [AU/d]
	
Retorna:
	a	-	Semi-eixo maior [AU]
	e	-	Ecentricidade
	i	-	Inclinacao da orbita [rad]
	Omega -	Longitude dos nodos ascendentes [rad]
	omega - Argumento do perihelio [rad]
	M	-	Anomalia media [rad]
'''

	h = np.cross(r,v) # Get vector perpendicular to r and v
	H = np.linalg.norm(h)
	Omega = np.arctan2(h[0],-h[1])
	i = np.arctan2(np.sqrt(h[0]*h[0] + h[1]*h[1]), h[2])
	u = np.arctan2(r[2]*H,-r[0]*h[1]+r[1]*h[0]) # Arg. da latitude

	R = np.linalg.norm(r) # Distancia
	v2 = np.dot(v,v) # velocidade ao quadrado
	a = 1.0 / (2.0/R-v2/GM)
	eCosE = 1.0-R/a
	eSinE = np.dot(r,v)/np.sqrt(GM*a)
	e2 = eCosE*eCosE + eSinE*eSinE
	e = np.sqrt(e2) # Ecentricidade

	E = np.arctan2(eSinE,eCosE) # Anomalia ecentrica
	M = E - eSinE # Anomalia Media
	nu = np.arctan2(np.sqrt(1.0-e2)*eSinE,eCosE-e2) # anomalia verdadeira
	omega = u - nu # arg. do perihelio
	if Omega < 0: Omega += 2.0*np.pi
	if omega < 0: omega += 2.0*np.pi
	if M < 0: M += 2.0*np.pi

	return a,e,i,Omega,omega,M

###########################################################################
