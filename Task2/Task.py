import argparse, os
from random import shuffle

script_dir = os.path.dirname(__file__)

class TaskHandler:

    def __init__(self):

        self.task_db = {}
        self.task_entry = {}

    def _transform_(self,msg):
        if msg['task_id'] not in self.task_db:
            self.task_entry = {'task_name': None, 'num_values': None, 'values': []}
            if 'task_name' in msg:
                self.task_entry['task_name'] = msg['task_name']
                self.task_entry['num_values'] = msg['num_values']
            else:
                self.task_entry['values'].append(msg['value'])
            self.task_db[msg['task_id']] = self.task_entry
        else:
            self.task_entry = self.task_db[msg['task_id']]
            if 'task_name' in msg:
                self.task_entry['task_name'] = msg['task_name']
                self.task_entry['num_values'] = msg['num_values']
            else:
                self.task_entry['values'].append(msg['value'])

    def _sum_(self,task_id):
        result = sum(self.task_entry['values'])
        self._get_(task_id,result)

    def _min_(self,task_id):
        result = min(self.task_entry['values'])
        self._get_(task_id,result)

    def _max_(self,task_id):
        result = max(self.task_entry['values'])
        self._get_(task_id,result)

    def _mean_(self,task_id):
        result = sum(self.task_entry['values']) / len(self.task_entry['values'])
        self._get_(task_id,result)

    def _count_(self,task_id):
        result = len(self.task_entry['values'])
        self._get_(task_id,result)

    def _get_(self,task_id,result):
        print("Task", task_id, ":", result)

    def receive_msg(self, msg):
        
        self._transform_(msg)
        
        if (self.task_entry['num_values'] is not None and
            len(self.task_entry['values']) == self.task_entry['num_values'] and
            self.task_entry['task_name'] is not None):
            
            foo = { 'sum':self._sum_ , 'min':self._min_ , 'max':self._max_ , 'mean':self._mean_ , 'count':self._count_ }
            try: 
                foo[self.task_entry['task_name']](msg['task_id'])
            except:
                print('Task', msg['task_id'], ': Not a Valid Task')


def run(scenario):
    """
    This function run the scenarios an call the receive_msg function of the TaskHandler.
    This function should not be changed.                                  #Acknowledged
    """
    with open(scenario) as h:
        lines = h.readlines()

    task_msgs = []
    for line in lines:
        line = line.strip()
        entries = line.split(' ')
        task_id = entries[0]
        task_name = entries[1]
        values = [int(e) for e in entries[2:]]
        task_msgs.append({'task_id': task_id, 'task_name': task_name, 'num_values': len(values)})

        for val in values:
            task_msgs.append({'task_id': task_id, 'value': val})

    shuffle(task_msgs)
    th = TaskHandler()

    for msg in task_msgs:
        th.receive_msg(msg)


if __name__ == '__main__':
    # You shouldn't have to tough anything here
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--scenario', type=int, default=None,
                        help='If set will run only a specific scenario. For example 0 for the first 1 for the second and so on.')
    args = parser.parse_args()

    scenearios = [script_dir+'\scenario1.txt',script_dir+'\scenario2.txt', script_dir+'\scenario3.txt']
    if args.scenario is not None:
        scenearios = scenearios[args.scenario:args.scenario + 1]

    for s in scenearios:
        print('*' * 35)
        print('Running scenario:', s)
        print('*' * 35)
        run(s)
        print()
