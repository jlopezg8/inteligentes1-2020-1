#=================================================================================
#Clase 5: B�squeda con adversarios ///////////////////////////////////////////////
#=================================================================================
rm(list=ls())
source('funcionestriki.R',encoding='iso8859-15')
#------------------------------------------------------------------------------------
#Funci�n para calcular la utilidad de un determinado estado en el triki :::::::::::::
#------------------------------------------------------------------------------------
#Esta funci�n considera por defecto al jugador con la x
util.triki=function(m,max='x'){
    library(pracma)
    p=which(m==max,arr.ind=TRUE); #Posici�n de los espacios con la marca seleccionada
    if(nrow(p)>0){
        if(max(table(p[,1]))>=3){return(1)} #Si hay tres o m�s filas repetidas, devuelve 1
        if(max(table(p[,2]))>=3){return(1)} #Si hay tres o m�s columnas repetidas, devuelve 1
        if(length(which(diag(m)==max))==3){return(1)} #Verifica la diagonal principal
        if(length(which(diag(rot90(m))==max))==3){return(1)} #Verifica la diagonal principal de la matriz rotada 90 grados
        }
    p=which(m!=max,arr.ind=TRUE); #Posici�n de los espacios con la marca contraria
    if(nrow(p)>0){
        if(max(table(p[,1]))>=3){return(-1)} #Si hay tres o m�s filas repetidas, devuelve -1
        if(max(table(p[,2]))>=3){return(-1)} #Si hay tres o m�s columnas repetidas, devuelve -1
        if(length(which(diag(m)!=max))==3){return(-1)} #Verifica la diagonal principal
        if(length(which(diag(rot90(m))!=max))==3){return(-1)} #Verifica la diagonal principal de la matriz rotada 90 grados
        }
    return(0)
    }   

#------------------------------------------------------------------------------------
#Funci�n para calcular el valor min-max de un estado ::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
# Esta funci�n supone que 'x' es max y 'o' es min
# Supone que el turno es de 'x'
minmax=function(m,max='x',turno='x'){
    if(turno=='x'){siguiente='o'}
    if(turno=='o'){siguiente='x'}
    
    util.actual=util.triki(m,max=max);
    if(util.actual!=0){ #Si la utilidad del estado es diferente de cero, es una hoja
        #print(m)
        return(util.actual);
    }
    if(is.null(triki.states(m))){ #Si el estado ya tiene todas las posiciones llenas, es una hoja
        #print(m)
        return(util.actual)
    }else{
        utilidades=c();
        estados=triki.states(m,turno=turno);
        for(i in 1:length(estados)){
            u=minmax(estados[[i]],max=max,turno=siguiente);
            utilidades=c(utilidades,u);
            }
        if(turno==max){
            return(max(utilidades))
        }else{
            return(min(utilidades))
        }
    }
}
    
#------------------------------------------------------------------------------------
#Rutina principal del algoritmo min-max :::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
    
m=matrix(c(NA,NA,NA,NA,'x',NA,NA,NA,NA),ncol=3,byrow=TRUE);
graph.triki(m)
cond=1
while(cond==1){
    m=fetch.triki(m,turno='o')  #Jugador real
    graph.triki(m)
    u=util.triki(m,max='x')
    if(u!=0){ 
        Sys.sleep(3)
        break;
    }
    if(is.null(triki.states(m))){ 
        Sys.sleep(3)
        break;
        }
    t=system.time({    
        m=triki.states(m)[[which.max(sapply(triki.states(m,turn='x'),minmax,turno='o'))]] #M�quina
    })
    print(t)
    graph.triki(m)
    u=util.triki(m,max='x')
    if(u!=0){ 
        Sys.sleep(3)
        break;
    }
    if(is.null(triki.states(m))){ 
        Sys.sleep(2)
        break;
        }
    }
 
#------------------------------------------------------------------------------------
#Poda alpha-beta ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
# Esta funci�n supone que 'x' es max y 'o' es min
# Supone que el turno es de 'x'
alphabeta=function(m,max='x',turno='x',alpha=-Inf,beta=Inf){
    if(turno=='x'){siguiente='o'}
    if(turno=='o'){siguiente='x'}
    
    util.actual=util.triki(m,max=max);
    if(util.actual!=0){ #Si la utilidad del estado es diferente de cero, es una hoja
        #print(m)
        return(util.actual);
    }
    if(is.null(triki.states(m))){ #Si el estado ya tiene todas las posiciones llenas, es una hoja
        #print(m)
        return(util.actual)
    }else{
        if(turno==max){
            utilidades=c();
            estados=triki.states(m,turno=turno);
            for(i in 1:length(estados)){
                u=alphabeta(estados[[i]],max=max,turno=siguiente,alpha=alpha,beta=beta);
                utilidades=c(utilidades,u);
                if(u>=beta){
                    break #Se suspende la b�squeda
                }
                alpha=max(c(utilidades,alpha));    
            }
            return(max(utilidades))
        }else{
            utilidades=c();
            estados=triki.states(m,turno=turno);
            for(i in 1:length(estados)){
                u=alphabeta(estados[[i]],max=max,turno=siguiente,alpha=alpha,beta=beta);
                utilidades=c(utilidades,u);
                if(u<=alpha){
                    break #Se suspende la b�squeda
                }
                beta=min(c(utilidades,beta));
            }
            return(min(utilidades))
        }
    }
}

#------------------------------------------------------------------------------------
#Rutina principal del algoritmo alpha-beta :::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
m=matrix(c(NA,NA,NA,NA,NA,NA,NA,NA,NA),ncol=3,byrow=TRUE);
graph.triki(m)
cond=1
while(cond==1){
      m=fetch.triki(m,turno='o')  #Jugador real
    graph.triki(m)
    
    u=util.triki(m,max='x')
    if(u!=0){ 
        Sys.sleep(2)
        break;
    }
    if(is.null(triki.states(m))){ 
        Sys.sleep(2)
        break;
        }
    t=system.time({
        m=triki.states(m)[[which.max(sapply(triki.states(m,turn='x'),h.alphabeta,turno='o'))]] #M�quina
    })
    print(t)
    graph.triki(m)
    
    u=util.triki(m,max='x')
    if(u!=0){ 
        Sys.sleep(2)
        break;
    }
    if(is.null(triki.states(m))){ 
        Sys.sleep(2)
        break;
        }
    }
