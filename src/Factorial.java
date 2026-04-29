import java.math.BigInteger;
import java.util.Scanner;

public class Factorial {
	private static volatile BigInteger lastResult = BigInteger.ONE;

	public static BigInteger recursiveFactorial(int num) {
		if (num < 0) {
			throw new IllegalArgumentException("Factorial is undefined for negative input.");
		}
		if (num == 0 || num == 1)
			return BigInteger.ONE;
		else
			return BigInteger.valueOf(num).multiply(recursiveFactorial(num - 1));
	}
	
	public static BigInteger iterativeFactorial(int num) {
		if (num < 0) {
			throw new IllegalArgumentException("Factorial is undefined for negative input.");
		}
		BigInteger count = BigInteger.ONE;
		for (int i = 2; i <= num; i++) {
			count = count.multiply(BigInteger.valueOf(i));
		}
		return count;
	}
	
	public static long getAvgTime(String type, int num, long numRuns) {
		long time = 0;
		try {
			for(int i = 0; i < numRuns; i++) {
				long start = System.nanoTime();
				if ("Recursive".equals(type)) {
					lastResult = recursiveFactorial(num);
				} else {
					lastResult = iterativeFactorial(num);
				}
				long end = System.nanoTime();
				time += (end - start);
			}
		} catch(StackOverflowError e) {
			System.out.println("StackOverflowError at " + num);
			return -1;
		}
		return time / numRuns;
	}
	
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter the number of test runs: ");
		long numRuns = scan.nextLong();
		scan.close();
		System.out.println("Recursive factorial of 5000: " + getAvgTime("Recursive", 5000, numRuns));
		System.out.println("Recursive factorial of 10000: " + getAvgTime("Recursive", 10000, numRuns));
		System.out.println("Recursive factorial of 30000: " + getAvgTime("Recursive", 30000, numRuns));
		System.out.println("Recursive factorial of 50000: " + getAvgTime("Recursive", 50000, numRuns));
		System.out.println("Recursive factorial of 70000: " + getAvgTime("Recursive", 70000, numRuns));
		System.out.println("Recursive factorial of 100000: " + getAvgTime("Recursive", 100000, numRuns));
		

		System.out.println("Iterative factorial of 5000: " + getAvgTime("Iterative", 5000, numRuns));
		System.out.println("Iterative factorial of 10000: " + getAvgTime("Iterative", 10000, numRuns));
		System.out.println("Iterative factorial of 30000: " + getAvgTime("Iterative", 30000, numRuns));
		System.out.println("Iterative factorial of 50000: " + getAvgTime("Iterative", 50000, numRuns));
		System.out.println("Iterative factorial of 70000: " + getAvgTime("Iterative", 70000, numRuns));
		System.out.println("Iterative factorial of 100000: " + getAvgTime("Iterative", 100000, numRuns));
	}

}
