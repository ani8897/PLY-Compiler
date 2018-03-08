void main(){

	int *a,*b,*c,e,f;

	if(*a > 5){
		a = &e;
		if(*b < 6){
			b = &e;
			if(*c >8){
				c = &e;
			}
		}
		else{
			b = &f;
		}
	}
	else{
		a = &f;
	}
}
