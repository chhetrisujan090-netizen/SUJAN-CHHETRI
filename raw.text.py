
# q3_turtle_pattern.py
import turtle

def draw_koch_edge(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        draw_koch_edge(t, length, depth-1)
        t.left(60)
        draw_koch_edge(t, length, depth-1)
        t.right(120)
        draw_koch_edge(t, length, depth-1)
        t.left(60)
        draw_koch_edge(t, length, depth-1)

def draw_polygon(t, sides, length, depth):
    for _ in range(sides):
        draw_koch_edge(t, length, depth)
        t.right(360 / sides)

if __name__ == "__main__":
    sides = int(input("Enter number of sides: "))
    length = int(input("Enter side length (pixels): "))
    depth = int(input("Enter recursion depth: "))

    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    t = turtle.Turtle()
    t.speed("fastest")
    draw_polygon(t, sides, length, depth)
    turtle.done()
