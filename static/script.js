function refreshPage() {
    // Display a "Refreshing..." message
    const refreshingMessage = document.createElement('div');
    refreshingMessage.textContent = 'Refreshing...'; // Set an initial message
    refreshingMessage.style.position = 'fixed';
    refreshingMessage.style.top = '50%';
    refreshingMessage.style.left = '50%';
    refreshingMessage.style.transform = 'translate(-50%, -50%)';
    refreshingMessage.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    refreshingMessage.style.color = 'white';
    refreshingMessage.style.padding = '20px';
    refreshingMessage.style.borderRadius = '5px';
    document.body.appendChild(refreshingMessage);

    // Send a GET request to the /refresh route
    fetch('/refresh')
        .then(response => {
            if (response.ok) {
                // If the request was successful, hide the message
                refreshingMessage.style.display = 'none';
                return response.text();
            } else {
                // If there was an error, display an error message
                refreshingMessage.textContent = 'Error refreshing the page.';
                refreshingMessage.style.backgroundColor = 'red';
                refreshingMessage.style.textAlign = 'center';
            }
        })
        .then(data => {
            // Update the content with the response data if needed
            document.getElementById('content').textContent = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
