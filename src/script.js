document.getElementById('spamButton').addEventListener('click', function() {
    const nglUsername = document.getElementById('nglUsername').value;
    const message = document.getElementById('message').value;
    const count = document.getElementById('count').value;
    const statusDiv = document.getElementById('status');
    const resultsList = document.getElementById('results');

    resultsList.innerHTML = ''; // Clear previous results
    statusDiv.textContent = 'Sedang menjalankan spam...';

    fetch('/api/spam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nglusername: nglUsername, message: message, count: count })
    })
    .then(response => response.json())
    .then(data => {
        statusDiv.textContent = 'Spam selesai!';
        data.results.forEach((result, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = `Pesan ${index + 1}: ${result ? 'Berhasil' : 'Gagal'}`;
            resultsList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        statusDiv.textContent = 'Terjadi kesalahan saat mengirim spam.';
    });
});
