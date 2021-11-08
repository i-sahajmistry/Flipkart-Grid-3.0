#include<bits/stdc++.h>
#define N 9
using namespace std;

vector<vector<int>> graph(N, vector<int>(N));
vector<bool> b(N, true);

void utilCluster(int a)
{
    queue<int> q;
    q.push(a);
    while(!q.empty())
    {
        a = q.front();
        cout << a;
        q.pop();
        if(b[a])
        {
            b[a] = false;
            for(int i = 0; i < graph[a].size(); i++)
            {
                // cout << graph[a][i] /*<< b[i] << i */;
                if(graph[a][i] and b[i])
                {
                    q.push(a);
                }
                // cout << q.size() << ' ';
            }
            // cout << endl;
        }
    }
}

int cluster()
{
    int clusters = 0;
    for(int i = 0; i < b.size(); i++)
    {
        if(b[i])
        {
            // for(bool l : b)
            //     cout << l << "   ";
            // cout << endl;
            clusters++;
            utilCluster(i);
        }
    }
    return clusters;
}

void addNode(int i, int j)
{
    graph[i][j] = 1;
    graph[j][i] = 1;
}

int main()
{
    addNode(1, 2);
    addNode(1, 4);
    addNode(2, 4);
    addNode(3, 4);

    addNode(5, 6);
    addNode(5, 7);
    addNode(6, 7);
    addNode(6, 8);
    cout << cluster();
    return 0;
}