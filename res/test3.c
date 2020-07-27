int x;

void fun(int a, int b) {
	printf("%d %d\n", a, b);
}

void fun2(int p, int q, int r) {
	return q + r;
}

int main() {
	int arr1[3];
	int arr2[] = { 1, 23, 456 };
	int arr3[3];
	int i;
	int y;

	y = 5;

	for(i = 0; i < 3; i = i + 1) {
		arr1[i] = arr2[i];
		fun(arr1[i], arr2[i]);
	}

	return 0;
}
