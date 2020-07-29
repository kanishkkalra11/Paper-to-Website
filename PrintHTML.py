import math


def HTML_CSS(box_list,f,page_width):
    f.write("<!DOCTYPE HTML>\n<HTML lang=\"en\">\n")
    f.write("<Head>\n<Title> demo </Title> \n<meta charset=\"utf-8\"> \n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> \n<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\"> \n<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script> \n<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js\"></script> \n<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js\"></script> \n</Head>\n")
    f.write("<Body>\n<div class=\"container-fluid\" style=\"position:absolute\">\n")
    for i in range(len(box_list)-1,-1,-1):
        if box_list[i].tag=="text":
            f.write("<text style=\"position:absolute;left:{}px;top:{}px;font-size:{}px;font-family:Bodoni Bd BT;\">{}</text>\n".format(box_list[i].x1,box_list[i].y1,box_list[i].size,box_list[i].text))
        else:
            f.write("<img src=\"demo-image.jpg\" alt=\"ImageHere\" style=\"position:absolute;left:{}px;top:{}px;\" width=\"{}\" height=\"{}\"/>\n".format(box_list[i].x1, box_list[i].y1, box_list[i].x2-box_list[i].x1, box_list[i].y2-box_list[i].y1))
    f.write("</div>\n</Body>\n</HTML>")


def HTML_CSS_BOOTSTRAP(box_list,f,page_width):
    l = len(box_list)
    curr_range = [box_list[0].y1, box_list[0].y2]
    hierarchy = list()
    row = list()
    for i in range(l):
        if(box_list[i].y1<=curr_range[1]):
            row.append(box_list[i])
            if(box_list[i].y2>curr_range[1]+100):
                curr_range[1]=box_list[i].y2
        else:
            row.sort(key=lambda x: x.x1)
            hierarchy.append(row)
            row = list()
            row.append(box_list[i])
            curr_range = [box_list[i].y1, box_list[i].y2]
    hierarchy.append(row)
    
    for row in hierarchy:
        row.sort(key=lambda x:x.x1)
        
    #for i in hierarchy:
    #    for j in i:
    #        print(j.x1,j.tag, j.text)
    #    print()
    
    hierarchy_1 = list()
    for row in hierarchy:
        l = len(row)
        curr_range = [row[0].x1, row[0].x2]
        row_1 = list()
        col = list()
        for i in range(l):
            if(row[i].x1<=curr_range[1]):
                col.append(row[i])
                if(row[i].x2>curr_range[1]+100):
                    curr_range[1]=row[i].x2
            else:
                col.sort(key=lambda x:x.y1)
                row_1.append(col)
                col = list()
                col.append(row[i])
                curr_range = [row[i].x1, row[i].x2]
        row_1.append(col)
        for col in row_1:
            col.sort(key=lambda x:x.y1)
        hierarchy_1.append(row_1)
    
    #for row in hierarchy_1:
    #    for i in row:
    #        for j in i:
    #            print(j.tag)
    #        print()
    #    print(',')
    
    for row in hierarchy_1:
        x_prev = 0
        c = 12
        for i in range(len(row)):
            if(i==len(row)-1):
                max_x = page_width
                row[i].append(c)
                break
            max_x = (max(row[i],key=lambda x: x.x2)).x2
            min_x = (min(row[i+1],key=lambda x:x.x1)).x1
            k = math.floor(((max_x+min_x-(2*x_prev))*6)/page_width)
            x_prev = (max_x + min_x)/2
            c = c - k
            row[i].append(k)
    
    #for row in hierarchy_1:
    #    for col in row:
    #        print(col)
    

    #PRINT HTML CODE
    f.write("<!DOCTYPE HTML>\n<HTML lang=\"en\">\n")
    f.write("<Head>\n<Title> demo </Title> \n<meta charset=\"utf-8\"> \n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> \n<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\"> \n<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script> \n<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js\"></script> \n<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js\"></script> \n</Head>\n")
    f.write("<Style>\ndiv{padding: 5px;}\n</Style>")
    f.write("<Body>\n<div class=\"container-fluid\" style=\"margin:2%\">\n")
    
    for row in hierarchy_1:
        f.write("\t<div class=\"row\">\n")
        l = len(row)
        for col in row:
            span = col[-1]
            f.write("\t\t<div class=\"col-sm-{}\">\n".format(span))
            for i in range(len(col)-1):
                if((len(col)-1)>1):
                    f.write("\t\t\t<div>\n")
                
                if(col[i].tag=="text"):
                    f.write("\t\t\t\t<p style=\"font-size:{}px;font-family:Bodoni Bd BT\">{}</p>\n".format(col[i].size,col[i].text))
                elif(col[i].tag=="Image"):
                    w = (col[i].x2-col[i].x1)*page_width/page_width
                    h = ((col[i].y2-col[i].y1)/(col[i].x2-col[i].x1))*w
                    f.write("\t\t\t\t<img src=\"demo-image.jpg\" alt=\"ImageHere\" width=\"{}\" height=\"{}\"/>\n".format(w,h))
                
                if((len(col)-1)>1):
                    f.write("\t\t\t</div>\n")
            f.write("\t\t</div>\n")
        f.write("\t</div>\n")
    
    f.write("</div>\n</Body>\n</HTML>")