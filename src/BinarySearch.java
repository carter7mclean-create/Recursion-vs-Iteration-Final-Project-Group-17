package classCode;
import java.util.*;

public class binarySearch2 {
	private static volatile int lastResult = -1;
	
	public static void main(String[] args) {
		//5k size array
		int[] l1 = new int[5000];
		for(int i = 0; i < 5000; i++) {
			l1[i] = i;
		}
		
		//10k size array
		int[] l2 = new int[10000];
		for(int i = 0; i < 10000; i++) {
			l2[i] = i;
		}
		//30k size array
		int[] l3 = new int[30000];
		for(int i = 0; i < 30000; i++) {
			l3[i] = i;
		}
		
		//50k size array
		int[] l4 = new int[50000];
		for(int i = 0; i < 50000; i++) {
			l4[i] = i;
		}
		//70k size array
		int[] l5 = new int[70000];
		for(int i = 0; i < 70000; i++) {
			l5[i] = i;
		}
		
		//100k size array
		int[] l6 = new int[100000];
		for(int i = 0; i < 100000; i++) {
			l6[i] = i;
		}
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter the number to search: ");
		long numToSearch = scan.nextLong();
		System.out.print("Enter the number of searches: ");
		long numRuns = scan.nextLong();
		
		scan.close();
		
		getAvgTime("Recursive,", l1, 1, 1);		
		
		System.out.println("Recursive binary search of 5000: " + getAvgTime("Recursive", l1, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Recursive binary search of 10000: " + getAvgTime("Recursive", l2, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Recursive binary search of 30000: " + getAvgTime("Recursive", l3, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Recursive binary search of 50000: " + getAvgTime("Recursive", l4, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Recursive binary search of 70000: " + getAvgTime("Recursive", l5, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Recursive binary search of 100000: " + getAvgTime("Recursive", l6, numToSearch, numRuns) + " nanoseconds.");

        System.out.println();
        
        System.out.println("Iterative binary search of 5000: " + getAvgTime("Iterative", l1, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Iterative binary search of 10000: " + getAvgTime("Iterative", l2, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Iterative binary search of 30000: " + getAvgTime("Iterative", l3, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Iterative binary search of 50000: " + getAvgTime("Iterative", l4, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Iterative binary search of 70000: " + getAvgTime("Iterative", l5, numToSearch, numRuns) + " nanoseconds.");
        System.out.println("Iterative binary search of 100000: " + getAvgTime("Iterative", l6, numToSearch, numRuns) + " nanoseconds.");
	}
	
	static int RecursiveSearch(int[] list, int left, int right, long a) {
		if (left > right) {
			return -1;
		}
		
		int mid = left + (right - left) / 2;
		if (list[mid] == a) {
			return mid;
		}
		else if (a > list[mid]) {
			return RecursiveSearch(list, mid + 1, right, a);
		}
		else {
			return RecursiveSearch(list, left, mid - 1, a);
		}
	}
	
	static int IterativeSearch(int[] list, int left, int right, long num) {
		
		while (left <= right) {
			int mid = left + (right - left) / 2;
			
			if (list[mid] == num) {
				return mid;
			}
			
			else if (num < list[mid]) {
				right = mid - 1;
			}
			else {
				left = mid + 1;
			}
		}
		return -1;
	}
	public static long getAvgTime(String type, int[] list, long num, long numRuns) {
        long time = 0;

        try {
            for (int i = 0; i < numRuns; i++) {
                long start = System.nanoTime();

                if ("Recursive".equals(type)) {
                    lastResult = RecursiveSearch(list, 0, list.length - 1, num);
                } else {
                    lastResult = IterativeSearch(list, 0, list.length - 1, num);
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
	
	
	
	
}
