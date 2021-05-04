from tinyec import registry
import secrets
#import numpy as np 
from socket import*
#import pickle


'''Public and Private key Generation using Elliptic curve cryptography'''
def Elliptic_crypto():
    curve = registry.get_curve('secp256r1')#standard elliptic curves
    privkey = secrets.randbelow(curve.field.n)
    f=curve.g
    m=f.y+f.x    
    pubkey = privkey * m
    privkey = str(privkey)
    pubkeycomp = str(pubkey)#public key compression
           
    return (privkey,pubkeycomp)

    
'''AES SubByte Step'''
    
def subbyte(arr):    
    b=[]
    s=[['0x52','0x09','0x6a','0xd5','0x30','0x36','0xa5','0x38','0xbf','0x40','0xa3','0x9e','0x81','0xf3','0xd7','0xfb'],
       ['0x7c','0xe3','0x39','0x82','0x9b','0x2f','0xff','0x87','0x34','0x8e','0x43','0x44','0xc4','0xde','0xe9','0xcb'],
       ['0x54','0x7b','0x94','0x32','0xa6','0xc2','0x23','0x3d','0xee','0x4c','0x95','0x0b','0x42','0xfa','0xc3','0x4e'],
       ['0x08','0x2e','0xa1','0x66','0x28','0xd9','0x24','0xb2','0x76','0x5b','0xa2','0x49','0x6d','0x8b','0xd1','0x25'],
       ['0x72','0xf8','0xf6','0x64','0x86','0x68','0x98','0x16','0xd4','0xa4','0x5c','0xcc','0x5d','0x65','0xb6','0x92'],
       ['0x6c','0x70','0x48','0x50','0xfd','0xed','0xb9','0xda','0x5e','0x15','0x46','0x57','0xa7','0x8d','0x9d','0x84'],
       ['0x90','0xd8','0xab','0x00','0x8c','0xbc','0xd3','0x0a','0xf7','0xe4','0x58','0x05','0xb8','0xb3','0x45','0x06'],
       ['0xd0','0x2c','0x1e','0x8f','0xca','0x3f','0x0f','0x02','0xc1','0xaf','0xbd','0x03','0x01','0x13','0x8a','0x6b'],
       ['0x3a','0x91','0x11','0x41','0x4f','0x67','0xdc','0xea','0x97','0xf2','0xcf','0xce','0xf0','0xb4','0xe6','0x73'],
       ['0x96','0xac','0x74','0x22','0xe7','0xad','0x35','0x85','0xe2','0xf9','0x37','0xe8','0x1c','0x75','0xdf','0x6e'],
       ['0x47','0xf1','0x1a','0x71','0x1d','0x29','0xc5','0x89','0x6f','0xb7','0x62','0x0e','0xaa','0x18','0xbe','0x1b'],
       ['0xfc','0x56','0x3e','0x4b','0xc6','0xd2','0x79','0x20','0x9a','0xdb','0xc0','0xfe','0x78','0xcd','0x5a','0xf4'],
       ['0x1f','0xdd','0xa8','0x33','0x88','0x07','0xc7','0x31','0xb1','0x12','0x10','0x59','0x27','0x80','0xec','0x5f'],
       ['0x60','0x51','0x7f','0xa9','0x19','0xb5','0x4a','0x0d','0x2d','0xe5','0x7a','0x9f','0x93','0xc9','0x9c','0xef'],
       ['0xa0','0xe0','0x3b','0x4d','0xae','0x2a','0xf5','0xb0','0xc8','0xeb','0xbb','0x3c','0x83','0x53','0x99','0x61'],
       ['0x17','0x2b','0x04','0x7e','0xba','0x77','0xd6','0x26','0xe1','0x69','0x14','0x63','0x55','0x21','0x0c','0x7d']]
    for i in arr:
        b3=[]        
        for j in i:
            b1=[]
            b2=[]
            if(len(j)<4):
                j=j[0:2]+'0'+j[2:4]            
            f1=int("{0:02d}".format(int(j[2], 16)))
            f2=int("{0:02d}".format(int(j[3], 16)))            
            b1=b1+s[f1]            
            b3.append(b1[f2])
        b.append(b3)
    return(b)


'''AES Shift rows as per row numbers'''    
def shiftrow(arr):
    sr=[]
    num=0  #number of times row is shifted  
    for i in arr:
        sr1=[]
        for j in range(num,len(i)):  #row shifting          
            sr1.append(i[j]) 
        for j in range(0,num):                
            sr1.append(i[j])
        sr.append(sr1)
        num=num+1
    return(sr)


def multiply_by_2(v):
    s = v << 1
    s &= 0xff
    if (v & 128) != 0:
        s = s ^ 0x1b
    return s


def multiply_by_3(v):
    return multiply_by_2(v) ^ v


def MixedColumn(grid):
    new_grid = [[], [], [], []]
    for i in range(4):
        col = [grid[j][i] for j in range(4)]
        col = mix_column(col)
        for i in range(4):
            new_grid[i].append(col[i])
    return new_grid


def mix_column(column):       
    r = [
        multiply_by_2(column[0]) ^ multiply_by_3(
            column[1]) ^ column[2] ^ column[3],
        multiply_by_2(column[1]) ^ multiply_by_3(
            column[2]) ^ column[3] ^ column[0],
        multiply_by_2(column[2]) ^ multiply_by_3(
            column[3]) ^ column[0] ^ column[1],
        multiply_by_2(column[3]) ^ multiply_by_3(
            column[0]) ^ column[1] ^ column[2],
    ]
    return r

def re(column):
    colu=[]
    for i in range(0,4):
        col=column[i]
        co=[]
        for j in range(0,4):                      
            co.append(int(str(col[j]),16))
        colu.append(co)    
    return(colu)

def de(column):
    colu=[]
    for i in range(0,4):
        col=column[i]
        co=[]
        for j in range(0,4):
            q=hex(col[j])
            if(len(q)<4):
                q=q[0:2]+'0'+q[2:4]
            co.append(q)
        colu.append(co)
    
    return(colu)


def rndsche(pub):

    s=[['0x63','0x7c','0x77','0x7b','0xf2','0x6b','0x6f','0xc5','0x30','0x01','0x67','0x2b','0xfe','0xd7','0xab','0x76'],
       ['0xca','0x82','0xc9','0x7d','0xfa','0x59','0x47','0xf0','0xad','0xd4','0xa2','0xaf','0x9c','0xa4','0x72','0xc0'],
       ['0xb7','0xfd','0x93','0x26','0x36','0x3f','0xf7','0xcc','0x34','0xa5','0xe5','0xf1','0x71','0xd8','0x31','0x15'],
       ['0x04','0xc7','0x23','0xc3','0x18','0x96','0x05','0x9a','0x07','0x12','0x80','0xe2','0xeb','0x27','0xb2','0x75'],
       ['0x09','0x83','0x2c','0x1a','0x1b','0x6e','0x5a','0xa0','0x52','0x3b','0xd6','0xb3','0x29','0xe3','0x2f','0x84'],
       ['0x53','0xd1','0x00','0xed','0x20','0xfc','0xb1','0x5b','0x6a','0xcb','0xbe','0x39','0x4a','0x4c','0x58','0xcf'],
       ['0xd0','0xef','0xaa','0xfb','0x43','0x4d','0x33','0x85','0x45','0xf9','0x02','0x7f','0x50','0x3c','0x9f','0xa8'],
       ['0x51','0xa3','0x40','0x8f','0x92','0x9d','0x38','0xf5','0xbc','0xb6','0xda','0x21','0x10','0xff','0xf3','0xd2'],
       ['0xcd','0x0c','0x13','0xec','0x5f','0x97','0x44','0x17','0xc4','0xa7','0x7e','0x3d','0x64','0x5d','0x19','0x73'],
       ['0x60','0x81','0x4f','0xdc','0x22','0x2a','0x90','0x88','0x46','0xee','0xb8','0x14','0xde','0x5e','0x0b','0xdb'],
       ['0xe0','0x32','0x3a','0x0a','0x49','0x06','0x24','0x5c','0xc2','0xd3','0xac','0x62','0x91','0x95','0xe4','0x79'],
       ['0xe7','0xc8','0x37','0x6d','0x8d','0xd5','0x4e','0xa9','0x6c','0x56','0xf4','0xea','0x65','0x7a','0xae','0x08'],
       ['0xba','0x78','0x25','0x2e','0x1c','0xa6','0xb4','0xc6','0xe8','0xdd','0x74','0x1f','0x4b','0xbd','0x8b','0x8a'],
       ['0x70','0x3e','0xb5','0x66','0x48','0x03','0xf6','0x0e','0x61','0x35','0x57','0xb9','0x86','0xc1','0x1d','0x9e'],
       ['0xe1','0xf8','0x98','0x11','0x69','0xd9','0x8e','0x94','0x9b','0x1e','0x87','0xe9','0xce','0x55','0x28','0xdf'],
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
        
        for j in sr1:
            f1=int(j[0],16)            
            f2=int(j[1],16)            
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
        pub1=hex(int(pref,2))
        pub1=pub1[2:]
        if(len(pub1)%32!=0):#satisfy constant length of 128 bits
            fin=32-(len(pub1)%32)
            for i in range(0,fin):
                pub1='0'+pub1
        resc.append(pub1)     
    
    return(resc)


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
                    fe=fe[0:2]+'0'+fe[2:4]
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
            st=st+str(j[2:4])            
    sr="{0:08b}".format(int(st, 16))
    if(len(sr)%128!=0):#satisfy constant length of 128 bits
        fin=128-(len(sr)%128)
        for i in range(0,fin):
            sr='0'+sr
    return(sr)


def AES(text,pubkey2):   
        
    pubkey21=pubkey2[0:32]
    pubkey22=pubkey2[32:64]    
    res1 = "{0:08b}".format(int(text, 16))    
    bindata=res1
    
    if(len(res1)%128!=0):#satisfy constant length of 128 bits
        fin=128-(len(res1)%128)
        for i in range(0,fin):
            bindata='0'+bindata

    cry=''
    strdata1=''
    strdata=''
    rounds=int(len(bindata)/128)
    rk=rndsche(pubkey22)
    for j in range(0,rounds):
        v=0        
        ini=bindata[j*128:(j+1)*128]        
        rnd0=addround(pubkey21,bindata[j*128:(j+1)*128])        
        arr=array(rnd0)
        arr2=shiftrow(arr)        
        arr1=subbyte(arr2)        
        sr4=dearr(arr1)
        for i in range(0,13):
            v=12-i            
            sr5=addround(rk[v],sr4)            
            arr=array(sr5)            
            arr=re(arr)
            arr3=MixedColumn(arr)
            arr3=MixedColumn(arr3)
            arr3=MixedColumn(arr3)
            arr3=de(arr3)            
            arr2=shiftrow(arr3)            
            arr1=subbyte(arr2)            
            sr4=dearr(arr1)
            ini=sr4
        
        sr5=sr4        
        cry=cry+sr5
    
    for i in range(0, len(cry), 8):
        temp= cry[i:i + 8]
        decimal_data = int(temp,2)        
        strdata1 = strdata1 + chr(decimal_data)  
    
    for i in range(0,len(strdata1)):        
        if(strdata1[i]!='\x00'):            
            strdata=strdata1[i:len(strdata1)]
            break
    
    return(strdata)

    
def inp(pri,Text,shkey2):
    tr=pri
    fr=shkey2
    pkey2=str(int(tr)*int(fr))
    pubkey2=hex(int(pkey2))    
    pubkey2=pubkey2[2:67]
    
    return (AES(Text,pubkey2))

(pri,pub)=Elliptic_crypto()

def share_key():
    return(pub)

def AES_Decrypt(cipher,shkey):
    ans=inp(pri,cipher,shkey)    
    return(ans)
