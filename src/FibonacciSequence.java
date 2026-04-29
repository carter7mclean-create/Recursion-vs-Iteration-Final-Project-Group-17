import java.math.BigInteger;
import java.util.Scanner;

public class FibonacciSequence {
    private static volatile BigInteger lastResult = BigInteger.ZERO;

    public static BigInteger recursiveFibonacci(int num) {
        if (num < 0) {
            throw new IllegalArgumentException("Fibonacci is undefined for negative input.");
        }
        return fibHelper(num, BigInteger.ZERO, BigInteger.ONE);
    }

    public static BigInteger fibHelper(int num, BigInteger a, BigInteger b) {
        if (num == 0) return a;
        if (num == 1) return b;
        return fibHelper(num - 1, b, a.add(b));
    }

    public static BigInteger iterativeFibonacci(int num) {
        if (num < 0) {
            throw new IllegalArgumentException("Fibonacci is undefined for negative input.");
        }
        if (num == 0) return BigInteger.ZERO;
        if (num == 1) return BigInteger.ONE;

        BigInteger a = BigInteger.ZERO;
        BigInteger b = BigInteger.ONE;

        for (int i = 2; i <= num; i++) {
            BigInteger temp = a.add(b);
            a = b;
            b = temp;
        }
        return b;
    }

    public static long getAvgTime(String type, int num, long numRuns) {
        long time = 0;

        try {
            for (int i = 0; i < numRuns; i++) {
                long start = System.nanoTime();

                if ("Recursive".equals(type)) {
                    lastResult = recursiveFibonacci(num);
                } else {
                    lastResult = iterativeFibonacci(num);
                }

                long end = System.nanoTime();
                time += (end - start);
            }
        } catch (StackOverflowError e) {
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
        System.out.println("Recursive fibonacci of 5000: " + getAvgTime("Recursive", 5000, numRuns));
        System.out.println("Recursive fibonacci of 10000: " + getAvgTime("Recursive", 10000, numRuns));
        System.out.println("Recursive fibonacci of 30000: " + getAvgTime("Recursive", 30000, numRuns));
        System.out.println("Recursive fibonacci of 50000: " + getAvgTime("Recursive", 50000, numRuns));
        System.out.println("Recursive fibonacci of 70000: " + getAvgTime("Recursive", 70000, numRuns));
        System.out.println("Recursive fibonacci of 100000: " + getAvgTime("Recursive", 100000, numRuns));

        System.out.println("Iterative fibonacci of 5000: " + getAvgTime("Iterative", 5000, numRuns));
        System.out.println("Iterative fibonacci of 10000: " + getAvgTime("Iterative", 10000, numRuns));
        System.out.println("Iterative fibonacci of 30000: " + getAvgTime("Iterative", 30000, numRuns));
        System.out.println("Iterative fibonacci of 50000: " + getAvgTime("Iterative", 50000, numRuns));
        System.out.println("Iterative fibonacci of 70000: " + getAvgTime("Iterative", 70000, numRuns));
        System.out.println("Iterative fibonacci of 100000: " + getAvgTime("Iterative", 100000, numRuns));
    }
}

