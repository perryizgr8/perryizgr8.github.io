---
layout: post
title:  "Some odd GCC behavior"
categories: C++
---
In C++, there are generally two kinds of memory that you use. 

1. Heap memory - This is what you use when you call `new()`.
1. Stack memory - This is what you use when you declare a non-static local variable inside a function.

The heap lasts for the entire lifetime of your program. You can access it from anywhere in the program if you know the memory location of your data. Heap memory needs to be allocated using some OS syscall, e.g. `brk()` in Linux. Once you are done with the memory, you must release it. This can be done by `delete()` or most commonly automatically when an allocated object's destructor is run.

The stack memory is local to the function where you declare a variable. It can be used by callees but not the callers. So you can use this memory as long as the current frame is not popped out of the stack.

Let us look at this program:

{% highlight cpp %}
#include <iostream>

int *func(int a, int b) {
    int sum = a + b;
    return &sum;
}

int main() {
    int *a = func(10, 5);
    std::cout << *a << "\n";
    return 0;
}
{% endhighlight %}

Here `func()` returns the memory address of `sum` which is a stack variable. The problem is that on returning from `func()`, the frame is popped out of the stack, which includes the local variables declared in `func()`. So `a` now points to a memory that is no longer supposed to be used.

So what happens if you compile it? Well, you get a warning from the compiler.

{% highlight shell %}
$ g++ scratch.cpp
scratch.cpp: In function ‘int* func(int, int)’:
scratch.cpp:5:12: warning: address of local variable ‘sum’ returned [-Wreturn-local-addr]
    5 |     return &sum;
      |            ^~~~
scratch.cpp:4:9: note: declared here
    4 |     int sum = a + b;
      |         ^~~
{% endhighlight %}

But we're using C++ and we know exactly what we're doing, so let us ignore this warning and execute the program.

{% highlight shell %}
$ ./a.out 
Segmentation fault (core dumped)
{% endhighlight %}

Huh... that's strange. Let's find out why that happened.

{% highlight shell %}
$ g++ scratch.cpp -g -O0
scratch.cpp: In function ‘int* func(int, int)’:
scratch.cpp:5:12: warning: address of local variable ‘sum’ returned [-Wreturn-local-addr]
    5 |     return &sum;
      |            ^~~~
scratch.cpp:4:9: note: declared here
    4 |     int sum = a + b;
      |         ^~~
$ gdb ./a.out 
GNU gdb (Ubuntu 9.1-0ubuntu1) 9.1
Reading symbols from ./a.out...
(gdb) start
Temporary breakpoint 1 at 0x1210: file scratch.cpp, line 8.
Starting program: /home/perry/a.out 

Temporary breakpoint 1, main () at scratch.cpp:8
8       int main() {
(gdb) n
9           int *a = func(10, 5);
(gdb) n
10          std::cout << *a << "\n";
(gdb) p a
$1 = (int *) 0x0
(gdb)
{% endhighlight %}

This is extremely peculiar. The address returned from `func()` and stored into `a` is 0. 

Let us rewrite the program and make use of the powerful debugging technique known as `printf`.

{% highlight cpp %}
#include <iostream>

int *func(int a, int b) {
    int sum = a + b;
    std::cout << "&sum=" << &sum << "\n";
    return &sum;
}

int main() {
    int *a = func(10, 5);
    std::cout << "a=" << a << "\n";
    std::cout << *a << "\n";
    return 0;
}
{% endhighlight %}

Let's run this.

{% highlight shell %}
$ g++ scratch.cpp
scratch.cpp: In function ‘int* func(int, int)’:
scratch.cpp:6:12: warning: address of local variable ‘sum’ returned [-Wreturn-local-addr]
    6 |     return &sum;
      |            ^~~~
scratch.cpp:4:9: note: declared here
    4 |     int sum = a + b;
      |         ^~~
$ ./a.out 
&sum=0x7ffe48dbc344
a=0
Segmentation fault (core dumped)
{% endhighlight %}

The address of `sum` is `0x7ffe48dbc344`, but for some reason the value returned to `main()` is 0.

At this point I was totally stumped, so I tried compiling the two variants of the program with `clang` instead of `gcc`.

{% highlight shell %}
$ ./a.out 
15
$ ./a_with_cout.out 
&sum=0x7fff62101714
a=0x7fff62101714
32767
{% endhighlight %}

First thing to note is that the original program ran as we expected. It returned the address to `sum` and printed the value stored at that address, even though that frame had been popped out.
Secondly, the revised program with `cout` shows that the address returned into `a` is the same as address of `sum`, but for some reason the value stored there has changed from the expected `15`.

Let's ignore the change in value for now, since accessing a memory location from a popped out frame is probably undefined behavior and the compiler is free to do whatever it likes when you go into undefined territory.

Let's try to find out why `gcc` and `clang` give us different programs for the same code. What if we looked at the disassembly? I will use the super useful [Compiler Explorer](https://godbolt.org/) for this purpose.

GCC 10.1 (x86-64) produces the following for `func()`:

{% highlight nasm %}
func(int, int):
        push    rbp
        mov     rbp, rsp
        mov     DWORD PTR [rbp-20], edi
        mov     DWORD PTR [rbp-24], esi
        mov     edx, DWORD PTR [rbp-20]
        mov     eax, DWORD PTR [rbp-24]
        add     eax, edx
        mov     DWORD PTR [rbp-4], eax
        mov     eax, 0
        pop     rbp
        ret
{% endhighlight %}

Towards the end, note how `0` is moved into `eax` then the function returns. The register `eax` is generally used to return values. So GCC is explicitly returning 0, instead of the address we wanted.

Clang 10.0.0 (x86-64) produces the following for `func()`:

{% highlight nasm %}
func(int, int):                              # @func(int, int)
        push    rbp
        mov     rbp, rsp
        mov     dword ptr [rbp - 4], edi
        mov     dword ptr [rbp - 8], esi
        mov     eax, dword ptr [rbp - 4]
        add     eax, dword ptr [rbp - 8]
        mov     dword ptr [rbp - 12], eax
        lea     rax, [rbp - 12]
        pop     rbp
        ret
{% endhighlight %}

The generated code is almost exactly the same, except that Clang returns the address we wanted. This is why this program did the expected thing and printed the sum.

Why is this happening? Why this difference between GCC and Clang? I don't know. Since we are doing something that is undefined in the C++ standard, the compiler is free to do whatever it wants. If I ever figure out why GCC is explicitly sabotaging our return value, I'll make a new post about that!