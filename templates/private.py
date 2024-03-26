def dtb(x):
    ans=''
    while(x>1):
        ans=str(x%2)+ans
        x=x//2
    ans=str(x)+ans
    while(len(ans)<8):
        ans='0'+ans
    return ans    

def btd(x):
    str(x)
    p=0
    out=0
    for i in range(len(x)-1,-1,-1):
        out+=int(x[i])*(2**p)
        p+=1
    return out

def encrypt(x):
    x=str(x)
    out=''
    for i in x:
        out+=dtb(ord(i))
    return out

def decrypt(x):
    x=str(x)
    i=0
    out=''
    for k in range(len(x)//8):
        out+=chr(btd(x[i:i+8]))
        i+=8
    return out

