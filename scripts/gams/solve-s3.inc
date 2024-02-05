* --- iterative approach to find the optimal pi_hr ---
Set VARS    /'pi_hr', 'ShareCold', 'obj'/;
Set IDX     /'pi_hr'/;
Set ITER_I  /I00*I200/;

PARAMETERS
StartValue(IDX)
StepsValue(IDX)
fixedValue(ITER_I)
logResults(ITER_I, VARS)
minObjValue
;

StartValue('pi_hr') = 11.5;
StepsValue('pi_hr')  = 0.01;

fixedValue(ITER_I) = StartValue('pi_hr') + (ord(ITER_I)-1)*StepsValue('pi_hr');

loop(ITER_I,
    pi_hr.fx                        = fixedValue(ITER_I);
    solve all_eqs using MIP minimizing obj;

    logResults(ITER_I,'pi_hr')      = pi_hr.l;
    logResults(ITER_I,'ShareCold')  = sum(T, x_c.l(T,'HP_EHR'))/sum(T, D_c(T));
    logResults(ITER_I,'obj')        = obj.l;
)
;

minObjValue = smin(ITER_I, logResults(ITER_I,'obj'));
pi_hr.fx    = sum(ITER_I$(logResults(ITER_I,'obj') = minObjValue), fixedValue(ITER_I));

solve all_eqs using MIP minimizing obj;