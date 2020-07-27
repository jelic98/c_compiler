int main() {
	int n;

	printf("Unesite pozitivan ceo broj: ");
	scanf("%d", &n);

	char space;
	char star;
	int i;
	
	space = ' ';
	star = '*';

	for(i = 0; i < n; i = i + 1) {
		int j;

		for(j = 0; j < n - i - 1; j = j + 1) {
			printf("%c", space);
		}

		for(j = 0; j < 2 * i + 1; j = j + 1) {
			printf("%c", star);
		}

		printf("\n");
	}

	return 0;
}
