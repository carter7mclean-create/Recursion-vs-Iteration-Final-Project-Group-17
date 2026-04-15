package classCode;
import java.util.*;

public class BinarySearch {
	
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
		
		int[] l3 = new int[30000];
		for(int i = 0; i < 30000; i++) {
			l3[i] = i;
		}

		int[] l4 = new int[50000];
		for(int i = 0; i < 50000; i++) {
			l4[i] = i;
		}

		int[] l5 = new int[70000];
		for(int i = 0; i < 70000; i++) {
			l5[i] = i;
		}
		
		int[] l6 = new int[100000];
		for(int i = 0; i < 100000; i++) {
			l6[i] = i;
		}
		
		int num = 100;
		int n = l1.length;
		int indexOfNum = RecursiveSearch(l1, 0, n-1, num);
		System.out.println("Number to be found: " + num);
		System.out.println("Number is found at index " + indexOfNum);
		
	}
	
	static int RecursiveSearch(int[] list, int left, int right, int a) {
		if(right >= 1) {
			int mid = (left + right)/2;
			if(list[mid] == a) {
				return mid;
			}
			else if(a > mid) {
				left = mid + 1;
				return RecursiveSearch(list, left, right, a);
			}
			else if(a < mid) {
				right = mid - 1;
				return RecursiveSearch(list, left, right, a);
			}
		}
		return -1;
	}
	
	static int IterativeSearch(int[] list, int left, int right, int num) {
		
		while(left <= right) {
			int mid = (left + right)/2;
			
			if(list[mid] == num) {
				return mid;
			}
			
			else if(num < mid) {
				right = mid - 1;
			}
			else if(num > mid) {
				left = mid + 1;
			}
		}
		return -1;
	}
	
	
	
}
