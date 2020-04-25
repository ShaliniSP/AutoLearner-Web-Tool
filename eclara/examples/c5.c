int main(){
	int x;
	scanf("%d", &x);
	
	for(int i = 0;i<10;i++){
		for(int j = 0;j<10;j++){
			x+=(i+j);
			for(int k = 0;k<10;k++)
				x++;
		}
		
			for(int k = 0;k<10;k++)
				x++;
	}
	for(int k = 0;k<10;k++)
		for(int j = 0;j<1;j++)
			x++;
	return x;
}
