#include <cstdio>
#include <unordered_map>
#include <utility>

using namespace std;

unordered_map<int, int> poly;

int main()
{
    int T;
    scanf("%d", &T);
    while (T--)
    {
        poly.clear();
        int n;
        scanf("%d", &n);
        for (int i = 0; i < n; i++)
        {
            int coef, expo;
            scanf("%d%d", &coef, &expo);
            poly[expo] += coef;
        }
        int m;
        scanf("%d", &m);
        for (int i = 0; i < m; i++)
        {
            int coef, expo;
            scanf("%d%d", &coef, &expo);
            poly[expo] += coef;
        }
        int q;
        scanf("%d", &q);
        for (int i = 0; i < q; i++)
        {
            int expo;
            scanf("%d", &expo);
            printf("%d ", poly[expo]);
        }
        putchar('\n');
    }
    return 0;
}
