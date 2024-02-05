# Grid search logbook


## Case 1
### S3
Each iteration fixes the value of pi_hr and solves the rest of the problem, according to the specifications in the table below.

| Attribute             | First Pass       | Second Pass      | Third Pass              |
|-----------------------|------------------|------------------|-------------------------|
| Start value           | 0                | 9                | 13                      |
| Step value            | 1                | 0.1              | 0.01                    |
| End value             | 50               | 19               | 16                      |
| Iterations            | 52               | 102              | 302                     |
| Solving time          | 00:05:55         | 00:13:05         | 00:38:20                |
| Time per iteration    | 6.83 s           | 7.70 s           | 7.62 s                  |
| Optimal value         | 14               | 13.8             | 13.74 / 13.7 / 13.78    |
| Percentile of interest| 20%              | 20%              | N/A                     |
| Prices of interest    | 9 - 19           | 13 - 16          | N/A                     |


**Comment**: Due to the model's 6-digit numerical precision, objective values can be resolved only to the nearest 10€. Consequently, in the third pass, multiple prices (13.74, 13.77, 13.78) appear optimal. Further refining the search is futile without increased precision.

**_Conclusion_**: For simplicity, the second pass is chosen as the optimal solution, with pi_hr = 13.8€.

### S4
Not written here, check excel file.

## Case 2
### S3

| Attribute             | First Pass       | Second Pass      | Third Pass              |
|-----------------------|------------------|------------------|-------------------------|
| Start value           | 0                | 11               | 11.5                    |
| Step value            | 1                | 0.1              | 0.01                    |
| End value             | 50               | 20               | 13.5                    |
| Iterations            | 52               | 92               | 202                     |
| Solving time          | 00:07:07         | 00:09:15         | 00:21:29                |
| Time per iteration    | 8.21 s           | 6.03 s           | 6.38 s                  |
| Optimal value         | 12               | 12.5             | 12.42                   |
| Percentile of interest| 20%              | 20%              | N/A                     |
| Prices of interest    | 11 - 20          | 11.5 - 13.5      | N/A                     |

**Comment**: In this case, the optimal value is 12.42.
**_Conclusion_**: Second pass (12.5€) or third pass (12.42€)?

### S4

#### First pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 0 - 20           | 1                | 20            |
| alpha_1               | -1 to 1          | 0.2              | -0.6          |
| Iterations            | 232              | -                | -             |
| Solving time          | 00:33:55         | -                | -             |
| Time per iteration    | 8.77 s           | -                | -             |

#### Second pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 15 to 25         | 0.5              | 20            |
| alpha_1               | -1.2 to -0.2     | 0.1              | -0.6          |
| Iterations            | 185              | -                | -             |
| Solving time          | 00:27:03         | -                | -             |
| Time per iteration    | 8.77 s           | -                | -             |

#### Third pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 17.5 to 22.5     | 0.1              | 19.8          |
| alpha_1               | -0.8 to -0.2     | 0.1              | -0.6          |
| Iterations            | 180              | -                | -             |
| Solving time          | 00:24:21         | -                | -             |
| Time per iteration    | 8.12 s           | -                | -             |

Another very close value is found at alpha_0 = 17.9 and alpha_1 = -0.5. However, the first value is kept, as the vicinity of this area is the lowest in the whole grid search.

## Case A:
- Medium-DC, 25 MW, without transmission losses. Only S4 is evaluated.

### S4
#### First pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 0 - 20           | 1                | 6             |
| alpha_1               | -1.5 to 1.5      | 0.3              | 0.2           |
| Iterations            | 167              | -                | -             |
| Solving time          | ??               | -                | -             |
| Time per iteration    | 8.5 s            | -                | -             |

#### Second pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 5 - 25           | 1                | 6             |
| alpha_1               | -0.6 - 0.3       | 0.1              | 0.3           |
| Iterations            | 148              | -                | -             |
| Solving time          | ??               | -                | -             |
| Time per iteration    | 8.5 s            | -                | -             |

#### Third pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 6 - 24           | 0.5              | 6 (19)        |
| alpha_1               | -0.7 - 0.4       | 0.1              | 0.3 (-0.7)    |
| Iterations            | 236              | -                | -             |
| Solving time          | ??               | -                | -             |
| Time per iteration    | 8.5 s            | -                | -             |

#### Fourth pass - A
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 5 - 7            | 0.1              | 6             |
| alpha_1               | 0.1 - 0.5        | 0.1              | 0.3           |
| Iterations            | ??               | -                | -             |
| Solving time          | ??               | -                | -             |
| Time per iteration    | 8.5 s            | -                | -             |

#### Fourth pass - B
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 16.5 - 23.5      | 1                | 19.1          |
| alpha_1               | -0.9 - -0.6      | 0.1              | -0.7          |
| Iterations            | 236              | -                | -             |
| Solving time          | ??               | -                | -             |
| Time per iteration    | 8.5 s            | -                | -             |

**_Conclusion_**: A fourth pass is done in two areas with optimal values in the third pass. The optimal value is 6€, with alpha_1 = 0.3. The second best value is 19.1€, with alpha_1 = -0.7, with an objective function 0.40% higher than the optimal value.

## Case B:
- Medium-DC, 25 MW, with transmission losses. Only S4 is evaluated.

### S4
#### First pass
| Attribute             | Value Range      | Step Size        | Optimal Value |
|-----------------------|------------------|------------------|---------------|
| alpha_0               | 0 - 20           | 1                | 20            |
| alpha_1               | -1.5 to 1.5      | 0.3              | -0.4          |
| Iterations            | 167              | -                | -             |
| Solving time          | ??               | -                | -             |
| Time per iteration    | 8.5 s            | -                | -             |