void draw(int n, int m) {
	if(n == 0) {
		return;
	}

	int i;

	for(i = 0; i < m; i = i + 1) {
		printf("*");
	}

	printf("\n");

	draw(n - 1, m);
}

int main() {
	int a;
	int b;

	printf("Unesite dva pozitivna cela broja: ");
	scanf("%d%d", &a, &b);

	draw(a, b);

	return 0;
}
