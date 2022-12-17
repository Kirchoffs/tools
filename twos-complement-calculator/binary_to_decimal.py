def binary_to_decimal(binary_string, length):
    if len(binary_string) == 0:
        print("Empty input")
        return -1
        
    if len(binary_string) > length:
        print("The length does not match")
        return -1
    
    first_bit = binary_string[0] if len(binary_string) == length else 0
    
    res = 0
    if first_bit == '0':
        for digit in binary_string:
            if digit != '0' and digit != '1':
                print("Not valid binary expression")
                return -1
            res = res * 2 + int(digit)
    else:
        for digit in binary_string:
            if digit != '0' and digit != '1':
                print("Not valid binary expression")
                return -1
            res = res * 2 + (1 - int(digit))
        res += 1
        res = -res
    
    return res

while True:
    binary_string, length = input("Input binary string and its length: ").split()
    print(binary_to_decimal(binary_string, int(length)))