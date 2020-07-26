
#------------------------------------------------------------------------------------
#Funci�n para hacer movimientos en el 2048 :::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
mover=function(m,move='down'){
    library(pracma)
    if(move=='right'){m=rot90(m,k=3)}
    if(move=='up'){m=rot90(m,k=2)}
    if(move=='left'){m=rot90(m,k=1)}
    for(j in 1:4){ #Columnas
        for(i in 3:1){ #Filas
             for(k in i:3){
                 if(m[k+1,j]==0){
                     m[k+1,j]=m[k,j];
                     m[k,j]=0;
                     }
                 }
             }
        for(i in 4:2){ #Filas
                if(m[i,j]==m[i-1,j]){
                     m[i,j]=2*m[i,j];
                     m[i-1,j]=0;
                     }
                 }
        for(i in 3:1){ #Filas
             for(k in i:3){
                 if(m[k+1,j]==0){
                     m[k+1,j]=m[k,j];
                     m[k,j]=0;
                     }
                 }
             }
        }
    if(move=='right'){m=rot90(m,k=1)}
    if(move=='up'){m=rot90(m,k=2)}
    if(move=='left'){m=rot90(m,k=3)}
    return(m)
    }
#------------------------------------------------------------------------------------
#Funci�n para generar un nuevo valor aleatorio :::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
gnv=function(m){
    libres=which(m==0);
    if(length(libres)>0){ #Si no hay posiciones libres, retorna el mismo elemento
        if(length(libres)>1)
            {
            pos=sample(libres,1)
        }else{
            pos=libres;
        }
        #if(runif(1)<0.25){
        #    m[pos]=4;
        #}else{
        m[pos]=2;
        #}
        }
    return(m);
}    

#------------------------------------------------------------------------------------
#Funci�n para graficar el 2048 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
#install.packages('raster', INSTALL_opts="--no-multiarch")
#install.packages('raster')
graph.2048=function(m){
    library(raster)
    m[m==0]=NA
    rm=raster(m)
    plot(rm,legend=FALSE,axes=FALSE)
    text(rm,digits=4)
    }
#------------------------------------------------------------------------------------
#Funci�n generadora de estados para el 2048 ::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
dco.states=function(m){
    mv=c('down','left','right','up');
    estados=vector(mode='list',length=4)
    for(i in 1:4){
        estados[[i]]=mover(m,move=mv[i])
    }
    estados=unique(estados);
    estados=setdiff(estados,list(m))
    return(estados)
}
#------------------------------------------------------------------------------------
#Funci�n generadora de estados aleatorios para el 2048 :::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
gnv.states=function(m){
    libres=which(m==0);
    if(length(libres)>0){
        estados=vector(length=length(libres),mode='list')
        for(i in 1:length(libres)){
            m1=m;
            m1[libres[i]]=2;
            estados[[i]]=m1;
            }
        return(estados)
    }else{
        return(list(m));
        }
    }
    
