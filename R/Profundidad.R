source('funciones8puzzle.R',encoding='iso8859-15')
#------------------------------------------------------------------------------------
#Rutina principal profundidad:::::::::::::::::::::::::::::::::::::::::::::::::::
#------------------------------------------------------------------------------------                        
m <- matrix(c(5,1,2,NA,7,3,6,4,8), nrow=3, ncol=3,byrow=TRUE)
#graph.puzzle(m)

cond=2;
pasos=0;
profundidad <- 1;
while (cond == 2) {
    frontera=list(m); #Nodos por visitar
    visitados=list(); #Nodos visitados
    pendientes=c(1); #Vector que almacena el n�mero de hijos pendientes por visitar para cada nodo en la lista de visitados
    #padres=list();
    cond = 0;
    print(c('Profundidad ', profundidad));
    while(cond==0){
            pasos=pasos+1;
            print(pasos);
            nodo=frontera[[length(frontera)]]; ##Aqu� cambia el algoritmo. Se usa primero el �ltimo de la frontera
            frontera=frontera[-length(frontera)]; ##Se remueve de la frontera
            pendientes[length(pendientes)]=pendientes[length(pendientes)]-1;  
            visitados[[length(visitados)+1]]=nodo;
            vecinos=puzzle.states(nodo);
            
            if (length(visitados)>=profundidad){
                hijos=list()
            }else{
                hijos=setdiff(vecinos,c(visitados,frontera));
                }
            
            pendientes[length(pendientes)+1]=length(hijos); ##Se agrega el n�mero de hijos pendientes por expandir
            #padres=c(padres,rep(list(nodo),length(hijos)));
            prueba=unlist(lapply(hijos,finalizar));
            if(any(prueba)){
                salida=hijos[which(prueba)];
                cond=1;
                }
            if(pendientes[length(pendientes)]==0){ ##Si ya se expandieron todos los hijos de un nodo, se remueve
                while(pendientes[length(pendientes)]==0){
                    print('Removiendo rama')
                    visitados=visitados[-length(visitados)];
                    pendientes=pendientes[-length(pendientes)];
                    if (length(pendientes) == 0) {
                        cond = 2;
                        break;
                    }
                }
            }else{
                frontera=c(frontera,hijos)
                }
            }
    profundidad = profundidad + 1;
}

ruta=c(visitados,salida)
for(i in 1:length(ruta)){
    graph.puzzle(ruta[[i]]);
    Sys.sleep(1)
}
