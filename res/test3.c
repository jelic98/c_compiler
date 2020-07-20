int main() {
	int arr1[3];
	int arr2[] = {1, 23, 456};
	int i;

	for(i = 0; i < 3; i = i + 1) {
		arr1[i] = arr2[i];
		printf("%d\n", arr1[i]);
	}

	return 0;
}
