class Node(object):
    def __init__(self,NodeDegree):
        self.NodeDegree=NodeDegree
        self.NodeData=[None]*(self.NodeDegree)
        self.Children=[None]*(self.NodeDegree+1)
        self.NodeisLeaf=True
        self.NodeisRoot=True
        self.Next=None
    def NodeInsert(self,Value,Child):
        if self.NodeData[0]==None:
            self.NodeData[0]=Value
            self.Children[0]=Child
        i=self.NodeDegree-1
        while(self.NodeData[i]==None):
            i=i-1
        if Value>self.NodeData[i]:
            self.NodeData[i+1]=Value
            self.Children[i+2]=Child
            return
        while(i>=0 and Value<self.NodeData[i] ):
            self.NodeData[i+1]=self.NodeData[i]
            self.Children[i+2]=self.Children[i+1]
            i=i-1
            if i>=0 and Value>self.NodeData[i]:
                self.NodeData[i+1]=Value
                self.Children[i+2]=Child
                break
        if i==-1:
            self.NodeData[i+1]=Value
            self.Children[i+2]=Child
            return
class BTree(object):
    def __init__(self, NodeDegree):
        self.NodeDegree=NodeDegree
        self.root=Node(self.NodeDegree)
        self.root.NodeisRoot=True
        self.splitNode=[None,None,None]
    def InsertRoot(self,Data):
        self.Insert(self.root,Data)
        if self.splitNode[0]!=None:
            NewRoot=Node(self.NodeDegree)
            if self.splitNode[1].NodeisLeaf:
                data,left,right=self.SplitLeafNode(self.splitNode[1],self.splitNode[0])
            else:
                data,left,right=self.SplitNonLeafNode(self.splitNode[1],self.splitNode[0],self.splitNode[2])
            splitNode=[None,None,None]
            NewRoot.NodeData[0]=data
            NewRoot.Children[0]=left
            NewRoot.Children[1]=right
            NewRoot.NodeisLeaf=False
            self.root=NewRoot

    def Insert(self,Node,Data):
        if Node.NodeisLeaf:
            l=len(Node.NodeData)
            if Node.NodeData[l-1]==None:
                Node.NodeInsert(Data,None)
                self.splitNode=[None,None,None]
            else:
                self.splitNode[0]=Data
                self.splitNode[1]=Node
        else:
            l=len(Node.NodeData)
            i=l-1
            while Node.NodeData[i]==None or Data < Node.NodeData[i] and i>0:
                i=i-1
            if i==0 and Data< Node.NodeData[i]:
                self.Insert(Node.Children[0],Data)
            elif i==0 and Data>Node.NodeData[i]:
                self.Insert(Node.Children[i+1],Data)
            else:
                self.Insert(Node.Children[i+1],Data)
            if self.splitNode[0]!=None:
                if self.splitNode[1].NodeisLeaf:
                    data,left,right=self.SplitLeafNode(self.splitNode[1],self.splitNode[0])
                else:
                    data,left,right=self.SplitNonLeafNode(self.splitNode[1],self.splitNode[0],self.splitNode[2])

                if Node.NodeData[l-1]==None:
                    Node.NodeInsert(data,right)
                    self.splitNode=[None,None,None]
                else:
                    self.splitNode[0]=data
                    self.splitNode[1]=Node
                    self.splitNode[2]=right

    def SplitLeafNode(self,Node1,Data):
        l=len(Node1.NodeData)
        i=int(l/2)
        Right=Node(Node1.NodeDegree)
        while i<=l-1 and (Node1.NodeData[i])!=None:
            Right.NodeData[i-int(l/2)]=Node1.NodeData[i]
            Node1.NodeData[i]=None
            i=i+1
        if Right.NodeData[0]!=None and Data>Right.NodeData[0]:
            Right.NodeInsert(Data,None)
        else:
            Node1.NodeInsert(Data,None)
        Node1.Next=Right
        return Right.NodeData[0],Node1,Right

    def SplitNonLeafNode(self,Node1,Data,Pointer):
        #print(Node1.NodeData,Data,Pointer.NodeData)
        l=len(Node1.NodeData)
        temp=[None]*(l+1)
        tempChild=[None]*(l+2)
        i=0
        while i<l:
            temp[i]=Node1.NodeData[i]
            i=i+1
        i=0
        while i<l+1:
            tempChild[i]=Node1.Children[i]
            i=i+1
        i=l-1
        while i>=0 and Data<=temp[i]:
            temp[i+1]=temp[i]
            tempChild[i+2]=tempChild[i+1]
            i=i-1
        temp[i+1]=Data
        tempChild[i+2]=Pointer
        Right=Node(Node1.NodeDegree)
        leng=len(temp)
        Right.NodeData=temp[int(leng/2)+1:]
        Node1.NodeData=temp[:int(leng)/2]
        while len(Right.NodeData)<Right.NodeDegree:
            Right.NodeData.append(None)
        while len(Node1.NodeData)<Node1.NodeDegree:
            Node1.NodeData.append(None)
        Right.Children=tempChild[int(leng/2)+1:]
        while len(Right.Children) < Right.NodeDegree+1:
            Right.Children.append(None)
        Node1.Children=tempChild[:int(leng/2)+1]
        while len(Node1.Children)< Node1.NodeDegree+1:
            Node1.Children.append(None)
        Right.NodeisLeaf=False
        Node1.NodeisLeaf=False
        return temp[int(leng/2)],Node1,Right

    def traverse(self,Node1):
        if Node1!=None and Node1.NodeisLeaf==True:
            print (Node1.NodeData)
        elif Node1==None:
            return
        i=0
        l=len(Node1.NodeData)
        while i<l and Node1.Children[i]!=None:
            self.traverse(Node1.Children[i])
            i=i+1
        self.traverse(Node1.Children[i])
    def search(self,key,Node1):
        i=0
        while Node1!=None and i<Node1.NodeDegree and Node1.NodeData[i]!=None:
            if Node1.NodeData[i]!=None and key<=Node1.NodeData[i]:
                break
            i=i+1
        if  i<len(Node1.NodeData)  and Node1.NodeData[i]!=None and Node1.NodeData[i]==key:
            return True
        elif Node1.NodeisLeaf:
            return False
        if i==0:
            return self.search(key,Node1.Children[0])
        return self.search(key,Node1.Children[i])
    def count(self,key,Node1):
        if Node1.NodeisLeaf:
            count=0
            for i in range(len(Node1.NodeData)):
                if Node1.NodeData[i]!=None and Node1.NodeData[i]==key:
                    count=count+1
            return count

        i=0
        while Node1!=None and i<Node1.NodeDegree and Node1.NodeData[i]!=None:
            if Node1.NodeData[i]!=None and key<Node1.NodeData[i]:
                break
            i=i+1
        if i==0:
            return self.count(key,Node1.Children[0])
        return self.count(key,Node1.Children[i])

    def rangesearch(self,key1,key2,Node1):
        if Node1.NodeisLeaf:
            count=0
            index=-1
            for i in range(len(Node1.NodeData)):
                if Node1.NodeData[i]!=None and Node1.NodeData[i]==key1:
                    index=i
                    break
            if index==-1:
                return 0
            temp=Node1
            value=key1
            while value!=key2 and temp!=None:
                index=index+1
                if index==len(temp.NodeData)-1:
                    index=0
                    temp=temp.Next
                count=count+1
            return count+1

        i=0
        while Node1!=None and i<Node1.NodeDegree and Node1.NodeData[i]!=None:
            if Node1.NodeData[i]!=None and key1<Node1.NodeData[i]:
                break
            i=i+1
        if i==0:
            return self.rangesearch(key1,key2,Node1.Children[0])
        return self.rangesearch(key1,key2,Node1.Children[i])


test=BTree(2)
# test.InsertRoot(1)
# test.InsertRoot(2)
# test.InsertRoot(3)

i=1
while i<=100:
    test.InsertRoot(i)
    i=i+1
#test.traverse(test.root)
if test.search(1,test.root):
    print("found")
print(test.count(101,test.root))
print(test.rangesearch(101,102,test.root))
