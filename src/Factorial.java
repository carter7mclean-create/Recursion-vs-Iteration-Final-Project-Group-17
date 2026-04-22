import java.util.Scanner;

public class Factorial {

	public static long recursiveFactorial(int num) {
		if(num == 0)
			return 1;
		else
			return num * recursiveFactorial(num-1);
	}
	
	public static long iterativeFactorial(int num) {
		int count = num;
		for(int i = 1; i < num; i++) {
			count *= i;
		}
		return count;
	}
	
	public static long getAvgTime(String type, int num, long numRuns) {
		long time = 0;
		try {
			for(int i = 0; i < numRuns; i++) {
				if(type.equals("Recursive")) {
					long start = System.nanoTime();
					recursiveFactorial(num);
					long end = System.nanoTime() - start;
					time += end;
				} else {
					long start = System.nanoTime();
					iterativeFactorial(num);
					long end = System.nanoTime() - start;
					time += end;
				}
			}
		} catch(StackOverflowError e) {
			System.out.println("StackOverflowError at " + num);;
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