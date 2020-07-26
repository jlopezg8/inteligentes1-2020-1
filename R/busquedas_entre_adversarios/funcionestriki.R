#------------------------------------------------------------------------------------
#Función para graficar el triki :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
graph.triki=function(m){
    df <- expand.grid(x=1:ncol(m),y=1:nrow(m))
    df$val <- m[as.matrix(df[c('y','x')])]
    par(mar=c(.5,.5,.5,.5))
    plot(x=df$x,y=df$y,pch=as.character(df$val), asp=1,cex=3,xlim=c(0.5,3.5),ylim=c(3.5,0.5),xaxt="n",yaxt="n",xlab="",ylab="",
    xaxs="i", yaxs="i", axes=F)
    abline(v=0.5+(0:3),h=0.5+(0:3))
    }

#------------------------------------------------------------------------------------
#Función para escribir en el triki :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------

fetch.triki=function(m,turno='x'){
    graph.triki(m); #Primero se grafica el triki
    coordenadas=locator(1);
    x=0.5+(0:3);
    y=0.5+(0:3); #Posiciones de las lineas horizontales y verticales
    columna=max(which(coordenadas$x>x));
    fila=max(which(coordenadas$y>y));
    m[fila,columna]=turno;
    return(m);
    }
    
#------------------------------------------------------------------------------------
#Función generadora de estados para el triki :::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
#(Esta función considera por defecto al jugador con la x)
triki.states=function(m,turno='x'){
    p=which(is.na(m)); #Posición de los espacios vacíos
    if(length(p)>0){
        estados=vector(length=length(p),mode='list');
        for(i in 1:length(p)){
            e=m;
            e[p[i]]=turno;
            estados[[i]]=e;
            }
        return(estados);
    }else{
        return(NULL);
    }
}
 
