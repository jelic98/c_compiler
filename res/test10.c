int main() {
	char asd[50] = {'q', 'w', 'e', 'r', 't', 'y'};
	char efg[50];
	
	printf("Unesite string: ");
	scanf("%s", efg);
	
	printf("Konkatenacija stringova: %s + %s\n", asd, efg);
	
	strcat(asd, efg);
	
	int length;
	length = strlen(asd);
	
	printf("Rezultat konkatenacije: %s\n", asd);
	printf("Duzina konkatenacije: %d\n", length);
	
	return 0;
}
