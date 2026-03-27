import java.util.Scanner;

public class FastExponentiation {

	public static void main(String[] args) 
	{
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter a base value: ");
		int x = scan.nextInt();
		System.out.print("Enter the value of the exponenet: ");
		int n = scan.nextInt();
		
		try
		{
			averageRecursion(x, n, 10);
		}
		catch (StackOverflowError e)
		{
			System.out.println("Recursion StackOverflowError");
		}
		
		try
		{
			averageIterative(x, n, 10);
		}
		catch (StackOverflowError e)
		{
			System.out.println("Iterative StackOverflowError");
		}
	}
	
	public static int recursiveExponentiation(int x, int n) //a ^ n
	{
		if (n == 0)
			return 1;
		return recursiveExponentiation(x, n-1) * x;
	}
	
	public static int iterativeExponentiation(int x, int n)
	{
		int num = x;
		for(int i = 1; i < n; i++)
		{
			num *= x;
		}
		return num;
	}
	
	public static void averageRecursion(int x, int n, int numRuns)
	{
		long totalTime = 0;
		for(int i = 1; i <= numRuns; i++)
		{
			long start = System.nanoTime();
			recursiveExponentiation(x, n);
			long runTime = System.nanoTime() - start;
			System.out.println("Recursion run #" + i + ": " + runTime);
			totalTime += runTime;
		}
		System.out.println();
		System.out.println("Recursion average runtime: " + totalTime/numRuns);
	}
	public static void averageIterative(int x, int n, int numRuns)
	{
		long totalTime = 0;
		for(int i = 1; i <= numRuns; i++)
		{
			long start = System.nanoTime();
			recursiveExponentiation(x, n);
			long runTime = System.nanoTime() - start;
			System.out.println("Iterative run #" + i + ": " + runTime);
			totalTime += runTime;
		}
		System.out.println("Iterative average runtime: " + totalTime/numRuns);
	}
}
