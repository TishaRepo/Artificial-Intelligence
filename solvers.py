class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far.
        self.best_state = None  

    def search(self, start_state):
   
        new_conf={}
        for key, value in self.conf_matrix.items():

            for i in value :
                if i in new_conf :
                    new_conf[i].append(key)
                else :
                    new_conf[i]=[key]
        self.conf_matrix=new_conf

        self.best_state = start_state
        self.best_cost = self.cost_fn(start_state)

        self.frontier={}
        self.explored = []
        word_list = start_state.split()
        word_list = [Node(index,word)for index,word in enumerate(word_list)]

        for node in word_list:
            for index,letter in enumerate(node.word) :
                if letter in self.conf_matrix:
                    mods=self.conf_matrix[letter]
                else :
                    node.nid[index]=-2
                node.mods.append(mods)

            new_entry=node.expand()
            for entry in new_entry :
                temp_list = word_list.copy()
                temp_list[entry.index]= entry
                temp_state=' '.join([temp.word for temp in temp_list])
                temp_cost = self.cost_fn(temp_state)
                self.frontier[str(entry.index)+':'+str(entry.nid)]= [temp_cost,entry]

        total_cost=0
        while self.frontier :
            total_cost+=1
            curr_key = self.frontier_select()
            curr_node =self.frontier[curr_key][1]
            curr_list=word_list.copy()
            curr_list[curr_node.index]=curr_node
            curr_state=' '.join([curr.word for curr in curr_list])
            curr_cost = self.cost_fn(curr_state)

            if curr_cost<=self.best_cost :
                word_list[curr_node.index]=curr_node
                self.best_cost=curr_cost
                self.best_state=curr_state
                self.refresh(word_list)
                #print(self.best_state,total_cost,curr_cost)
            
            #print(curr_state,total_cost,curr_cost)


            new_entry=curr_node.expand()
            self.explored.append(curr_key)
            del self.frontier[curr_key]

            for entry in new_entry :
                new_key = str(entry.index)+':'+str(entry.nid)
                if new_key not in self.explored:
                    temp_list = word_list.copy()
                    temp_list[entry.index]= entry
                    temp_state=' '.join([temp.word for temp in temp_list])
                    temp_cost = self.cost_fn(temp_state)
                    self.frontier[new_key]= [temp_cost,entry]


    def frontier_select(self):

        to_sort = [self.frontier[key][0] for key in self.frontier]
        value = min(to_sort)
        length = -1
        candidate = None
        for key in self.frontier :
            if self.frontier[key][0]==value:
                return key

    def refresh(self,word_list):
        for key in self.frontier :
            temp_list = word_list.copy()
            temp_list[self.frontier[key][1].index]= self.frontier[key][1]
            temp_state=' '.join([temp.word for temp in temp_list])
            temp_cost = self.cost_fn(temp_state)
            self.frontier[key][0]=temp_cost


class Node():
    def __init__(self,index,word):
        self.index=index
        self.word=word
        self.nid =[-1 for letter in word]
        self.mods =[]
    def expand(self):
        new_entry=[]
        for index,mod in enumerate(self.nid) :
            if self.nid[index]==-1 :
                for j,i in enumerate(self.mods[index]):
                    new_node=Node(self.index,self.word[:index]+i+self.word[index+1:])
                    new_node.mods=self.mods
                    new_node.nid = self.nid.copy()
                    new_node.nid[index]= j
                    new_entry.append(new_node)
                
        return new_entry


