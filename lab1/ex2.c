#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#include <stdlib.h>

int main() {

	/* Open an executable file here */
	FILE* dummy_file_ptr = fopen("./bin/dummy", "r");

	const long offset_for_foo = 0x1106; // 0000000000401106 <foo> (File Offset: 0x1106):
	size_t foo_size = 0x1150 - 0x1106; // 0000000000401150 <main> (File Offset: 0x1150) since main is after the foo function
	int prot = PROT_EXEC | PROT_READ | PROT_WRITE; // we need to read and execute the code of foo; also we need to write to the allocated memory :)
	int fd = dummy_file_ptr->_fileno; // get the file descriptor from the FILE* of the opened executable file

	void *ptr = mmap(NULL, foo_size, prot, MAP_PRIVATE | MAP_ANON, fd, 0); // I don't think fd is used since we use MAP_ANON

	int res = fseek(dummy_file_ptr, offset_for_foo, SEEK_SET);  // Move from start of file to offset_for_foo
	if(res != 0){
		printf("fseek error");
		return res;
	}
	/* Copy the bytes here */
	void * aux = malloc(foo_size);
	fread(aux, 1, foo_size, dummy_file_ptr);
	memcpy(ptr, aux, foo_size);
	free(aux);

	/* This monster casts ptr to a function pointer with no args and calls it. Basically jumps to your code. */
	(*(void(*)()) ptr)();

	// Cleanup
	munmap(ptr, foo_size);
	fclose(dummy_file_ptr);
}
