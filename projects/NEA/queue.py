class Queue:
    def __init__(self):
        self.__list = []

    def push(self, item):
        self.__list.append(item)
    
    def pull(self):
        if self.__list == []:
            return None
        else:
            return self.__list.pop(0)
        
    def search(self, item):
        for i in self.__list:
            if i == item:
                return True
        return False
    
    def empty(self):
        if self.__list == []:
            return True
        else:
            return False