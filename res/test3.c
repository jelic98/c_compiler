int x;

int fun(int a, int b) {
	printf("%d %d\n", a, b);
}

int arr1[3];
int arr2[] = {1, 23, 456};
int i;

int main() {
	for(i = 0; i < 3; i = i + 1) {
		arr1[i] = arr2[i];
		fun(arr1[i], arr2[i]);
	}

	return 0;
}
