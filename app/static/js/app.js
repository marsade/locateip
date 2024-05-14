let lat = document.querySelector('.lat').innerHTML;
let long = document.querySelector('.long').innerHTML;

let map = L.map('map').setView([lat, long], 15);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
let marker = L.marker([lat, long]).addTo(map);