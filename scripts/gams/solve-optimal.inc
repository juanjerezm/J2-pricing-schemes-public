* NOT IMPLEMENTED FOR S5, SPECIAL CONDITIONS FOR S2 NOT REQUIRED

$ifi %case% == C1 $ifi %scenario% == S3  pi_hr.fx       = 13.8;
$ifi %case% == C1 $ifi %scenario% == S4  pi_alpha_0.fx  =  6.0;
$ifi %case% == C1 $ifi %scenario% == S4  pi_alpha_1.fx  =  0.3;

$ifi %case% == C2 $ifi %scenario% == S3  pi_hr.fx       = 12.5;
$ifi %case% == C2 $ifi %scenario% == S4  pi_alpha_0.fx  = 19.8;
$ifi %case% == C2 $ifi %scenario% == S4  pi_alpha_1.fx  = -0.6;

solve all_eqs using MIP minimizing obj;