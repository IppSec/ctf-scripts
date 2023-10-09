CC = gcc
CFLAGS = -z execstack -fno-stack-protector -g
TARGET = shellcode.elf 
SRC = main.c

$(TARGET): $(SRC)
	$(CC) -o $(TARGET) $(SRC) $(CFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: clean
