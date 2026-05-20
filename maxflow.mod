/**********************/
/* Declare index sets */
/**********************/
set NODES;
set EDGES within (NODES cross NODES);
set BUSES;
set ROUTE{BUSES} within EDGES;
set S;
set T;

/**********************/
/* Declare parameters */
/**********************/

/* Source and sink */



/* Capacity */

/* Compute capacity of each edge using freq and load of buses */
param freq{BUSES};          # number of buses per hour
param load{BUSES};          # number of passengers per bus

param capacity{(i,j) in EDGES} :=
    sum{b in BUSES : (i,j) in ROUTE[b] or (j,i) in ROUTE[b]} 
        freq[b] * load[b];  # number of passengers per hour

/* Coordinates */

param coord{NODES, {'long', 'lat'}};

/* Output file */

param outfile symbolic default "outputs/sol_maxflow_baseline.txt";


/***************************************/
/* Form and solve optimization problem */
/***************************************/

/* Declare variables */
var Flow{(i,j) in EDGES} >=0, <= capacity[i,j];
var f >=0;

/* Declare objective function */
maximize total_flow: f;

/* Declare constraints */
subject to source_flow:
    + sum{(j,i) in EDGES : i in S} Flow[j,i]  
    - sum{(i,j) in EDGES : i in S} Flow[i,j]  
    == -f;
subject to sink_flow:
    + sum{(j,i) in EDGES : i in T} Flow[j,i]  
    - sum{(i,j) in EDGES : i in T} Flow[i,j]  
    == f;
subject to flow_conservation {i in NODES diff (S union T)}:
    + sum{(j,i) in EDGES} Flow[j,i]  # Flow entering i
    - sum{(i,j) in EDGES} Flow[i,j]  # Flow leaving i
    == 0;

/* Solve the optimization problem */
solve;


/****************/
/* Print output */
/****************/

/* Output solution */

printf "%20s%20s%16s%16s\n", 'i', 'j', 'Flow', 'capacity' > outfile;
printf{(i,j) in EDGES}: "%20s%20s%16.0f%16.0f\n", 
    i, j, Flow[i,j], capacity[i,j] >> outfile;
printf "Wrote solution to %s\n", outfile;

/* Output total flow into each sink and out of each source */

printf "SOURCE flow:\n";
printf{i in S} "%20s%16.0f\n", i, -sum{(i,j) in EDGES} Flow[i,j]; 

printf "SINK flow:\n";
printf{i in T} "%20s%16.0f\n", i, sum{(j,i) in EDGES} Flow[j,i]; 

/* Output total flow */

printf "Total flow: %d passengers/hour\n", total_flow;


/****************/
/* End of model */
/****************/
end;
