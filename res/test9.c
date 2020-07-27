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

	a = 3;
	b = 5;

	draw(a, b);

	return 0;
}
