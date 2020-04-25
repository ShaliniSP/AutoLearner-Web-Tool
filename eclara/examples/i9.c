int main(){

	int x;
	scanf("%d", &x);

	if(x<0){
		for(int i = 0;i<10;i++)
			x++;
	}
	else{
		for(int i = 0;i<10;i++)
			x--;
	}
	return x;

}