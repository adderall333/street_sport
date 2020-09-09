ymaps.ready(init);
function init(){
    var myMap = new ymaps.Map("map", {
        center: [55.79717499, 49.10240174],
        zoom: 11
    });

    myMap.events.add('click', function (e) {
        let coords = String(e.get("coords"));
        let result = coords.split(',')[0] + " " + coords.split(',')[1];
        document.getElementsByClassName("coordinates")[0].value = result;
    });
}

function showMap(){
    document.getElementsByClassName("add-map")[0].style.display = "block";
}

var control = document.getElementById("img-input");
var label = document.getElementById("img-input-label")
control.addEventListener("change", function(event) {
    len = control.files.length;
    switch (len) {
        case 1:
            label.innerText = "Загружен " + len + " файл";
            break;
        case 2:
        case 3:
        case 4:
            label.innerText = "Загружено " + len + " файла";
            break;
        default:
            label.innerText = "Загружено " + len + " файлов";
            break;
    }
}, false);