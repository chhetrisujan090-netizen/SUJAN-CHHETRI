import turtle
def(t,length,depth)
if depth==0
t.forward(length)
return
length/=3
draw_pattern(t,length,depth -1)
t.left(60)
draw_pattern(t,length,depth -1)
t.rigth(120)
darw_pattern(t,length,depth-1)
t.left(60)
draw(t,length,depth -1)
def main()
if _ name_=="main"
sides= int(input("enter number of sides:"))
length= int(input("enter length of sides:"))
depth= int(input("enter depth of recursion:"))
window=turtle.screen()
window.bgcolor("white")
winndow.title("koch snowflake")
t=turtle.turtle()
t.color("white")
t.speed(0)
for i in range(sides)
draw(t,length,depth)

t.right(360/sides)
turtle.done()






