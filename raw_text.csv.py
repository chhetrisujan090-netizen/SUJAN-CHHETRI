import turtle

def koch(t, l, d):
    if d==0: t.forward(l)
    else:
        l/=3
        for a in [0,60,-120,60]:
            koch(t,l,d-1); t.left(a)

sides=int(input("Sides: "))
length=int(input("Length: "))
depth=int(input("Depth: "))

t=turtle.Turtle()
for _ in range(sides):
    koch(t,length,depth)
    t.right(360/sides)

turtle.done() 
