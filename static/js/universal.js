//THIS IS A HACK -- I DON'T KNOW WHY IT WORKS BUT IT DOES
//TAKES IN DATA AND SENDS BACK OUT THE SAME DATA SO IT CAN WORK IN HTML
function myFunc(vars) {
    return vars
}

function onEachFeature(feature, layer) {
      layer.bindTooltip('<h1><p>Creole Language: '+feature.properties.creole_language+'</p></h1>'+'<p>Creole Word: '+feature.properties.creole_word+'</p>'
      +'<p>English/French Word: '+feature.properties.word+'</p>'+'<p>Acrolect: '+feature.properties.acrolect+'</p>');
}

//Creating the map
var map = L.map('map').fitWorld();
map.setZoom(3);

//Adding OpenStreemap credits -- this needs to be here legally speaking
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);