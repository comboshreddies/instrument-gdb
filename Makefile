
gdb_test: gdb_test.c
	gcc -o gdb_test ./gdb_test.c -g

clean:
	rm -f gdb_test
