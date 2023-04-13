import sys, json

image_suffixes = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
slides = []

with open(sys.argv[1]) as f:
    slide = dict()
    slide["points"] = []
    for l in f:
        l = l[:-1]
        if l.startswith("- "):
            slide["points"].append(l[2:])
        else:
            if "title" in slide:
                slides.append(slide)
                slide = dict()
                slide["points"] = []
            slide["title"] = l
            if any(l.split(" ")[0].lower().endswith(suffix) for suffix in image_suffixes):
                slide["image"] = l.split(" ")[0]
                slide["caption"] = l.split(" ", 1)[1]
    if "title" in slide:
        slides.append(slide)
print """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>""",

print slides[0]["title"]

print """</title>
<style>,
@font-face {
	font-family: Montserrat;
	src: url('Montserrat-Medium.ttf');
}
html {
    cursor: none;
}
body {
    font-family: Montserrat, sans-serif;
    margin: 0;
    padding: 0;
}
#image {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
}
#caption {
	display: none;
	position: fixed;
	top: 0;
	left: 0;
	padding: 1em;
	background: white;
	font-size: 150%;
}
#title {
    color: #4799c8;
    font-size: 400%;
    margin-top: 6vw;
    margin-bottom: 1em;
    margin-left: 10%;
    margin-right: 10%;
}
#points {
    padding: 0;
    margin: 0;
    width: 80%;
    margin-left: 10%;
    font-size: 250%;
}
#points li {
    list-style: none;
    margin-bottom: 1em;
}
</style>
<script>
var slides =""",

print json.dumps(slides),

print """;
</script>
<script>
var index = 0;
function showSlide() {
    if (slides[index].image) {
        document.getElementById("title").innerHTML = "";
        document.getElementById("image").src = slides[index].image;
        document.getElementById("image").style.display = "block";
        document.getElementById("caption").innerHTML = slides[index].caption;
        document.getElementById("caption").style.display = "block";
    } else {
        document.getElementById("title").innerHTML = slides[index].title;
        document.getElementById("image").src = "";
        document.getElementById("image").style.display = "none";
        document.getElementById("caption").style.display = "none";
    }
    document.getElementById("points").innerHTML = slides[index].points.map(function(p) {
        return "<li>" + p + "</li>";
    }).join("");
}

function next() {
    if (index < slides.length - 1) {
        index++;
        showSlide();
    }
}

function prev() {
    if (index > 0) {
        index--;
        showSlide();
    }
}

function keyup(event) {
    if (event.code == "ArrowLeft") {
        prev();
    } else if (event.code == "ArrowRight" || event.code == "Space") {
        next();
    }
}
</script>
</head>
<body onClick="next()" onKeyUp="keyup(event)">
<div style="width: 100%; height: 89px; background-color: #4799c8;">
<img src="sgh.png" style="position: fixed; top: 10px; left: 10px; height: 69px;">
</div>
<img id="image">
<div id="caption"></div>
<div id="title"></div>
<ul id="points"></ul>
<script>
showSlide();
</script>
</body>
</html>
"""
