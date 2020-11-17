print('00' * 256)

data_string = ''
for i in range(256):
    data_string += 'data[%s],' % i

print(data_string)