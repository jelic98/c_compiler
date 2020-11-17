int main() {
	int start;
	int finish;

	printf("Unesite dva pozitivna cela broja: ");
	scanf("%d%d", &start, &finish);

	int i;

	for(i = start; i < finish; i = i + 1) {
		printf("Element #%d: %d\n", i - start + 1, i);
	}

	return 0;
}
