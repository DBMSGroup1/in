def myhash(x):
    ans=''
    for i in x:
        ans+=hex(ord(i)).replace('0x','')
    return ans
print(myhash('123'))
