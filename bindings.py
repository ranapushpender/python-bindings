#Stats
import os
import subprocess

program = 'docker'
stop_command = 'stop'

def createProcess(options):
    process = subprocess.Popen(options,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    stdout,stderr = process.communicate()
    return (stdout.decode('UTF-8'),stderr.decode('UTF-8'),len(stderr.decode('UTF-8'))>0)

def createProcessSingleine(options):
    process = subprocess.Popen(options,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    result = process.stdout.readline().decode('UTF-8')
    result = process.stdout.readline().decode('UTF-8')
    process.terminate()
    return result

    
class Container:
    def __init__(self,l):
        self.cid = l[0]
        self.image = l[1]
        self.status = l[4]
        #self.port = l[5]
        self.name = l[1]
        
    def stop(self,options=[]):
        options = [program,stop_command]+options+[self.cid]
        process = createProcess(options)
        return process
    
    def start(self,options=[]):
        options = [program,'start']+options+[self.cid]
        process = createProcess(options)
        return process
    
    def delete(self,options=[]):
        self.stop()
        options = [program,'rm']+options+[self.cid]
        process = createProcess(options)
        return process
    
    def stats(self):
        options = [program,'stats']+[self.cid]
        text = createProcessSingleine(options)
        text = text.split('  ')
        text = list(filter(lambda w : w!='' and w!=' ',text))
        return {
            "name" : text[1],
            "cpu" : text[2],
            "ram_limit" : text[3],
            "ram" : text[4],
            "io" :text[5],
            "block_io":text[6],
            "pid" : text[7]
            
        }
        

class Docker:
    def __init__(self):
        self.name="docker"
    def getContainers(self):
        result = createProcess(['docker','ps','-a'])
        objs = []
        if not result[2]:
            text = result[0]
            text = text.split('\n')
            text = text[1::]
            for index,line in enumerate(text):
                text[index] = text[index].split('  ')
                text[index] = list(filter(lambda element : element.rstrip()!='' and element.lstrip!='',text[index]))
                if(len(text[index])>0):
                    objs.append(Container(text[index]))
        return objs
    def findContainer(self,cid):
        containers = self.getContainers()
        for container in containers:
            if container.cid == cid:
                return container
        return None
    def createContainer(self,options):
        options = ['docker','run','-d']+options.split(' ')
        result = createProcess(options)
        return result
                

docker = Docker()
container = docker.findContainer("fa4a09c8d092")
stats = container.stats()
for key,value in stats.items():
    print("{} : {}".format(key,value))
container.start()
stats = container.stats()
for key,value in stats.items():
    print("{} : {}".format(key,value))
