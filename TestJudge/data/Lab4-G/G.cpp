#include <cstdio>
#include <algorithm>
#include <cassert>

using namespace std;

const int MAXK = 5100;

const long long MOD = 1000000;

const long long INV3 = 666667;

long long fib[MAXK*2];

struct node
{
    long long first, len;
    bool inv;

    int prev, next;

    node(long long first = -1, long long len = 0,
         bool inv = false, int prev = -1, int next = -1):
        first(first), len(len), inv(inv), 
        prev(prev), next(next) {}
} list[MAXK*2];

inline void print_node(int ind)
{
    printf("[%d]: {first=%lld, len=%lld, inv=%d, prev=%d, next=%d}\n", ind, 
            list[ind].first, list[ind].len, list[ind].inv, list[ind].prev, list[ind].next);
}

int size;
int head;

inline int find(long long & cnt, int ind, long long val)
{
    while (ind != 0 && cnt+list[ind].len <= val)
    {
        cnt += list[ind].len;
        ind = list[ind].next;
    }
    /*
    putchar('#');
    print_node(ind);
    */
    if (val > cnt)
    {
        size++;
        long long nlen = cnt + list[ind].len - val;
        if (list[ind].inv)
        {
            list[size] = node(list[ind].first, nlen, true, ind, list[ind].next);
            list[ind].first = list[ind].first + nlen;
        }
        else
        {
            list[size] = node(list[ind].first+val-cnt, nlen, false, ind, list[ind].next);
        }
        list[list[ind].next].prev = size;
        list[ind].next = size;
        list[ind].len = val - cnt;

        /*
        putchar('$');
        print_node(ind);
        putchar('$');
        print_node(size);
        */

        cnt += list[ind].len;
        ind = list[ind].next;
    }
    return ind;
}

inline void print_list()
{
    for (int ind = head; ind != 0; ind = list[ind].next)
    {
        print_node(ind);
    }
    putchar('\n');
}

int main()
{
    long long N;
    int K;
    scanf("%lld%d", &N, &K);
    fib[0] = fib[1] = 1 % N;
    for (int i = 2; i < K*2; i++)
    {
        fib[i] = (fib[i-1] + fib[i-2]) % N;
    }

    list[0] = node(N, 0, false, 1, 1);
    list[1] = node(0, N, false, 0, 0);
    size = 1;
    head = 1;

    // print_list();

    for (int i = 0; i < K; i++)
    {
        // printf("@%d:\n", i+1);
        if (fib[2*i] > fib[2*i+1]) swap(fib[2*i], fib[2*i+1]);
        fib[2*i+1]++;
        long long cnt = 0;
        int start = find(cnt, head, fib[2*i]);
        int end = find(cnt, start, fib[2*i+1]);

        int prev_start = list[start].prev;
        int prev_end = list[end].prev;
        if (head == start)
        {
            head = prev_end;
        }
        for (int cur = start; cur != end; cur = list[cur].prev)
        {
            swap(list[cur].prev, list[cur].next);
            list[cur].inv = !list[cur].inv;
        }
        swap(list[prev_start].next, list[end].prev);
        swap(list[start].next, list[prev_end].prev);

        // print_list();
    }

    long long ans = 0;
    long long a = 0;
    for (int ind = head; ind != 0; ind = list[ind].next)
    {
        long long k = list[ind].len;
        long long pk;
        if (k & 1)
        {
            pk = (k-1) / 2 % MOD * k % MOD;
        }
        else
        {
            pk = k / 2 % MOD * (k-1) % MOD;
        }
        k %= MOD;
        a %= MOD;
        if (list[ind].inv)
        {
            long long b = (list[ind].first+list[ind].len-1) % MOD;
            long long tans = (k*a*b%MOD + pk*(b-a)%MOD - pk*(k+k-1)%MOD*INV3%MOD) % MOD;
            ans = (ans + tans) % MOD;
        }
        else
        {
            long long b = list[ind].first % MOD;
            long long tans = (k*a*b%MOD + pk*(b+a)%MOD + pk*(k+k-1)%MOD*INV3%MOD) % MOD;
            ans = (ans + tans) % MOD;
        }
        ans = (ans + MOD) % MOD;
        a += list[ind].len;
    }
    printf("%lld\n", ans);

    return 0;
}
