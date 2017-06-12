import time, functools
"""
def compoot(x):
	result = 4*(x^3) - 9*(x^2) + 4*x
	print(result)


start = time.time()
curr = time.time()

tupe = ('h','i',' ','m','y',' ','n','a','m')

while (curr - start < 2):
	curr = time.time()
	
	if (curr-start) % 1 == 0: 
		print(curr-start)
		print(tupe[1:3])
#------------
string = "1,23,3"
print(list(string.split(",")))

[1,1,1,1,1,2,2,2]
def lookAndSay(a):
	result = []
	seen = []
	for item in a:
		count = 0
		if item in seen: pass
		else:
			seen.append(item)
			for match in a:
				if match == item: count += 1
			result.append( (item,count) )
	return result

def memory(f):
    # You are not responsible for how this decorator works
    # on the inside, just how to use it!
    mem = dict()
    @functools.wraps(f)
    def wrapper(n):
        if n not in mem:
            mem[n] = f(n)
        else: return mem[args]
    return wrapper

@memory
def fib(n):
    if (n < 2):
        return 1
    else:
        return fib(n-1) + fib(n-2)

def testFib(maxN=40):
    for n in range(maxN+1):
        start = time.time()
        fibOfN = fib(n)
        ms = 1000*(time.time() - start)
        print("fib(%2d) = %8d, time =%5dms" % (n, fibOfN, ms))

def main():
	testFib()
"""

def rangeSum(lo, hi):
    if (lo > hi):
        return 0
    else:
        return lo + rangeSum(lo+1, hi)

def callWithLargeStack(f,*args):
    import sys
    import threading
    sys.setrecursionlimit(2**14) # max recursion depth of 16384
    isWindows = (sys.platform.lower() in ["win32", "cygwin"])
    if (not isWindows): return f(*args) # sadness...
    threading.stack_size(2**27)  # 64MB stack
    # need new thread to get the redefined stack size
    def wrappedFn(resultWrapper): resultWrapper[0] = f(*args)
    resultWrapper = [None]
    #thread = threading.Thread(target=f, args=args)
    thread = threading.Thread(target=wrappedFn, args=[resultWrapper])
    thread.start()
    thread.join()
    return resultWrapper[0]

def memory(f):
    mem = dict()
    @functools.wraps(f)
    def wrapper(n):
        if n not in mem:
            mem[n] = f(n)
        return mem[n]
    return wrapper

def flatline(n):
	return (n == 4 or n == 2 or n == 1)

@memory
def algorithm(n):
	count = 0
	while (not flatline(n) and count <= 100):
		if (n % 2 == 0): n = algorithm(n//2)
		else: n = algorithm(3*n+1)
		count += 1

	if count == 100 and not flatline(n): return False
	else: return True

def testFib(maxN=  9000000):
    for n in range(8999000,maxN+1):
        start = time.time()
        fibOfN = algorithm(n)
        ms = 1000*(time.time() - start)
        print("fib(%2d)=%8d,time =%5dms" % (n, fibOfN, ms))

if __name__ == '__main__':
	testFib()
	#main()


