n =  new Date();
y = n.getFullYear();
m = n.getMonth() + 1;
d = n.getDate();

var list = document.getElementsByClassName("date")

for (var i=0; i<list.length;i++){
    list[i].innerHTML = m + "/" + d + "/" + y;
}


