#------------------------------------------------------------------------------------
#Rutina principal greedy search ::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------                        
source('funciones8puzzle.R',encoding='iso8859-15')
m <- matrix(c(5,1,2,NA,7,3,6,4,8), nrow=3, ncol=3,byrow=TRUE)
#graph.puzzle(m)

frontera=list(m); #Nodos por visitar
visitados=list(); #Nodos visitados
fh=d.mah; #Funci�n heur�stica
heur=fh(m);
padresf=list(NA);
padres=list()
cond=0;
pasos=0;

while(cond==0){
        nodo=frontera[[1]];
        padres=c(padres,padresf[1]); #Registra el padre por el que se lleg� a ese nodo
        visitados=c(visitados,list(nodo)); #Se agrega el nodo a la lista de visitados
        if(fh(nodo)==0){ #Termina cuando la distancia al nodo evaluado es cero
            salida=nodo;
            cond=1
            break;
        }
        frontera=frontera[-1];
        padresf=padresf[-1];
        heur=heur[-1];
        vecinos=puzzle.states(nodo);
        hijos=setdiff(vecinos,c(visitados,frontera)); #Hijos del nodo que se est� analizando
        heur.hijos=sapply(hijos,fh);
        #Actualizaciones
        if(length(hijos)!=0){
            frontera=c(frontera,hijos); #Se agregan los hijos a la frontera
            padresf=c(padresf,rep(list(nodo),length(hijos)))
            heur=c(heur,heur.hijos); #Se agregan las heur�sticas de los hijos
            orden=order(heur); #Nuevo orden
            frontera=frontera[orden];
            padresf=padresf[orden];
            heur=heur[orden];
        }else{
            print('Camino cerrado')
        }
        pasos=pasos+1;
        print(pasos);
        }

#------------------------------------------------------------------------------------
#Rutina para encontrar la ruta que sigui� el algoritmo a partir de los padres :::::::
#------------------------------------------------------------------------------------
cond=0;
nodo=visitados[[length(visitados)]]; #La ruta empieza con el �ltimo nodo visitado
ruta=list(nodo);
while(cond==0){
    nodo=padres[[which(sapply(visitados,identical,nodo))]];
    if(all(is.na(nodo))){
        break;
        }
    ruta=c(ruta,list(nodo));    
    }
ruta=ruta[length(ruta):1]
#------------------------------------------------------------------------------------
#Gr�ficas ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------
for(i in 1:length(ruta)){
    graph.puzzle(ruta[[i]]);
    Sys.sleep(0.3)
}
