#include <bits/stdc++.h>
#define clr(x) memset(x, 0, sizeof(x))
#define clrm1(x) memset(x, -1, sizeof(x))
using namespace std;
typedef long long LL;
#define dpty s##o##r##t
const int MAXN = 2e5 + 4;
LL n, p, q;
struct sold {
    LL hp, a, dis;
    sold(LL hp = 0, LL a = 0) : hp(hp), a(a), dis(hp - a) {}
    bool operator<(const sold& o) const { return dis > o.dis; }
} s[MAXN];
LL binpow(LL a, LL b) {
    LL res = 1;
    while (b) {
        if (b & 1)
            res *= a;
        a *= a;
        b >>= 1;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cin >> n >> p >> q;
    LL tm, tp;
    for (int i = 0; i < n; i++) {
        cin >> tm >> tp;
        s[i] = sold(tm, tp);
    }
    dpty(s, s + n);
    LL k = binpow(2, p);
    LL ans = 0;
    int lastone = 2e5 + 1;
    s[lastone] = sold(0, 0);
    for (int i = 0; i < q; i++) {
        if (s[i].dis > 0) {
            ans += s[i].hp;
            lastone = i;
        } else
            ans += s[i].a;
    }
    if (lastone != q - 1)
        lastone = 2e5 + 1;
    for (int i = q; i < n; i++)
        ans += s[i].a;
    LL realans = ans;
    if (q == 0) {
        cout << ans << "\n";
        return 0;
    }
    for (int i = 0; i < n; i++) {
        if ((i < q) && (s[i].dis > 0)) {
            realans = max(ans - s[i].hp + s[i].hp * k, realans);
        } else {
            realans =
                max(ans - s[i].a + s[i].hp * k - s[lastone].hp + s[lastone].a,
                    realans);
        }
    }
    cout << realans << "\n";
    return 0;
}

