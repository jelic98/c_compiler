int main() {
	int broj;
	int cj;
	int cd;
	int cs;

	printf("Unesite pozitivan ceo broj: ");
	scanf("%d", &broj);

	cj = broj % 10;
	cd = (broj / 10) % 10;
	cs = (broj / 100) % 10;

	if(broj == cj * cj * cj + cd * cd * cd + cs * cs * cs) {
		printf("Broj %d jeste Armstrongov broj\n", broj);
	} else {
		printf("Broj %d nije Armstrongov broj\n", broj);
	}

	return 0;
}
