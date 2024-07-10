# A tool for instrumenting gdb execution for automated, selective and low overhead observation of debugged program #


Gdb support python scripting, so here is simple example to instrument gdb for purpose that matched my needs 
example below were run on both arm64 and amd64 linux

I wanted to observe some part of execution, but not whole execution. Initially I did not have symbols or source code.
I've decided that I will observe system call write (debuging with printf), and use gdb python to check syscall arguments.
(one can choose to start observing on any other breakpoint if source and symbols are available)

Example program gdb_test program will dive recursively up to depth of 120, increasing depth one by one, then exit/return.
On each depth that is dividable by 10 it will print 'aaa <depth>'.

The output of gdb_test program is
``` console
$ ./gdb_test
aaa 0
aaa 10
aaa 20
aaa 30
aaa 40
aaa 50
aaa 60
aaa 70
aaa 80
aaa 90
aaa 100
aaa 110
aaa 120
```

I wanted to observe all steps, all backtraces from the moment application wrote 'aaa 70' to
moment application writes 'aaa 90', and after that I do not interfere with execution.
With provided output, depending on available debug symbols, one can reconstruct execution trace of
function calls, inspect registers or locals on every step, or set more specific breakpoints.

Use this as an example and a template for further drill down.

Idea behind was to instrument execution of some gdb observed program with minimall overhead, and no user inputs.
Ie I can't response with continue in console that fast that I would like to, yet python gdb extension can.

Process is being observed in light way till it matches some predefined state (in this example till app it writes 'aaa 70').
After that point process is being intensively observed till it matches next state (in this example till app writes 'aaa 90')

## compile test app 
compile gdb_test app with
``` console
gcc -o gdb_test gdb_test.c -g
```  

or just 
``` console
make
```

## run 
run gdb observe with
``` console
gdb -x gdb_observe_test.py
```

