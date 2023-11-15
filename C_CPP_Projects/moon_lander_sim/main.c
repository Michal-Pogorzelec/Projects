#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>

#define G_DEFINED 1.6f
#define MAX_FINAL_SPEED 1.0f
#define TIME_STAMP 250 /* W ms */

int check_input(double const m, double const h, double const v, double const F)
{
    if (m <= 0.0f || h <= 0 || v < 0 || F <= 0)
    {
        printf("Wrong input parameters!\n");
        return 1;
    }
    else
    {
        printf("Entry parameters: %.2lfkg, %.2lfm, %.2lfm/s^2, %lfN\n", m, h, v, F);
        return 0;
    }
}

double abs_double(double x)
{
    if (x < 0)
    {
        x = x * (-1.0f);
    }
    return x;
}

double count_a(double const m, double const F_c)
{
    double a = (m*G_DEFINED - F_c) / m;
    a = abs_double(a);

    return a;
}

double solution(double const h_0, double const v_0, double const a)
{
    return 0.5f * ((2.0f*h_0) + (v_0 * (v_0/G_DEFINED))) * (G_DEFINED / (G_DEFINED+a));
}

void delay(int numOfMilliSeconds)
{
    clock_t start_time = clock();
    while (clock() < start_time + numOfMilliSeconds)
    {}
}

void update_params(double *h, double *v, bool *engine, double const h_threshold, double const a)
{
    double time = (double)TIME_STAMP/1000.0f; // cast time type to seconds
    double g = G_DEFINED;
    double v_diff;
    if (*engine == false && *v > MAX_FINAL_SPEED)
    {
        v_diff = g*time;
        *v += v_diff;
        *h -= ((*v)*time + (g*time*time*0.5f));
        if (*h <= h_threshold)
        {
            *engine = true; /* ON */
        }
    }
    else if (*engine == false && *v < MAX_FINAL_SPEED)
    {
        v_diff = g*time;
        *v += v_diff;
        *h -= ((*v)*time + (g*time*time*0.5f));
        if (*v + v_diff >= MAX_FINAL_SPEED) // check if in the next step we would go over 1m/s
        {
            *engine = true;
        }
    }
    else
    {
        v_diff = a * time;
        *v -= v_diff;
        *h -= ((*v)*time - (a*time*time*0.5f));
        if (*v - v_diff <= 0) // check if in the next step we would get minus speed when engine is off
        {
            *engine = false;
        }
    }
    if (*h <= 0)
    {
        *h = 0;
    }
}


int main() {
    double m, h_0, v_0, F_c;
    double h1_threshold, a, current_h, current_v;
    bool engine_work = false;
    bool touched = false;
    char engine_state[] = "OFF";
    printf("Welcome in space simulation!\n");
    printf("Mass:");
    scanf("%lf", &m);
    printf("Entry height:");
    scanf("%lf", &h_0);
    printf("Entry speed:");
    scanf("%lf", &v_0);
    printf("Engine thrust:");
    scanf("%lf", &F_c);

    if (check_input(m, h_0, v_0, F_c) == 1)
    {
        return 1;
    }

    current_h = h_0;
    current_v = v_0;
    a = count_a(m, F_c);
    h1_threshold = solution(h_0, v_0, a); // h1_threshold - height we should turn on the engine
    h1_threshold += h1_threshold*0.05; // 5% safety margin
    if (h1_threshold > h_0) /* if the h1_threshold is higher than entry, turn on engine immediately */
    {
        engine_work = true;
    }
    printf("Braking we can get = %f \n", a);
    printf("Should turn on the engine on the height = %.2lf\n", h1_threshold);

    printf("Start simulation! \n");

    while (!touched)
    {
        update_params(&current_h, &current_v, &engine_work, h1_threshold, a);
        if (current_h == 0)
        {
            touched = true;
        }
        if (engine_work) strcpy(engine_state, "ON");
        else strcpy(engine_state, "OFF");
        printf("H=%.2lf, V=%.2lf ", current_h, current_v);
        for (int i=0; i<3; i++)
        {
            printf("%c", engine_state[i]);
        }
        printf("\n");
        delay(TIME_STAMP); /* If you want to reduce the TimeStamp so that the calculations are performe
 * faster, but the display remained at the same frequency, you can use counter and modulo division with printf */
    }

    if (current_v < 1)
    {
        printf("Landing successfull! \n");
    }
    else
    {
        printf("Landing went wrong. End speed: %.2lf", current_v);
    }

    return 0;
}
