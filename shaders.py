import libmat
import math

def vShader(verx, **kwarg):
    mdmat=kwarg["mdmat"]
    viewmat=kwarg["viewmat"]
    projecmat=kwarg["projecmat"]
    vpmat=kwarg["vpmat"]
    vt=[verx[0],verx[1],verx[2],1]
    matrs=libmat.nmult([vpmat, projecmat, viewmat, mdmat])
    vt=libmat.mvmult(matrs, vt)
    vt=[vt[0]/vt[3],vt[1]/vt[3],vt[2]/vt[3],vt[3]/vt[3]]
    return vt

def fShader(**kwarg):
    tcrds=kwarg["tcrds"]
    textura=kwarg["textu"]
    if textura is None:
        return textura.obtener_color(tcrds[0], tcrds[1])
    else:
        return (1,1,1)    
    
def gShader(**kwarg):
    r=g=b=1
    textura=kwarg["textu"]
    tc, tc2, tc3=kwarg["tcrds"]
    n, n2, n3=kwarg["normales"]
    luzdir=kwarg["dluz"]
    x,y,z=kwarg["bcrds"]
    mdmat=kwarg["mdmat"]
    if textura is not None:
        i=tc[0]*x+tc2[0]*y+tc3[0]*z
        j=tc[1]*x+tc2[1]*y+tc3[1]*z
        r,g,b=textura.obtener_color(i,j)
    nr=libmat.nrv(libmat.mvmult(mdmat,[x*n[0]+y*n2[0]+z*n3[0],x*n[1]+y*n2[1]+z*n3[1],x*n[2]+y*n2[2]+z*n3[2],0]))
    it=libmat.prodpunto(nr,libmat.negativev(luzdir))
    if it<0:
        return [0,0,0]
    r,g,b=min(r*it,1),min(g*it,1),min(b*it,1)
    return r,g,b

def invShader(**kwarg):
    r, g, b=gShader(**kwarg)
    return 1-r,1-g,1-b

def pixelShader(**kwarg):    
    r, g, b=gShader(**kwarg)
    for i in range(0,5):
        if i/5>r:
            r=i/5
            break
    for i in range(0,5):
        if i/5>g:
            g=i/5
            break
    for i in range(0,5):
        if i/5>b:
            b=i/5
            break
    return r,g,b
def darkShader(**kwarg):
    r, g, b=gShader(**kwarg)
    return r*0.5,g*0.5,b*0.5

def briShader(**kwarg):
    r, g, b=gShader(**kwarg)
    return r*1.5,g*1.5,b*1.5

def ruShader(**kwarg):
    clr=[0,0,0]
    textura=kwarg["textu"]
    tc, tc2, tc3=kwarg["tcrds"]
    x,y,z=kwarg["bcrds"]
    if textura is not None:
        i=tc[0]*x+tc2[0]*y+tc3[0]*z
        j=tc[1]*x+tc2[1]*y+tc3[1]*z
        r,g,b=textura.obtener_color(i,j)
        paso=0
        ruido=0.1
        for py in range(-1,2):
            for px in range(-1,2):
                ptx=i+px*ruido
                pty=j+py*ruido
                c=textura.obtener_color(ptx,pty)
                paso+=1
                for i in range(0,3):
                    
                    clr[i]+=c[i]
        return clr[0]/paso,clr[1]/paso,clr[2]/paso
    else:
        return (1,1,1)
    
def shadow(**kwarg):
    r, g, b=gShader(**kwarg)
    for i in range(0,10):
        if 0.1*i>r:
            r=0.1*i
            break
    for i in range(0,10):
        if 0.1*i>g:
            g=0.1*i
            break
    for i in range(0,10):
        if 0.1*i>b:
            b=0.1*i
            break
    return r,g,b