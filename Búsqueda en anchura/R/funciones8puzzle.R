#---------------------------------------------------------------------------
#Función para graficar el rompecabezas ::::::::::::::::::::::::::::::::::::
#---------------------------------------------------------------------------
graph.puzzle=function(m){
    df <- expand.grid(x=1:ncol(m),y=1:nrow(m))
    df$val <- m[as.matrix(df[c('y','x')])]
    par(mar=c(.5,.5,.5,.5))
    plot(x=df$x,y=df$y,pch=as.character(df$val), asp=1,cex=3,xlim=c(0.5,3.5),ylim=c(3.5,0.5),xaxt="n",yaxt="n",xlab="",ylab="",
    xaxs="i", yaxs="i", axes=F)
    abline(v=0.5+(0:3),h=0.5+(0:3))
    }

#------------------------------------------------------------------------
#Función generadora de estados para el rompecabezas ::::::::::::::::::
#--------------------------------------------------------------------------
puzzle.states=function(m){
    p=which(is.na(m),arr.ind=TRUE); #Posición del espacio vacío
    ph=matrix(c(1,0,0,1,-1,0,0,-1)+rep(p,4),nrow=4,byrow=TRUE);#Posiciones a donde se va a mover el espacio vacío
    ph=apply(ph,2,pmin,3); #Corrección de las posiciones para que no sean mayores a 3
    ph=apply(ph,2,pmax,1); #Corrección de las posiciones para que no sean menores a 1
    estados=vector(length=4,mode='list');
    for(i in 1:nrow(ph)){
        e=m;
        e[p[1],p[2]]=e[ph[i,1],ph[i,2]];
        e[ph[i,1],ph[i,2]]=NA;
        estados[[i]]=e;
    }
    return(estados);
}

#---------------------------------------------------------------------------
#Esta función verifica si se llegó al nodo :::::::::::::::::::::::::::::::
#---------------------------------------------------------------------------
finalizar=function(nodo){
                         solucion <- matrix(c(1,2,3,4,5,6,7,8,NA), nrow=3, ncol=3,byrow=TRUE);
                         return(identical(nodo,solucion))
                        }

 #------------------------------------------------------------------------------------
#Heurística (distancia Manhattan)  :::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
d.mah=function(nodo){
                    solucion <- matrix(c(1,2,3,4,5,6,7,8,NA), nrow=3, ncol=3,byrow=TRUE);
                    dist=vector(length=8); #Vector para guardar las distancias
                    for(i in 1:8){
                        dist[i]=sum(abs(which(solucion==i,arr.ind=TRUE)-which(nodo==i,arr.ind=TRUE)));
                        }
                    return(sum(dist))
                    }
#------------------------------------------------------------------------------------
#Heurística (distancia Hamming)  :::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
d.ham=function(nodo){
                    solucion = matrix(c(1,2,3,4,5,6,7,8,NA), nrow=3, ncol=3,byrow=TRUE);
                    comp=nodo==solucion #Comparación entre las matrices
                    dist=8-length(which(comp==TRUE)) #Suma el número de falsos
                    return(dist)
                    }

 
