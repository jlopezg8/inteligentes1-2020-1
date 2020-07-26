#================ Experimentos 8-Puzzle=============================================

source('funciones8puzzle.R',encoding='iso8859-15')

#------------------------------------------------------------------------------------
#Rutina principal anchura::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------                  
m <- matrix(c(5,1,2,NA,7,3,6,4,8), nrow=3, ncol=3,byrow=TRUE)
graph.puzzle(m)

frontera=list(m); #Nodos por visitar
visitados=list(); #Nodos visitados
padres=list();
cond=0;
pasos=0;
while(cond==0){
        pasos=pasos+1;
        print(pasos);
        nodo=frontera[[1]]; #Se toma el primer elemento de la frontera
        frontera=frontera[-1]; #Quitar el primer elemento de la frontera
        visitados[[length(visitados)+1]]=nodo; #Ingresamos el nodo a la lista de visitados
        vecinos=puzzle.states(nodo);
        hijos=setdiff(vecinos,c(visitados,frontera));
        padres=c(padres,rep(list(nodo),length(hijos)));
        prueba=unlist(lapply(hijos,finalizar));
        if(any(prueba)){
            salida=hijos[which(prueba)]; #La salida ser� el hijo que est� en la posici�n para la cual finalizar fue TRUE
            cond=1;
            }
        frontera=c(frontera,hijos) #Se agregan los hijos a la frontera
        }

#------------------------------------------------------------------------------------
#Rutina para encontrar la ruta que sigui� el algoritmo a partir de los padres :::::::
#------------------------------------------------------------------------------------
cond=0;
nodo=visitados[[length(visitados)]]; #La ruta empieza con el �ltimo nodo visitado
ruta=list(nodo);
while(cond==0){
    nodo=padres[[which(sapply(visitados,identical,nodo))-1]];
    ruta=c(ruta,list(nodo));
    if(identical(nodo,list(m))){
        cond=1;
        }
    }
ruta=c(salida,ruta)
ruta=ruta[length(ruta):1]

#------------------------------------------------------------------------------------
#Gr�ficas ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
for(i in 1:length(ruta)){
    graph.puzzle(ruta[[i]]);
    Sys.sleep(1)
}

