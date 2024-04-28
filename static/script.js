const backendUrl = 'http://localhost:5000'; // url backend

const askButton = document.getElementById('ask-button');
const questionInput = document.getElementById('question');
const responseText = document.getElementById('response-text');
const loader = document.querySelector('.loader');
const audioContainer = document.querySelector('.audio-controls');
const audioPlayer = document.getElementById('audio-player');
const downloadButton = document.getElementById('download-button');


window.onload = () => {
    questionInput.value = '';
};

askButton.addEventListener('click', () => {
    const question = questionInput.value;
    if (!question) {
        alert('Apetraho aloha ny fanontanianao');
        return;
    }

    // Loading eto
    loader.classList.remove('hidden');
    responseText.classList.add('hidden');
    audioContainer.classList.add('hidden');
    downloadButton.classList.add('hidden');

    // Manao appel api
    fetch(`${backendUrl}/read?prompt=${question}`, {
        method: 'POST',
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        // body: JSON.stringify({ prompt: question })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Nisy olana kely tany amin'ny serivera");
        }
        return response.json();
    })
    .then(data => {
        // Mi'afficher reponse
        responseText.textContent = data.message;
        responseText.classList.remove('hidden');
        loader.classList.add('hidden');

        // Source audio file
        audioPlayer.src = "static/out.mp3";
        audioContainer.classList.remove('hidden');
        downloadButton.href = "static/out.mp3";
        downloadButton.classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        // gestion erreur
        responseText.textContent = "Nisy olana kely tany amin'ny serveur";
        responseText.classList.remove('hidden');
        loader.classList.add('hidden');
    });
});
