import java.util.Scanner;

public class FastExponentiation {

	public static void main(String[] args) 
	{
		Scanner scan = new Scanner(System.in);
		long x = 2;
		System.out.println("The base vaue is: " + x);
		System.out.print("Enter the value of the exponenet: ");
		long n = scan.nextLong();
		System.out.println("Enter the number of test runs: ");
		long numRuns = scan.nextLong();
		scan.close();
		
		long recursion = 0;
		long iterative = 0;
		try
		{
			recursion = averageRecursion(x, n, numRuns);
		}
		catch (StackOverflowError e)
		{
			System.out.println("Recursion StackOverflowError");
		}
		
		try
		{
			iterative = averageIterative(x, n, numRuns);
		}
		catch (StackOverflowError e)
		{
			System.out.println("Iterative StackOverflowError");
		}
		System.out.println("\n\n");
		System.out.println("Recursive average runtime: " + recursion);
		System.out.println("Iterative average runtime: " + iterative);

	}
	
	public static long recursiveExponentiation(long x, long n) //a ^ n
	{
		if (n == 0)
		{
			return 1;
		}
		if (n % 2 == 0)
		{
			long half = recursiveExponentiation(x, n/2);
			return half * half;
		}
		else
		{
			return x * recursiveExponentiation(x, n-1);
		}
	}
	
	public static long iterativeExponentiation(long x, long n)
	{
		long result = 1;
		while (n > 0)
		{
			if (n % 2 != 0)
			{
				result *= x;
			}
			x *= x;
			n /= 2;
		}
		return result;
	}
	
	public static long averageRecursion(long x, long n, long numRuns)
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
		System.out.println();
		return (totalTime/numRuns);
	}
	public static long averageIterative(long x, long n, long numRuns)
	{
		long totalTime = 0;
		for(int i = 1; i <= numRuns; i++)
		{
			long start = System.nanoTime();
			iterativeExponentiation(x, n);
			long runTime = System.nanoTime() - start;
			System.out.println("Iterative run #" + i + ": " + runTime);
			totalTime += runTime;
		}
		System.out.println("Iterative average runtime: " + totalTime/numRuns);
		return (totalTime/numRuns);
	}
}
