#include<bits/stdc++.h>
using namespace std;

bool utilCluster(int a, vector<bool>& b)
{
    queue<int> q;
    q.push(a);
    while(!q.empty())
    {
        a = q.front();
        q.pop();
        if(b[a])
        {
            b[a] = false;
            for(int i = 0; i < graph[a].size(); i++)
            {
                if(b[a])
                {
                    q.push(a);
                }
            }
        }
    }
}

int cluster()
{
    int clusters = 0;
    vector<bool> b(N, true);
    for(int i = 0; i < b.size(); i++)
    {
        if(b[i])
        {
            clusters++;
            utilCluster(i, b);
        }
    }
    return clusters;
}

int main()
{
    map<int, vector<int>> graph;

    graph[1].push_back(2);
    graph[2].push_back(3);
    graph[2].push_back(1);
    graph[3].push_back(2);
    graph[3].push_back(5);
    graph[3].push_back(4);
    graph[4].push_back(3);
    graph[5].push_back(3);

    for(auto i : graph)
    {
        cout << i.first << " :";
        for(int j : i.second)
        {
            cout << j << " -> "; 
        }
        cout << endl;
    }
    return 0;
}