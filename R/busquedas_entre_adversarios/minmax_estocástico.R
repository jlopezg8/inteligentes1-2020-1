#================================================================================
#Clase 6: Juegos estoc�sticos  ////////////////////////////////////////////
#================================================================================
rm(list=ls())
source('funciones2048.R',encoding='iso8859-15')
#------------------------------------------------------------------------------------
#Ciclo para que juegue un humano ##S�lo funciona en consola#####
#------------------------------------------------------------------------------------
#install.packages('keypress')
library(keypress)
m=matrix(rep(0,16),nrow=4)
m[sample(16,2)]=2

cond=1
while(cond==1){
    graph.2048(m)
    Sys.sleep(0.1);
    movimiento=keypress(block=TRUE)
    m=mover(m,move=movimiento);
    m=gnv(m);
    }
        
#------------------------------------------------------------------------------------
#Funci�n para determinar la utilidad dl 2048 :::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
util.2048=function(m){
    return(length(which(m==0)) + log2(max(m))) #En cada paso maximiza el n�mero de posiciones vac�as
}

#------------------------------------------------------------------------------------
#Funci�n para calcular el valor min-max de un estado (con cut-off) :::::::::::::::::::
#------------------------------------------------------------------------------------

minmax=function(m,max='jugador',turno='jugador',llamados=0){
    if(turno=='jugador'){siguiente='rand'}
    if(turno=='rand'){siguiente='jugador'}
    
    util.actual=util.2048(m);
    if(llamados>=3){
        return(util.actual)
    } 
    if(length(dco.states(m))==0){ #Si el estado ya tiene todas las posiciones llenas, es una hoja
        #print(m)
        return(util.actual)
    }else{
        if(turno==max){
            utilidades=c();
            estados=dco.states(m);
            for(i in 1:length(estados)){
                u=minmax(estados[[i]],max=max,turno=siguiente,llamados=llamados+1);
                utilidades=c(utilidades,u);
            }
            return(max(utilidades))
        }else{
            utilidades=c();
            estados=gnv.states(m);
            for(i in 1:length(estados)){
                u=minmax(estados[[i]],max=max,turno=siguiente,llamados=llamados+1);
                utilidades=c(utilidades,u);
            }
            return(mean(utilidades))
        }
    }
}
    
#------------------------------------------------------------------------------------
#Rutina principal del algoritmo min-max :::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------

m=matrix(rep(0,16),nrow=4)
m[sample(16,2)]=2
graph.2048(m);
cond=1;
while(cond==1){
    t=system.time({    
        m=dco.states(m)[[which.max(sapply(dco.states(m),minmax,turno='rand'))]] #M�quina
    })
    print(t)
    graph.2048(m);
    ss=dco.states(m)
    if(length(ss)==0){
        Sys.sleep(3)
        break;
    }
    m=gnv(m);
    graph.2048(m);
    ss=dco.states(m)
    if(length(ss)==0){ 
        Sys.sleep(3)
        break;
    }
}
