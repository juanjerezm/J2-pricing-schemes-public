* --- iterative approach to find the optimal pi_hr ---
Set VARS    /'pi_hr', 'pi_alpha_0', 'pi_alpha_1', 'ShareCold', 'obj'/;
Set IDX     /'pi_alpha_0', 'pi_alpha_1'/;
Set ITER_I  /I00*I20/;
set ITER_J  /J00*J20/;


PARAMETERS
StartValue(IDX)
StepValue(IDX)
fixedValue_I(ITER_I)
fixedValue_J(ITER_J)
logResults(ITER_I, ITER_J,VARS)
minObjValue

filter_check
;

StartValue('pi_alpha_0') = 0;
StartValue('pi_alpha_1') = -2.5;
StepValue('pi_alpha_0')  = 1;
StepValue('pi_alpha_1')  = 0.25;

fixedValue_I(ITER_I) = StartValue('pi_alpha_0') + (ord(ITER_I)-1)*StepValue('pi_alpha_0');
fixedValue_J(ITER_J) = StartValue('pi_alpha_1') + (ord(ITER_J)-1)*StepValue('pi_alpha_1');

loop((ITER_J,ITER_I),
*   a
    filter_check = fixedValue_I(ITER_I) + fixedValue_J(ITER_J) * 11.4355654761905 * 1;
    continue$(filter_check < -18 OR filter_check > 40);

    pi_alpha_0.fx = fixedValue_I(ITER_I);
    pi_alpha_1.fx = fixedValue_J(ITER_J);

    solve all_eqs using MIP minimizing obj;

    logResults(ITER_I,ITER_J,'pi_hr')       = sum(DD,pi_hr.l(DD))/sum(DD,1);
    logResults(ITER_I,ITER_J,'pi_alpha_0')  = pi_alpha_0.l;
    logResults(ITER_I,ITER_J,'pi_alpha_1')  = pi_alpha_1.l;
    logResults(ITER_I,ITER_J,'ShareCold')   = sum(T, x_c.l(T,'HP_EHR'))/sum(T, D_c(T));
    logResults(ITER_I,ITER_J,'obj')         = obj.l;
);

minObjValue     = smin((ITER_I,ITER_J)$logResults(ITER_I,ITER_J,'obj'), logResults(ITER_I,ITER_J,'obj'));

pi_alpha_0.fx   = sum((ITER_I,ITER_J)$(logResults(ITER_I, ITER_J,'obj') = minObjValue), fixedValue_I(ITER_I));
pi_alpha_1.fx   = sum((ITER_I,ITER_J)$(logResults(ITER_I, ITER_J,'obj') = minObjValue), fixedValue_J(ITER_J));

solve all_eqs using MIP minimizing obj;