def decimal_to_binary(decimal, length):
    sign = 0 if int(decimal) >= 0 else 1
    
    decimal = abs(int(decimal))
    bits = []
    while decimal > 0:
        bits.append(decimal & 1)
        decimal >>= 1
    
    if sign == 1:
        i = 0
        while i < len(bits) and bits[i] == 0:
            i += 1
            
        if i < len(bits):
            bits[i] = 1
            i += 1
        elif i + 1 < length:
            bits.append(1)
        
        while i < len(bits):
            bits[i] = 1 - bits[i]
            i += 1
    
    while len(bits) < length:
        bits.append(sign)
        
    bits.reverse()
    
    return "".join(map(lambda bit: str(bit), bits))

while True:
    decimal, length = input("Input decimal and its binary number of bits: ").split()
    print(decimal_to_binary(decimal, int(length)))