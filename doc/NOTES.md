
## Testing equation rendering

### Similarity measure

![equation](https://latex.codecogs.com/svg.image?S_i_j&space;=&space;e^{-\alpha&space;D_i_j})

### Alpha parameter

![equation](https://latex.codecogs.com/svg.image?\alpha&space;=&space;-(ln&space;0.5)&space;/&space;D&space;)

### Distance between samples

![equation](https://latex.codecogs.com/svg.image?D_i_j&space;=&space;\left&space;[&space;\sum_{k=1}^{n}&space;((x_i_k&space;-&space;x_j_k)&space;/&space;(max_k&space;-&space;min_k))^{2}&space;\right&space;]^{1/2})

### Entropy measure of a dataset

![equation](https://latex.codecogs.com/svg.image?E&space;=&space;-\sum_{i=1}^{N-1}&space;\sum_{j=i&plus;1}^{N}(S_i_j&space;*&space;log(S_i_j)&space;&plus;&space;(1-S_i_j)&space;*&space;log(1-S_i_j)))
