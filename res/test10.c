int main() {
	char asd[50] = {'q', 'w', 'e', 'r', 't', 'y'};
	char efg[50];
	scanf("%s", efg);
	strcat(asd, efg);
	int length;
	length = strlen(asd);
	printf("String of length %d is %s\n", length, asd);
	return 0;
}
