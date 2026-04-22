import java.util.Scanner;

public class FastExponentiation {

	public static void main(String[] args) 
	{
		Scanner scan = new Scanner(System.in);
		long x = 2;
		System.out.println("The base vaue is: " + x);
//		System.out.print("Enter the value of the exponent: ");
//		long n = scan.nextLong();
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
	public static long getAvgTime(String type, int n, long numRuns) {
        long time = 0;

        try {
            for (int i = 0; i < numRuns; i++) 
            {
                long start = System.nanoTime();

                if (type.equals("Recursive")) 
                {
                    recursiveExponentiation(2, n);
                } 
                else 
                {
                    iterativeExponentiation(2, n);
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
