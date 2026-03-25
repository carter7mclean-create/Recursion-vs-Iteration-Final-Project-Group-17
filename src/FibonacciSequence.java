import java.math.BigInteger;

public class FibonacciSequence {

    public static BigInteger recursiveFibonacci(int num) {
        return fibHelper(num, BigInteger.ZERO, BigInteger.ONE);
    }

    public static BigInteger fibHelper(int num, BigInteger a, BigInteger b) {
        if (num == 0) return a;
        if (num == 1) return b;
        return fibHelper(num - 1, b, a.add(b));
    }

    public static BigInteger iterativeFibonacci(int num) {
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

    public static long getAvgTime(String type, int num) {
        long time = 0;

        try {
            for (int i = 0; i < 10; i++) {
                long start = System.nanoTime();

                if (type.equals("Recursive")) {
                    recursiveFibonacci(num);
                } else {
                    iterativeFibonacci(num);
                }

                long end = System.nanoTime();
                time += (end - start);
            }
        } catch (StackOverflowError e) {
            System.out.println("StackOverflowError at " + num);
            return -1;
        }

        return time / 10;
    }

    public static void main(String[] args) {
        System.out.println("Recursive fibonacci of 5000: " + getAvgTime("Recursive", 5000));
        System.out.println("Recursive fibonacci of 10000: " + getAvgTime("Recursive", 10000));
        System.out.println("Recursive fibonacci of 30000: " + getAvgTime("Recursive", 30000));
        System.out.println("Recursive fibonacci of 50000: " + getAvgTime("Recursive", 50000));
        System.out.println("Recursive fibonacci of 70000: " + getAvgTime("Recursive", 70000));
        System.out.println("Recursive fibonacci of 100000: " + getAvgTime("Recursive", 100000));

        System.out.println("Iterative fibonacci of 5000: " + getAvgTime("Iterative", 5000));
        System.out.println("Iterative fibonacci of 10000: " + getAvgTime("Iterative", 10000));
        System.out.println("Iterative fibonacci of 30000: " + getAvgTime("Iterative", 30000));
        System.out.println("Iterative fibonacci of 50000: " + getAvgTime("Iterative", 50000));
        System.out.println("Iterative fibonacci of 70000: " + getAvgTime("Iterative", 70000));
        System.out.println("Iterative fibonacci of 100000: " + getAvgTime("Iterative", 100000));
    }
}
