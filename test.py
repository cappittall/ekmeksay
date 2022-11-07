import os

#pat = '/home/cappittall/Documents/ekmeksay/models/'
pat = '/home/mendel/ekmeksay/model/'
version= str(max([int(i) for i in os.listdir(pat) if i.isdigit()]))
model= pat+'modelv' + version + '_edgetpu.tflite'

sayi=12345678910111213
for i in range(2,sayi):
    if sayi % (i) ==0:
        print(i, 'Sayısına bölündü')

        