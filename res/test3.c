int x;

void fun(int a, int b) {
	printf("%d %d\n", a, b);
}

int fun2(int x, int y) {
	return x + y;
}

int fun3(int p, int q, int r) {
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
		arr1[i] = fun2(arr1[i], arr2[i]);
		fun(arr1[i], arr2[i]);
	}

	return 0;
}
