import random, time, math
from pyprocessing import *
from graph import LongestPath

longest_path = LongestPath()

size(1440,760)
			
def draw():
	background(255);
	noStroke();
	smooth()
	
	font = createFont("Times New Roman Bold", 15)
	textFont(font); 
	fill(88,140,140)
	text("Longest Path Problem", 30, 40)
	
	font = createFont("Times New Roman Bold", 12)
	textFont(font); 
	fill(88,140,140)
	text("Score: %s, Sum: %s" % (longest_path.max_edge['value'], longest_path.sum_to[longest_path.max_edge['id'].destination]), 30, 40+20)
	
	x_difference = 540
	line_path = longest_path.line_path
	
	for i in range(len(line_path)-1):
		stroke(0,0,0)
		strokeWeight(3)
		line(line_path[i].x, line_path[i].y, line_path[i+1].x, line_path[i+1].y)
		comparison_point = line_path[i]
	
	for point in line_path:
		fill(255,255,255)
		stroke(217, 4, 43)
		strokeWeight(2)
		ellipse(point.x, point.y, 18, 18)
	
		font = createFont("Times New Roman", 7); 
		textFont(font); 
		fill(0,0,0)
		text(str(longest_path.cordinate_hash[point].get_value()), point.x-4, point.y+3);
		
	for points in longest_path.P:
		stroke(0,0,0)
		strokeWeight(1)
		line(points[0].x, points[0].y, points[1].x, points[1].y)
		
	for i in range(len(line_path)-1):
		stroke(0,0,0)
		strokeWeight(3)
		line(line_path[i].x-x_difference, line_path[i].y, line_path[i+1].x-x_difference, line_path[i+1].y)
	
	for vertex in longest_path.VP:
		fill(255,255,255)
		stroke(217, 4, 43)
		strokeWeight(2)
		point = vertex.point
		x = vertex.point.x
		y = vertex.point.y
		ellipse(x, y, 18, 18)
	
		font = createFont("Times New Roman", 8); 
		textFont(font); 
		fill(0,0,0)
		text(str(longest_path.sum_to[vertex]), x-5, y+25);
		
		if vertex.get_value() >= 10:
			font = createFont("Times New Roman", 7)
			textFont(font); 
			fill(0,0,0)
			text(str(vertex.get_value()), x-4, y+3)
		else:
			font = createFont("Times New Roman", 7)
			textFont(font); 
			fill(0,0,0)
			text(str(vertex.get_value()), x-2, y+3)
			
def mouseClicked():
	globals()["longest_path"] = LongestPath()
	
run()