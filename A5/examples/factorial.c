int f(int *a)
{
	int* ret;
	int* b;
	int* c;
	if(*a == 1){
		*ret = 1;
	}
	else{
		*b = *a;
		*a = *a - 1;
		*c = f(a);
		*ret = *b * *c;
	}
	return *ret;
}

void main(){
	int* a;
	*a = 5;
	*a = f(a);
}