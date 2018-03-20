
int *a;
int *b,*d;
int don(int a, int **b, void ****c)
{	
	int **x,*z;
	void ****y;
	**x = **b + don(a,x,y);
	don();
	**b = *z * **x;
}

void main()
{
	int *a,**b;
	void *****c;
	don(*a,b,*c);

}