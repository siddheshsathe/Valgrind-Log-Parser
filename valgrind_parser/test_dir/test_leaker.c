#include<stdio.h>
#include<stdlib.h>

int main(){
    int *memory_allocation_var = malloc(1000);
    int conditional_jump_variable_without_initialize;
    if (conditional_jump_variable_without_initialize > 0){
        printf("Variable not initialized still using here \n");
    }
    return 0;
}