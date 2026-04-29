import java.math.BigInteger;
import java.util.Scanner;

public class FastExponentiation {
	private static volatile BigInteger lastResult = BigInteger.ONE;

	public static void main(String[] args) 
	{
		Scanner scan = new Scanner(System.in);
		BigInteger x = BigInteger.valueOf(2);
		System.out.println("The base vaue is: " + x);

		System.out.print("Enter the number of test runs: ");
		long numRuns = scan.nextLong();
		scan.close();
		
		System.out.println("Recursive fast exponentiaion of 5000: " + getAvgTime("Recursive", 5000, numRuns));
        System.out.println("Recursive fast exponentiaion of 10000: " + getAvgTime("Recursive", 10000, numRuns));
        System.out.println("Recursive fast exponentiaion of 30000: " + getAvgTime("Recursive", 30000, numRuns));
        System.out.println("Recursive fast exponentiaion of 50000: " + getAvgTime("Recursive", 50000, numRuns));
        System.out.println("Recursive fast exponentiaion of 70000: " + getAvgTime("Recursive", 70000, numRuns));
        System.out.println("Recursive fast exponentiaion of 100000: " + getAvgTime("Recursive", 100000, numRuns));
        System.out.println();
        System.out.println("Iterative fast exponentiaion of 5000: " + getAvgTime("Iterative", 5000, numRuns));
        System.out.println("Iterative fast exponentiaion of 10000: " + getAvgTime("Iterative", 10000, numRuns));
        System.out.println("Iterative fast exponentiaion of 30000: " + getAvgTime("Iterative", 30000, numRuns));
        System.out.println("Iterative fast exponentiaion of 50000: " + getAvgTime("Iterative", 50000, numRuns));
        System.out.println("Iterative fast exponentiaion of 70000: " + getAvgTime("Iterative", 70000, numRuns));
	        System.out.println("Iterative fast exponentiaion of 100000: " + getAvgTime("Iterative", 100000, numRuns));
		}
	
	public static BigInteger recursiveExponentiation(BigInteger x, long n) //a ^ n
	{
		if (n < 0) {
			throw new IllegalArgumentException("Exponent must be non-negative.");
		}
		if (n == 0)
		{
			return BigInteger.ONE;
		}
		
		BigInteger half = recursiveExponentiation(x, n / 2);
		BigInteger squared = half.multiply(half);
		if (n % 2 == 0)
		{
			return squared;
		}
		return squared.multiply(x);
	}
	
	public static BigInteger iterativeExponentiation(BigInteger x, long n)
	{
		if (n < 0) {
			throw new IllegalArgumentException("Exponent must be non-negative.");
		}
		BigInteger result = BigInteger.ONE;
		while (n > 0)
		{
			if (n % 2 != 0)
			{
				result = result.multiply(x);
			}
			x = x.multiply(x);
			n /= 2;
		}
		return result;
	}
	public static long getAvgTime(String type, int n, long numRuns) {
        long time = 0;

	        try {
	            for (int i = 0; i < numRuns; i++) 
	            {
	                long start = System.nanoTime();

	                if ("Recursive".equals(type)) 
	                {
	                    lastResult = recursiveExponentiation(BigInteger.valueOf(2), n);
	                } 
	                else 
	                {
	                    lastResult = iterativeExponentiation(BigInteger.valueOf(2), n);
	                }

                long end = System.nanoTime();
                time += (end - start);
            }
        } catch (StackOverflowError e) {
            System.out.println("StackOverflowError at " + n);
            return -1;
        }

        return time / numRuns;
    }
	
}
