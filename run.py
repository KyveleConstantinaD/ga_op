import GaOp as ga  
import export_excel
import matplotlib.pyplot as plt
import globfile as g
import pois_in_plot as pl


def run(runSet, initialPopulation, parentSelection): 
    
    # set variables based on dataset selected by the user
    iterations=30

    if runSet ==130:
        files='Sets/set_130.txt'
        t_list=[50,100,150,200,250,300,350,400,410]
        start=1-1 #poi numbering in the system starts from 0
        end=2-1 #poi numbering in the system starts from 0
        numOfPois=130
        iterations=20
        
            
    if runSet == 1:
        files='Sets/tsiligirides_1_correct.txt'
        t_list=[5,10,15,20,25,30,35,40,46,50,55,60,65,70,73,75,80,85]
        start=1-1 #poi numbering in the system starts from 0
        end=32-1 #poi numbering in the system starts from 0
        numOfPois=32

    
    if runSet == 2:
        files='Sets/tsiligirides_2.txt'
        t_list=[15,20,23,25,27,30,32,35,38,40,45]
        start=1-1 #poi numbering in the system starts from 0
        end=21-1 #poi numbering in the system starts from 0
        numOfPois=21
        
        
    print(f"Running for selected data set: {files}")
    print(f"Initial population generation method selected: {initialPopulation}")
    print(f"Parent selection method chosen: {parentSelection}")

    # create list of tuples with all pois in file for ga 
    f = open( files )
    pois = []
    an_unused_value = f.readline() # ignore first line of file
    for i in range( numOfPois ):
        pois.append(tuple( [ float( x ) for x in f.readline().split() ] + [ i ] ) )
    
    # initialise lists and variables
    avg_score=[]
    avg_distance=[]
    scores=[]
    distances=[]
    routes_excel=[]
    avg_gen=[]
    gen=[]
    cpu_time=[]
    avg_cpu=[]
    list_p_time=[]
    sum_distance=0
    sum_score=0
    sum_gen=0
    sum_cpu=0
    fist_found=[]
    found_in=[]   
    excel_index=0
    
    # run for each tmax given by the dataset
    for i in t_list:
        routes=[]
        sum_score=0
        sum_distance=0
        sum_gen=0
        sum_cpu=0
        runs=[]
        parent_time=[]
        best_history=[]
        best_similar=[]
        flat_best=[]
        atest=[]
        aaa=[]
        print(f"Running for t = {i}")
    
        # run for number of iterations set by the dataset/literature
        for j in range(iterations):
            print(f"Iteration i = {j}, tmax = {i}")
    
            # run genetic algorithm and retrive 100 solutions
            routes.append(ga.genetic_alg(pois,numOfPois, i, start , end, initialPopulation, parentSelection))
            
            # collect data for excel export
            iter_cpu_time=g.end_time[routes[j][3]]-g.start_time
            runs.append(j) #delete
            
            routes[j].append(iter_cpu_time)
            routes[j].append(j)
            sum_score+=routes[j][0]
            sum_distance+=routes[j][2]
            sum_gen+=routes[j][3]
            sum_cpu+=iter_cpu_time
                        
            atest.append([j,g.testtest])
            
            
            parent_time.append(sum(g.parent_e_time[0:routes[j][3]])-sum(g.parent_s_time[0:routes[j][3]]))

        # sort routes : Score Descending, Route cost ascending
        # select best
        
        # out of the solutions given by the ga select the best
        routes.sort(key=lambda x: (-x[0], x[2]))
    
        # update data for excel export
        cpu_time.append(routes[0][4])
        scores.append(routes[0][0])
        distances.append(routes[0][2])
        gen.append(routes[0][3]+1) # generations start from 0
        routes_excel.append([x[3]+1 for x in routes[0][1]])
        avg_score.append(sum_score/iterations)
        avg_distance.append(sum_distance/iterations)
        avg_gen.append(sum_gen/iterations)
        avg_cpu.append(sum_cpu/iterations)
        
        # caclulate data for outputs    
        best_history=atest[routes[0][5]][1] 
    
        best_similar=[]
        # best_similar.sort(key=lambda x: (x[2], x[0]))
        for hg in best_history:
            for sb in hg[1]:
                # print(hg[0])
                if sb[0]==routes[0][0]:
                    best_similar.append([hg[0], sb[0],sb[2],[x[3] for x in sb[1]]])
        best_similar.sort(key=lambda x: (x[0]))
    
        unique_combinations = {}
        
        # Iterate through the original list
        for sublist in best_similar:
            key = tuple(sublist[:2])  # Use the first two numbers as the key
            if key not in unique_combinations:
                unique_combinations[key] = sublist
                
        unique_best_similar=[]
        # Convert the dictionary values back to a list
        unique_best_similar = list(unique_combinations.values())
        
        flat_best=[routes[0][0],routes[0][2],[x[3] for x in routes[0][1]]]
        aaa=[x for x in unique_best_similar if x[1:4]==flat_best]
        fist_found.append(aaa[0][0]+1)
        found_in.append(routes[0][5])
        list_p_time.append(parent_time[excel_index])
     
              
        # create plot with best solution
        pl.plot_pois(pois, [x[3] for x in routes[0][1]], i, files)
    
        # export excel file for each tmax of the dataset
        export_excel.create_excel_file([avg_score[excel_index]], [avg_distance[excel_index]], [scores[excel_index]],
                                       [distances[excel_index]], [routes_excel[excel_index]], [[t_list[excel_index]]] , files, [avg_gen[excel_index]],
                                       [gen[excel_index]], [cpu_time[excel_index]],[avg_cpu[excel_index]], [parent_time[excel_index]],[aaa[0][0]+1],[routes[0][5]],i)
        excel_index+=1
    
    # export consolidated excel file
    export_excel.create_excel_file(avg_score, avg_distance, scores, 
                                    distances, routes_excel, t_list ,files, avg_gen, gen, cpu_time, avg_cpu, list_p_time, fist_found, found_in, 'all data')
