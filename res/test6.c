int main() {
	int n;

	printf("Unesite pozitivan ceo broj: ");
	scanf("%d", &n);

	int fact;
	int i;
	
	fact = 1;
	
	for(i = 2; i <= n; i = i + 1) {
		fact = fact * i;
	}
	
	printf("Faktorijel broja %d je %d\n", n, fact);

	return 0;
}
