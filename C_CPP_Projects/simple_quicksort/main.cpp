#include <iostream>

using namespace std;

int *create(int n)
{
    int *tab;
    tab = new int [n];

    for(int i = 0; i<n; i++)
    {
        tab[i] = i*i;
    }

    return tab;
}


void quicksort(int *tab, int lewy, int prawy)
{

    int v = tab[(lewy+prawy)/2];
    int i = lewy;
    int j = prawy;

    do {
        while (tab[i] < v) i++;
        while (tab[j] > v) j--;

        if (i <= j) {
            swap(tab[i], tab[j]);
            i++;
            j--;
        }
    }while(i<=j);

    if(i < prawy)
    {
        quicksort(tab, i, prawy);
    }
    if (j > lewy)
    {
        quicksort(tab, lewy, j);
    }

}


int main() {

    int x = 10;
    int *w = &x;

    int tab[] = {1, 2, 3};
    int *tab2;
    int *w2 = &tab[0];


    int tab3[] = {9, 6 ,0, 3, 1, 5, 8};
    quicksort(tab3, 0, 6);

    for (int i = 0; i < 7; i++)
    {
        cout << tab3[i] << endl;
    }



    return 0;
}
