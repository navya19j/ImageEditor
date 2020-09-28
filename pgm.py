# name: File path of the pgm image file
# Output is a 2D list of integers
def readpgm(name):
    image = []
    with open(name) as f:
        lines = list(f.readlines())
        if len(lines) < 3:
            print("Wrong Image Format\n")
            exit(0)

        count = 0
        width = 0
        height = 0
        for line in lines:
            if line[0] == '#':
                continue

            if count == 0:
                if line.strip() != 'P2':
                    print("Wrong Image Type\n")
                    exit(0)
                count += 1
                continue

            if count == 1:
                dimensions = line.strip().split(' ')
#               print(dimensions)
                width = dimensions[0]
                height = dimensions[1]
                count += 1
                continue

            if count == 2:  
                allowable_max = int(line.strip())
                if allowable_max != 255:
                    print("Wrong max allowable value in the image\n")
                    exit(0)
                count += 1
                continue

            data = line.strip().split()
            data = [int(d) for d in data]
            image.append(data)
    return image    

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
    with open(file, 'w') as fout:
        if len(img) == 0:
            pgmHeader = 'p2\n0 0\n255\n'
        else:
            pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
            fout.write(pgmHeader)
            line = ''
            for i in img:
                for j in i:
                    line += str(j) + ' '
            line += '\n'
            fout.write(line)

def averagepgm(x,H,W):
    
    l=[0]*H
    for i in range (len(x)):
        l[i]=x[i][::]

    for i in range (1,H-1):
        for j in range (1,W-1):
            l[i][j]=int((x[i-1][j-1]+x[i-1][j+1]+x[i][j-1]+x[i][j]+x[i][j+1]+x[i+1][j]+x[i+1][j+1]+x[i-1][j]+x[i+1][j-1])/9)
    return l
    
def hdif(i,j,x):

    y=((x[i-1][j-1]-x[i-1][j+1]) + 2*(x[i][j-1]-x[i][j+1]) + (x[i+1][j-1]-x[i+1][j+1]))
    return y

def vdif(i,j,x):
    
    y=((x[i-1][j-1]-x[i+1][j-1]) + 2*(x[i-1][j]-x[i+1][j]) + (x[i-1][j+1]-x[i+1][j+1]))
    return y

def grad(i,j,x):
    
    y=int((hdif(i,j,x)*hdif(i,j,x) + vdif(i, j,x)*vdif(i,j,x))**(1/2))
    return y

def edgedetection(x,H,W):

    image=[[0 for m in range (W+2)]for n in range (H+2)]

    for i in range (0,H):
        for j in range (0,W):
            image[i+1][j+1]=x[i][j]

    a=[]
    for i in range (1,H+1):
        for j in range (1,W+1): 
            a.append(grad(i,j,image))

    k=max(a)
    
    l=[0]*(H+2)
    for i in range (len(image)):
        l[i]=image[i][::]

    for i in range (1,H+1):
        for j in range (1,W+1):
            l[i][j]=int(((grad(i,j,image))/k)*255)

    k=[[0 for m in range (W)]for n in range (H)]

    for i in range (0,H):
        for j in range (0,W):
            k[i][j]=l[i+1][j+1]

    return k

def nenergymatrix(y,H,W):
  energy=[0]*H
  for i in range (len(y)):
    energy[i]=y[i][::]
  for i in range (0,H):
    for j in range (0,W):
      if i==0:
        energy[i][j]=y[i][j]
      elif j==0:
        energy[i][j]=y[i][j] + min(energy[i-1][j], energy[i-1][j+1])
      elif j==W-1:
        energy[i][j] = y[i][j] + min(energy[i-1][j-1], energy[i-1][j])
      else:
        energy[i][j] = y[i][j] + min(energy[i-1][j-1], energy[i-1][j], energy[i-1][j+1])

  return energy

def energymatrix(y,H,W):
    a=nenergymatrix(y,H,W)
    b=[]
    for i in range (0,H):
        for j in range (0,W):
            b.append(a[i][j])
    m=max(b)
    for i in range (0,H):
        for j in range (0,W):
                a[i][j]=int(((a[i][j])/m)*255)
    return a

def minabove(k,H,W):
  i=k[0]
  j=k[1]
  m=energymatrix(y,H,W)
  if j==0:
    if m[i-1][j]>m[i-1][j+1]:
        return (i-1,j+1)
    elif m[i-1][j]<m[i-1][j+1]:
        return (i-1,j)
    else:
        return (i-1,j,i-1,j+1)
  elif j==W-1:
    if m[i-1][j]>m[i-1][j-1]:
        return (i-1,j-1)
    elif m[i-1][j]<m[i-1][j-1]:
        return (i-1,j)
    else:
        return (i-1,j-1,i-1,j)
        
  else:
    if m[i-1][j]>=m[i-1][j+1]>m[i-1][j-1] or m[i-1][j+1]>=m[i-1][j]>m[i-1][j-1] :
        return (i-1,j-1)
    elif m[i-1][j+1]>=m[i-1][j-1]>m[i-1][j] or m[i-1][j-1]>=m[i-1][j+1]>m[i-1][j] :
        return (i-1,j)
    elif m[i-1][j-1]>=m[i-1][j]>m[i-1][j+1] or m[i-1][j]>=m[i-1][j-1]>m[i-1][j+1] :
        return (i-1,j+1) 
    elif m[i-1][j]>m[i-1][j+1]==m[i-1][j-1] :
        return (i-1,j+1,i-1,j-1)
    elif m[i-1][j-1]>m[i-1][j]==m[i-1][j+1]:
        return (i-1,j,i-1,j+1)
    elif m[i-1][j+1]>m[i-1][j-1]==m[i-1][j]:
        return (i-1,j-1,i-1,j)
    elif m[i-1][j+1]==m[i-1][j-1]==m[i-1][j]:
        return (i-1,j-1,i-1,j,i-1,j+1)


def leastenergypath(x,y,m,H,W):
  s=[]
  l=[]
  k=m[H-1][::]
  a=min(m[H-1][::])
  c=k.count(a)
  i=0
  j=0
  while i<len(k) and j!=c:
    if k[i]==a:
      s.append((H-1,i))
      x[H-1][i]=255
      i=i+1
      j=j+1
    else:
      i=i+1

  flag=True
  while len(s)!=0 and flag :
    temp=s[len(s)-1]
    if temp != None and len(temp)==2:
      a=s.pop()
      i=temp[0]
      j=temp[1]
      x[i][j]=255
      if i==0:
        flag=False
      else:
        s.append(minabove(temp,H,W))
    elif temp != None and len(temp)==4:
      a=s.pop()
      if i==0:
        flag=False
      else:
        s.append(minabove(temp[0:2],H,W))
        s.append(minabove(temp[2:4],H,W))
      i=temp[0]
      j=temp[1]
      k=temp[2]
      l=temp[3]
      x[i][j]=255
      x[k][l]=255

    elif temp != None and len(temp)==6:
      a=s.pop()
      i=temp[0]
      j=temp[1]
      k=temp[2]
      l=temp[3]
      m=temp[4]
      n=temp[5]
      x[i][j]=255
      x[k][l]=255
      x[m][n]=255
      if i==0:
        flag=False
      else:

        s.append(minabove(temp[0:2],H,W))
        s.append(minabove(temp[2:4],H,W))
        s.append(minabove(temp[4:6],H,W))
    else:  
      s.pop()


  return x


#Function Calls

x = readpgm('test.pgm')

H=len(x)

W=len(x[0][::])

z=averagepgm(x,H,W)
print(z)

y=edgedetection(x,H,W)
print(y)

w=energymatrix(y,H,W)
print(w)

k=leastenergypath(x,y,w,H,W)
print(k)


writepgm(readpgm('flower_gray.pgm'),'input.pgm')
writepgm(z,'average.pgm')
writepgm(y,'edge.pgm')
writepgm(k,'energy.pgm')



            # test.pgm is the image present in the same working directory