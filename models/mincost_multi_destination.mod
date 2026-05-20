/**********************/
/* Declare index sets */
/**********************/
set NODES;
set EDGES within (NODES cross NODES);
set BUSES;
set ROUTE{BUSES} within EDGES;
set DESTINATIONS within NODES;

/**********************/
/* Declare parameters */
/**********************/

/* Coordinates */

param coord{NODES, {'long', 'lat'}};

param unitcost := .10;  

param pi := 3.14159265358979;
param R := 6371;            # mean radius of the Earth in km

param a{(i,j) in EDGES} := 
              sin(pi*( (coord[i,'lat'] - coord[j,'lat'])/2 )/180)^2 + 
              (
              cos(pi*coord[i,'lat']/180) * 
              cos(pi*coord[j,'lat']/180) * 
              sin(pi*( (coord[i,'long'] - coord[j,'long'])/2 )/180)^2
              ) ;

param dist{(i,j) in EDGES} := 
              2*R*atan( sqrt(a[i,j]), sqrt(1-a[i,j]) );

param cost{(i,j) in EDGES} := unitcost * dist[i,j];

param demand {NODES, DESTINATIONS} default 0;

param output_file symbolic;

/* Capacity */

/* Compute capacity of each edge using freq and load of buses */
param freq{BUSES};          # number of buses per hour
param load{BUSES};          # number of passengers per bus

param capacity{(i,j) in EDGES} :=
    sum{b in BUSES : (i,j) in ROUTE[b] or (j,i) in ROUTE[b]} 
        freq[b] * load[b];  # number of passengers per hour

/***************************************/
/* Form and solve optimization problem */
/***************************************/

/* Declare variables */
# var Flow{(i,j) in EDGES} >=0, <= capacity[i,j];
var Flow{EDGES, DESTINATIONS} >=0;


/* Declare objective function */
minimize total_cost: sum{(i,j) in EDGES, k in DESTINATIONS} cost[i,j] * Flow[i,j,k];

/* Declare constraints */

subject to flow_conservation {i in NODES, k in DESTINATIONS}:
    + sum{(j,i) in EDGES} Flow[j,i,k]  
    - sum{(i,j) in EDGES} Flow[i,j,k]  
    == demand[i,k];

subject to capacity_constraint {(i,j) in EDGES}:
    sum{k in DESTINATIONS} Flow[i,j,k] <= capacity[i,j];

/* Solve the optimization problem */
solve;

/****************/
/* Print output */
/****************/

/* Output solution to output_file */

printf "%20s%20s%16s%16s%16s%16s\n", 'i', 'j', 'k' , 'Flow', 'capacity' , 'Dual' > output_file;
printf{(i,j) in EDGES, k in DESTINATIONS}: "%20s%20s%16s%16.0f%16.0f%16.4f\n", 
    i, j, k, Flow[i,j,k], capacity[i,j], capacity_constraint[i,j].dual >> output_file;
printf "Wrote solution to %s\n", output_file;


/* Output total cost */

printf "Total cost: %16.4f $\n", total_cost;


/****************/
/* End of model */
/****************/
end;
