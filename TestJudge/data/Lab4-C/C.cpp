#include <cstdio>
#include <list>
#include <cctype>

using namespace std;

list<char> line;

int main()
{
    int T;
    scanf("%d", &T);
    while (T--)
    {
        line.clear();
        auto it = line.begin();
        int n;
        scanf("%d", &n);
        bool replace = false;
        while (n--)
        {
            char ch = getchar();
            while (!isalnum(ch)) ch = getchar();
            if (isdigit(ch))
            {
                if (!replace) line.insert(it, ch);
                else 
                {
                    if (it == line.end())
                    {
                        line.insert(it, ch);
                        it--;
                    }
                    else *it = ch;
                    replace = false;
                }
            }
            else
            {
                if (ch == 'H' && it != line.begin()) it--;
                if (ch == 'L' && it != line.end()) it++;
                if (ch == 'I') it = line.begin();
                if (ch == 'r') replace = true;
                if (ch == 'x' && it != line.end())
                {
                    auto del = it;
                    it++;
                    line.erase(del);
                }
            }
        }
        for (it = line.begin(); it != line.end(); it++)
        {
            putchar(*it);
        }
        putchar('\n');
    }
    return 0;
}
