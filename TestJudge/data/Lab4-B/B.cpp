#include <cstdio>
#include <cstring>
#include <algorithm>

using namespace std;

const int MAXN = 100010;

struct node
{
    int prv, nxt;
} team[MAXN];

inline void print(int head, int N)
{
    int tn = N;
    for (int nod = head; nod != N; nod = team[nod].nxt)
    {
        printf("%d ", nod);
    }
    putchar('\n');
}

int main()
{
    int T;
    scanf("%d", &T);
    while (T--)
    {
        int N, M;
        scanf("%d%d", &N, &M);
        int head = 0;
        int prev = N;
        int id;
        for (int i = 0; i < N; i++)
        {
            scanf("%d", &id);
            if (i == 0) head = id;
            team[id].prv = prev;
            team[prev].nxt = id;
            prev = id;
        }
        team[id].nxt = N;
        for (int i = 0; i < M; i++)
        {
            int x1, y1, x2, y2;
            scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
            if (head == x1) head = x2;
            else if (head == x2) head = x1;
            if (team[y1].nxt == x2)
            {
                team[team[x1].prv].nxt = x2;
                team[team[y2].nxt].prv = y1;
                team[y1].nxt = team[y2].nxt;
                team[x2].prv = team[x1].prv;
                team[x1].prv = y2;
                team[y2].nxt = x1;
            }
            else
            {
                team[team[x1].prv].nxt = x2;
                team[team[y2].nxt].prv = y1;
                team[team[x2].prv].nxt = x1;
                team[team[y1].nxt].prv = y2;
                swap(team[x1].prv, team[x2].prv);
                swap(team[y1].nxt, team[y2].nxt);
            }
        }
        print(head, N);
    }
    return 0;
}
