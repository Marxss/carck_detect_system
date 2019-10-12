

def readData(file_path):
    file=open(file_path)
    vertexs=[]
    vnorms=[]
    line=file.readline()
    while line:
        line=line.split()
        if line[0]=='facet':
            vnorms.append(list(map(float,[line[2],line[3],line[4]])))
        if line[0]=='vertex':
            vertexs.append(list(map(float,[line[1],line[2],line[3]])))
        line=file.readline()
    file.close()
    return vertexs,vnorms


if __name__ == "__main__":
    vertexs, vnorms=readData('gear.stl')
    print(vertexs[0][0])