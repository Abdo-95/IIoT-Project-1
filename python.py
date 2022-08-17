from opcua import Server
from datetime import datetime
import time
import string
import random
from time import sleep
now = datetime.now()
# now setup our server
myserver = Server ()    
# Seting the Server endpoint, the port should be exposed in the Dockerfile befor building the images
url = "opc.tcp://0.0.0.0:4848"
myserver.set_endpoint(url)
# Seting the Server name
name = "OPCUA_TEST_Server"
addspace = myserver.register_namespace(name)
node = myserver.get_objects_node()
param = node.add_object(addspace, "Parameters")
t_text1 = param.add_variable(addspace, "Text1", "Bravo")
i_int1  = param.add_variable('ns = 3;s="Sort1"', "myinteger1", "1")
b_bool1 = param.add_variable('ns = 3;s="Sort2"' , "mybool1", "True")
hight_mes = param.add_variable('ns=3;s="Sort3"', "Hight station", "0,45")
#setting the variables to Writable to be able to change the values 
t_text1.set_writable() 
i_int1.set_writable()
b_bool1.set_writable()
#starting the Server
myserver.start()
print("Server started at ()". format(url))
print("At ", now)

print("This is the way to do it ") 
#this function will return random  uppercase + lowercase from the asci table and will join them together in one string
def randStr(chars = string.ascii_uppercase + string.ascii_lowercase , N=5):
	return ''.join(random.choice(chars) for _ in range(N))
  
while True: #functions used here are to contiusly change the values of the datapoints
  i_int1.set_value(random.randint(0, 1000))
  b_bool1.set_value(random.choice([True, False]))
  t_text1.set_value(randStr())
  hight_mes.set_value(random.randint(0, 1000))
  a = hight_mes.get_value() 
  b = i_int1.get_value()
  c = t_text1.get_value()
  d = b_bool1.get_value()
  print (a , b , c , d)
  sleep (3)
