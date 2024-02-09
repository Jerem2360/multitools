/*
Multiline comments should be ignored
void foo(int a, int b);
*/
//#include <stdint.h>
#define macro(abc, def) abc * def

#if defined(macro) && (1 <= 2)

void bar(long a, long b);

#endif

int main(int argc, char** argv) {
    /*This comment should be ignored*/
    printf("Hello");
    // abort()
}


