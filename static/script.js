// Function to fetch data from the server
function fetchData() {
    fetch('/get-data') // Fetch data from the server
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            const resultsContainer = document.getElementById('results-container');
            resultsContainer.innerHTML = ''; // Clear previous results

            // Loop through the data and create HTML elements to display each result
            data.forEach(result => {
                const resultElement = document.createElement('div');
                resultElement.textContent = result;
                resultsContainer.appendChild(resultElement);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Event listener for the fetch data button
document.getElementById('fetch-data-btn').addEventListener('click', fetchData);
