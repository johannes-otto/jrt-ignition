data=range(100)
with open('ignition_table.txt','w') as file:
  file.write('\n'.join(map(lambda x: str(500),data)))
