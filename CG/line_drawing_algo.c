#include<graphics.h>
#include<math.h>
#include<stdio.h>
#include<conio.h>
#include<dos.h>
#define round(x)((int)(x+0.5))

int color=MAGENTA;

//DDA function for line generation

void DDA(int xa, int ya, int xb, int yb)
{
    //Calculate dx and dy
    int dx= xb - xa;
    int dy= yb - ya;

    int steps= abs(dx)>abs(dy)? abs(dx): abs(dy);

    float xinc =dx/steps;
    float yinc =dy/steps;

    float x =xa;
    float y=ya;

    for(int i=0; i <=steps; i++){
        putpixel(round(x),round(y),color);
        x+=xinc;
        y+=yinc;
        delay(100);
    }
}
int main():
{
    int gd=DETECT, gm;
    initgraph(&gd, &gm, "C:\Turbo.C.3.2\WinRoot\TURBOC3\BGI");

    outtextxy(100,100, "This is DDA-Digital Differential Analyer");

    DDA(2,200,80,100);
    color=BLUE;
    DDA(80,100,80,200);
    color=WHITE;
    DDA(80,200,2,200):
    getch();
    close_graphs();
    return 0;


}