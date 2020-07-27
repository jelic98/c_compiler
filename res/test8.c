int main() {
	int n;

	printf("Unesite pozitivan ceo broj: ");
	scanf("%d", &n);

	int niz[100];
	int i;

	for(i = 0; i < n; i = i + 1) {
		printf("Unesite ceo broj za %d. element niza: ", i + 1);
		scanf("%d", &niz[i]);
	}

	for(i = 0; i < n; i = i + 1) {
		int j;

		for(j = i; j < n; j = j + 1) {
			if(niz[i] > niz[j]) {
				int temp;
				temp = niz[i];
				niz[i] = niz[j];
				niz[j] = temp;
			}
		}
	}
	
	printf("Sortirani niz: ");

	for(i = 0; i < n; i = i + 1) {
		printf("%d", niz[i]);

		if(i == n - 1) {
			printf("\n");
		} else {
			printf(" ");
		}
	}

	return 0;
}
