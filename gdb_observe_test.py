""" tool for instrumeting gdb execution via python """

def exit_handler(event):
    """ exit event handler """
    print("event type: exit")
    if hasattr(event, 'exit_code'):
        print(f"exit code: {event.exit_code}d")
    else:
        print("exit code not available")
    gdb.execute("quit")


def stop_handler(_):
    """ stop event handler """
    print("event type: stop")


def get_n_bytes_from_reg(n):
    """ get n bytes from pointer pointed by register """
    arch = gdb.selected_frame().architecture().name()
    if arch in reg_from_arch:
        reg = reg_from_arch[arch]
        return (
            gdb.selected_frame().read_register(reg).cast(
                gdb.lookup_type('char').pointer()).string())[:n]
    return ""


# run this after specifying file <binary>
def detect_target_arch():
    """ detect architecture """
    target_lines = gdb.execute("info target", True, True).split('\n')
    for i in target_lines:
        words = i.split(' ')
        if words[-2] == "type" and words[-3] == "file":
            return words[-1][:-1]
    return ""


gdb.events.exited.connect(exit_handler)
gdb.events.stop.connect(stop_handler)

reg_from_arch = {}
reg_from_arch["i386:x86-64"] = "rsi"
reg_from_arch["aarch64"] = "x1"

# catching write syscall on intel/arm
syscall_from_arch = {}
syscall_from_arch["elf64-x86-64"] = "1"
syscall_from_arch["elf64-littleaarch64"] = "64"

MYEXEFILE = "./gdb_test"
print("### preparing to run: " + MYEXEFILE)

gdb.execute("file " + MYEXEFILE)

target = detect_target_arch()

gdb.execute("set pagination off")

print("### setting syscall catchpoint on write syscall - arch specific")
gdb.execute("catch syscall " + syscall_from_arch[target])
gdb.execute("info breakpoints")
gdb.execute("show logging")

print("### running ")
gdb.execute("run")

# do nothing until we observe write with 'aaa 70'
# payload in register on catched syscall
while get_n_bytes_from_reg(6) != "aaa 70":
    gdb.execute("continue")

frame_to_observe = gdb.selected_frame().name()
# syscalls do have call and return break, so one more continue
gdb.execute("continue")

print("### observing, step by step execution from 70 to 90")
print("### waiting for frame " + frame_to_observe + " and arg 'aaa 90'")

# we observe step by step, until we spot write syscall with arg 'aaa 90'
while not (
         gdb.selected_frame().name() == frame_to_observe and
         get_n_bytes_from_reg(6) == "aaa 90"):
    gdb.execute("backtrace 12")
    gdb.execute("info local")
    gdb.execute("info args")
    gdb.execute("info frame")
    print("### step")
    gdb.execute("step")

# we exited section of execution that we wanted to observe in details
gdb.execute("delete breakpoint 1")
gdb.execute("continue")

gdb.execute("quit")
