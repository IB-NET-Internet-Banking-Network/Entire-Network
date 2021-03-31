from tinyec import registry
import secrets
import numpy as np 

'''Public and Private key Generation using Elliptic curve cryptography'''
def Elliptic_crypto():

    curve = registry.get_curve('secp256r1')#standard elliptic curves
    
    privkey = secrets.randbelow(curve.field.n)    
    pubkey = privkey * curve.g
    privkey = str(privkey)
    pubkeycomp = '0'+str(2 + pubkey.y % 2) + str(hex(pubkey.x)[2:])#public key compression
    pubkeycomp = str(pubkeycomp)

    print("public key:",pubkeycomp)    
    return (privkey,pubkeycomp)

    
'''AES SubByte Step'''
def subbyte(arr):

    b=[]
    s=[['0x63','0x7c','0x77','0x7b','0xf2','0x6b','0x6f','0xc5','0x30','0x10','0x67','0x2b','0xfe','0xd7','0xab','0x76'],
       ['0xca','0x82','0xc9','0x7d','0xfa','0x59','0x47','0xf0','0xad','0xd4','0xa2','0xaf','0x9c','0xa4','0x72','0xc0'],
       ['0xb7','0xfd','0x93','0x26','0x36','0x3f','0xf7','0xcc','0x34','0xa5','0xe5','0xf1','0x71','0xd8','0x31','0x15'],
       ['0x40','0xc7','0x23','0xc3','0x18','0c96','0x50','0x9a','0x70','0x12','0x80','0xe2','0xeb','0x27','0xb2','0x75'],
       ['0x90','0x83','0x2c','0x1a','0x1b','0x6e','0x5a','0xa0','0x52','0x3b','0xd6','0xb3','0x29','0xe3','0x2f','0x84'],
       ['0x53','0xd1','0x00','0xed','0x20','0xfc','0xb1','0x5b','0x6a','0xcb','0xbe','0x39','0x4a','0x4c','0x58','0xcf'],
       ['0xd0','0xef','0faa','0xfb','0x43','0x4d','0x33','0x85','0x45','0xf9','0x20','0x7f','0x50','0x3c','0x9f','0xa8'],
       ['0x51','0xa3','0x40','0x8f','0x92','0x9d','0x38','0xf5','0xbc','0xb6','0xda','0x21','0x10','0xff','0xf3','0xd2'],
       ['0xcd','0x0c','0x13','0xec','0x5f','0x97','0x44','0x17','0xc4','0xa7','0x7e','0x3d','0x64','0x5d','0x19','0x73'],
       ['0x60','0x81','0x4f','0xdc','0x22','0x2a','0x90','0x88','0x46','0xee','0xb8','0x14','0xde','0x5e','0x0b','0xdb'],
       ['0xe0','0x32','0x3a','0x0a','0x49','0x60','0x24','0x5c','0xc2','0xd3','0xac','0x62','0x91','0x95','0xe4','0x79'],
       ['0xe7','0xc8','0x37','0x6d','0x8d','0xd5','0x4e','0x89','0x6c','0x56','0xf4','0xea','0x65','0x7a','0xae','0x80'],
       ['0xba','0x78','0x25','0x2e','0x1c','0xa6','0xb4','0xc6','0xe8','0xdd','0x74','0x1f','0x4b','0xbd','0x8b','0x8a'],
       ['0x70','0x3e','0xb5','0x66','0x48','0x30','0xf6','0x0e','0x61','0x35','0x57','0xb9','0x86','0xc1','0x1d','0x9e'],
       ['0xc1','0xf8','0x98','0x11','0x69','0xd9','0x8e','0x94','0x9b','0x1e','0x87','0xe9','0xce','0x55','0x28','0xdf'],
       ['0x8c','0xa1','0x89','0x0d','0xbf','0xe6','0x42','0x68','0x41','0x99','0x2d','0x0f','0xb0','0x54','0xbb','0x16']]

    for i in arr:
        b3=[]        
        for j in i:
            b1=[]
            b2=[]
            if(len(j)<4):
                j=j+'0'            
            f1=int("{0:02d}".format(int(j[2], 16)))
            f2=int("{0:02d}".format(int(j[3], 16)))            
            b1=b1+s[f1]            
            b3.append(b1[f2])
        b.append(b3)
    return(b)            


def MixedColumn(arr):
    
    fy=[]
    sec=[[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    z='00011011'
    c=0
    h=0
    m=[]
    fe=[]
    rez = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
    #print('rez',rez)
    for i in range(0,16):
        s=sec[c]
        w=rez[h]     
        #print('w',w)
        
        for j in range(0,4):
            p=s[j]
            q=w[j]
            t=''
            k=''
            sr1=''
            re="{0:08b}".format(int(q, 16))
            if(len(re)%8!=0):#satisfy constant length of 128 bits
                fin=8-(len(re)%8)
                for a in range(0,fin):
                    re='0'+re
            for e in range(len(re)-1,len(re)):#row shifting          
                sr1=sr1+re[e]                
            for e in range(0, len(re)-1):                
                sr1=sr1+'0'
            if(p==1):
                m.append(re)
            elif(p==2):
                if(re[7]==1):
                    for y in range(0,8):
                        t=t+str(int(sr1[y])^int(z[y]))
                    m.append(t)
                else:
                    m.append(sr1)
            elif(p==3):
                if(re[7]==1):
                    for y in range(0,8):
                        t=t+str(int(sr1[y])^int(z[y])^int(re[y]))
                    m.append(t)
                else:
                    for y in range(0,8):
                        t=t+str(int(sr1[y])^int(re[y]))
                    m.append(t)
            #print('m',m)
            if(j%3==0 and j!=0):
                for ki in range(0,8):                    
                    u1=m[0]
                    u2=m[1]
                    u3=m[2]
                    u4=m[3]
                    k=k+str(int(u1[ki])^int(u2[ki])^int(u3[ki])^int(u4[ki]))
                b=hex(int(k,2))
                if(len(b)%4!=0):#satisfy constant length of 128 bits
                    fin=4-(len(b)%4)
                    for a in range(0,fin):
                        b=b+'0'                
                fe.append(b)
                #print('fe',fe)
                m=[]
        #print('h',h)
        #print('c',c)
        h=h+1
        
        if((i+1)%4==0 and i!=0):
            h=0
            
        if((i+1)%4==0 and i!=0):
            c=c+1
            fy.append(fe)
            #print('fy',fy)
            fe=[]
            
            
    rez1 = [[fy[j][i] for j in range(len(fy))] for i in range(len(fy[0]))]        
    return(rez1)

def rndsche(pub):

    s=[['0x63','0x7c','0x77','0x7b','0xf2','0x6b','0x6f','0xc5','0x30','0x10','0x67','0x2b','0xfe','0xd7','0xab','0x76'],
       ['0xca','0x82','0xc9','0x7d','0xfa','0x59','0x47','0xf0','0xad','0xd4','0xa2','0xaf','0x9c','0xa4','0x72','0xc0'],
       ['0xb7','0xfd','0x93','0x26','0x36','0x3f','0xf7','0xcc','0x34','0xa5','0xe5','0xf1','0x71','0xd8','0x31','0x15'],
       ['0x40','0xc7','0x23','0xc3','0x18','0c96','0x50','0x9a','0x70','0x12','0x80','0xe2','0xeb','0x27','0xb2','0x75'],
       ['0x90','0x83','0x2c','0x1a','0x1b','0x6e','0x5a','0xa0','0x52','0x3b','0xd6','0xb3','0x29','0xe3','0x2f','0x84'],
       ['0x53','0xd1','0x00','0xed','0x20','0xfc','0xb1','0x5b','0x6a','0xcb','0xbe','0x39','0x4a','0x4c','0x58','0xcf'],
       ['0xd0','0xef','0faa','0xfb','0x43','0x4d','0x33','0x85','0x45','0xf9','0x20','0x7f','0x50','0x3c','0x9f','0xa8'],
       ['0x51','0xa3','0x40','0x8f','0x92','0x9d','0x38','0xf5','0xbc','0xb6','0xda','0x21','0x10','0xff','0xf3','0xd2'],
       ['0xcd','0x0c','0x13','0xec','0x5f','0x97','0x44','0x17','0xc4','0xa7','0x7e','0x3d','0x64','0x5d','0x19','0x73'],
       ['0x60','0x81','0x4f','0xdc','0x22','0x2a','0x90','0x88','0x46','0xee','0xb8','0x14','0xde','0x5e','0x0b','0xdb'],
       ['0xe0','0x32','0x3a','0x0a','0x49','0x60','0x24','0x5c','0xc2','0xd3','0xac','0x62','0x91','0x95','0xe4','0x79'],
       ['0xe7','0xc8','0x37','0x6d','0x8d','0xd5','0x4e','0x89','0x6c','0x56','0xf4','0xea','0x65','0x7a','0xae','0x80'],
       ['0xba','0x78','0x25','0x2e','0x1c','0xa6','0xb4','0xc6','0xe8','0xdd','0x74','0x1f','0x4b','0xbd','0x8b','0x8a'],
       ['0x70','0x3e','0xb5','0x66','0x48','0x30','0xf6','0x0e','0x61','0x35','0x57','0xb9','0x86','0xc1','0x1d','0x9e'],
       ['0xc1','0xf8','0x98','0x11','0x69','0xd9','0x8e','0x94','0x9b','0x1e','0x87','0xe9','0xce','0x55','0x28','0xdf'],
       ['0x8c','0xa1','0x89','0x0d','0xbf','0xe6','0x42','0x68','0x41','0x99','0x2d','0x0f','0xb0','0x54','0xbb','0x16']]

    rc=['00000001','00000010','00000100','00001000','00010000','00100000','010000000','10000000','00011011','01010110','01101100','11011000','10101011','01001101']      
    resc=[]
    resc.append(pub)
    pub1=pub
    for t in range(0,13):
        w=[]
        n=[]
        sr1=[]
        b1=''
        r1=''
        m=''
        ms=''
        pref=''
        pre=[]        
        
        for i in range(0,31,2):
            p=''
            p=p+pub1[i:i+2]
            w.append(p)
        for i in range(12,16):
            n.append(w[i])
        for j in range(len(n)-1,len(n)):#row shifting          
            sr1.append(n[j])                
        for j in range(0, len(n)-1):                
            sr1.append(n[j])
        #print('n',n)
        for j in sr1:
            f1=int(j[0],16)            
            f2=int(j[1],16)
            #f2=int("{0:02d}".format(j[1], 16))
            b4=s[f1]
            b3=b4[f2]
            b1=b1+str(b3[2:3])
        res ="{0:08b}".format(int(b1, 16))
        if(len(res)%32!=0):#satisfy constant length of 128 bits
            fin=32-(len(res)%32)
            for i in range(0,fin):
                res='0'+res
        for i in range(1,25):
            rc[t]=rc[t]+'0'
        r1=r1+rc[t]
        for i in range(0,32):
            q=int(res[i])            
            r=int(r1[i])
            m=m+str(q^r)
        bin1="{0:08b}".format(int(pub, 16))        
        if(len(bin1)%128!=0):#satisfy constant length of 128 bits
            fin=128-(len(res)%128)
            for i in range(0,fin):
                bin1='0'+bin1
        for i in range(0,32):
            q=int(bin1[i])            
            r=int(m[i])
            ms=ms+str(q^r)
        pre.append(ms)
        ms=''
        co=0
        cm=0
        q1=''
        q1=q1+pre[co]
        for i in range(32,129):            
            if(i%32==0 and i!=32):
                pre.append(ms)
                ms=''
                co=0
                cm=0
                q1=''
                co=co+1
                q1=q1+pre[co]   
            if(i==128):
                break
            q=int(q1[cm])            
            r=int(bin1[i])            
            ms=ms+str(q^r)
            cm=cm+1        
        for i in pre:
            pref=pref+i
        #print('pref',pref)
        #print('hex',len(hex(int(pref,2))))
        pub1=hex(int(pref,2))
        pub1=pub1[2:]
        if(len(pub1)%32!=0):#satisfy constant length of 128 bits
            fin=32-(len(pub1)%32)
            for i in range(0,fin):
                pub1=pub1+'0'
        resc.append(pub1)     
    
    return(resc)

    
'''AES Shift rows as per row numbers'''    
def shiftrow(arr):
    sr=[]
    num=0  #number of times row is shifted  
    for i in arr:
        sr1=[]
        for j in range(len(i)-num,len(i)):  #row shifting          
            sr1.append(i[j]) 
        for j in range(0, len(i)-num):                
            sr1.append(i[j])
        sr.append(sr1)
        num=num+1
    return(sr)
            
'''xor text and shared key'''            
def addround(pub,bintxt):
    binpub = str("{0:08b}".format(int(pub, 16))) #hex to bin conversion   
    if(len(binpub)%128!=0):
        fin1=128-(len(binpub)%128)
        for i in range(0,fin1):
            binpub='0'+binpub
    rnd=''
    for i in range(0,len(binpub)):
        rnd=rnd+str(int(bintxt[i])^int(binpub[i]))#addRound key operation
    return(rnd)

def array(bindata):
    
    arr=[]
    c=0
    d=int(len(bindata)/4)
    for i in range(0,4):#State array
        ele=[]
        for j in range(c,d,8):
            temp=bindata[j:j+8]
            tm=int(temp,base=2)
            fe=hex(tm)
            if(len(fe)%4!=0):#satisfy constant length of 128 bits
                fin=4-(len(fe)%4)
                for i in range(0,fin):
                    fe=fe+'0'
            ele.append(fe)            
            #print(temp)
        c=c+32
        d=d+32
        arr.append(ele)
    return(arr)

def dearr(arr):
    st=''
    for i in arr:
        for j in i:
            st=st+str(j[2:3])
    sr="{0:08b}".format(int(st, 16))
    if(len(sr)%128!=0):#satisfy constant length of 128 bits
        fin=128-(len(sr)%128)
        for i in range(0,fin):
            sr='0'+sr
    return(sr)

'''AES Encryption'''
def AES(text,pubkey2):   
        
    pubkey21=pubkey2[0:32]
    pubkey22=pubkey2[32:64]
    #print('pu1',pubkey21)
    res = ''.join(format(i, '08b') for i in bytearray(text, encoding ='utf-8')) #decimal to binary
    res1=str(res)
    bindata=res1
    """for i in range(0, len(res1), 8):
        temp= res1[i:i + 8]
        decimal_data = int(temp,base=2)
        strdata = strdata + chr(decimal_data)  
    print(strdata)"""
    if(len(res1)%128!=0):#satisfy constant length of 128 bits
        fin=128-(len(res1)%128)
        for i in range(0,fin):
            bindata='0'+bindata

    cry=''        
    rk=rndsche(pubkey22)
    ini=bindata
    rnd0=addround(pubkey21,bindata)

    for i in range(0,14):
        arr=array(ini)
        arr1=subbyte(arr)
        arr2=shiftrow(arr1)
        arr3=MixedColumn(arr2)
        sr4=dearr(arr3)
        sr5=addround(rk[i],sr4)
        ini=sr5    
    arr=array(sr5)
    arr1=subbyte(arr)
    sr4=dearr(arr3)
    sr5=addround(pubkey21,sr4)
    cry=cry+sr5
    """binpub1 = str("{0:08b}".format(int(pubkey21, 16)))
    binpub2 = "{0:08b}".format(int(pubkey22, 16))
    if(len(binpub1)%128!=0):
        fin1=128-(len(binpub1)%128)
        for i in range(0,fin1):
            binpub1='0'+binpub1
    rnd1=[]
    for i in range(0,len(binpub1)):
        rnd1.append((int(bindata[i])^int(binpub1[i])))"""
    print(len(cry))
    return(cry)

    
def inp():
    Text=str(input("enter plain Text"))
    shkey2=input("secret key")
    (pri,pub)=Elliptic_crypto()
    tr="{0:08d}".format(int(pri[0:64], 16))
    fr="{0:08d}".format(int(shkey2, 16))
    pkey2=str(int(tr)*int(fr))
    pubkey2=hex(int(pkey2,10))    
    pubkey2=pubkey2[2:67]
    print(pubkey2)
    return (AES(Text,pubkey2))
print(inp())
    
    
      

