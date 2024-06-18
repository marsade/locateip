// Latitude and longitude for leaflet
// let reload = true
// if (reload) {
//   window.location = window.location
//   reload = false
// }


function fetchIPAddress() {
  // Fetch the extracted IP address from the backend
  fetch('/get_extracted_ip')
    .then(response => response.json())
    .then(data => {
      if (data.ip_address || data.domain_name) {
        // Use the extracted IP address directly
        console.log('Extracted IP address:', data.ip_address);
        console.log('Extracted domain name:', data.domain_name);
        // Exit the function here since we already have the IP address
        return;
      }
      else {
        FetchAndSendIpAddress();
      }})
    };


function FetchAndSendIpAddress(){
  fetch('/proxy?url=https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            const ipAddress = data.ip;
            console.log('Fetched IP address:', ipAddress);
            // Call a function to send the fetched IP address to the Flask backend
            sendIPAddressToBackend(ipAddress);
            // Proceed with other operations using the fetched IP address
        })
        .catch(error => {
            console.error('Error fetching IP address:', error);
        });
}
// Call the function to fetch the IP address 
// Function to send the IP address to the Flask backend
function sendIPAddressToBackend(ipAddress) {
  const requestData = { ip_address: ipAddress };
  console.log('Sending JSON data to backend:', requestData);
  fetch('/extract_ip', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData) // Send the IP address in the request body
  })
  .then(response => {
      if (response.ok) {
          console.log('IP address sent to backend successfully');
      } else {
          console.error('Failed to send IP address to backend');
      }
  })
  .catch(error => {
      console.error('Error sending IP address to backend:', error);
  });
}

// Call the function to fetch the IP address when the page loads
window.onload = fetchIPAddress;

let lat = document.querySelector('.lat').innerHTML;
let long = document.querySelector('.long').innerHTML;

let map = L.map('map').setView([lat, long], 15);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
let marker = L.marker([lat, long]).addTo(map);