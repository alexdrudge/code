class Priority:
    def __init__(self):
        self.__list = []
    
    def push(self, item, weight):
        if self.__list == []:
            self.__list.append([item, weight])
        else:
            inserted = False
            for i in range(len(self.__list)):
                # binary sort to place the item
                if weight <= self.__list[i][1] and not inserted:
                    self.__list.insert(i, [item, weight])
                    inserted = True
            if not inserted:
                self.__list.append([item, weight]) # place at the end if its the largest item
    
    def pull(self):
        if self.__list == []:
            return None
        else:
            return self.__list.pop(0)
    
    def reweigh(self, item, weight):
        for i in range(len(self.__list)):
            if self.__list[i][0] == item:
                self.__list.pop(i) # remove the item from the queue
                self.push(item, weight) # add the item back to the queue

    def get_weight(self, item):
        for i in self.__list:
            if i[0] == item:
                return i[1]
        return None

    def search(self, item):
        for i in self.__list:
            if i[0] == item:
                return True
        return False
    
    def empty(self):
        if self.__list == []:
            return True
        else:
            return False