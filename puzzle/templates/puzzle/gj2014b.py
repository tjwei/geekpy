def compute(C,F,X):
    best, farms = X/2, 0
    if X <= C:
        return best
    dt, dc, drate = 0, 0, 2    
    while 1:
        delta = C/drate
        dt = dt + delta        
        dc= dc + drate*delta - C
        drate += F
        new_time = dt + (X-dc)/drate
        if new_time >= best:
            break
        best = new_time
    return best
        
        


f=open("input")
T=int(f.readline())
for case in range(T):
    C,F,X = map(float, f.readline().split())
    #print(C,F,X)
    rtn = compute(C,F,X)
    print("Case #%d: %s"%(case+1, rtn))
f.close()
    
