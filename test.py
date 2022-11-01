import os

#pat = '/home/cappittall/Documents/ekmeksay/models/'
pat = '/home/mendel/ekmeksay/model/'
version= str(max([int(i) for i in os.listdir(pat) if i.isdigit()]))
model= pat+'modelv' + version + '_edgetpu.tflite'
