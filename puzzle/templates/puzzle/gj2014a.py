f=open("input")
T=int(f.readline())
for case in range(T):
    g1 = int(f.readline())
    m1 = [f.readline().split() for i in range(4)][g1-1]
    g2 = int(f.readline())
    m2 = [f.readline().split() for i in range(4)][g2-1]    
    inter = set(m1)&set(m2)
    rtn = "Bad magician!"
    if len(inter)==1:
        rtn=list(inter)[0]
    if len(inter)==0:
        rtn = "Volunteer cheated!"    
    print("Case #%d: %s"%(case+1, rtn))
f.close()
    
