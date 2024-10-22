const characterCardTemplate = document.querySelector('#character-card-template');
const characterCardContainer = document.querySelector('#character-card-container');
const searchInput = document.querySelector('#search-input');

let characters = [];

// Fetch the data once when the page loads
fetch('https://jsonplaceholder.typicode.com/users')
    .then(res => res.json())
    .then(data => {
        characters = data.map(character => {
            const card = characterCardTemplate.content.cloneNode(true).children[0];
            const name = card.querySelector('.character-name'); // Correct selector
            const content = card.querySelector('.content'); // Correct selector
            name.textContent = character.name;
            content.textContent = character.email;
            characterCardContainer.appendChild(card);
            return { name: character.name.toLowerCase(), email: character.email.toLowerCase(), element: card };
        });
    })
    .catch(error => console.error('Error fetching data:', error));

// Filter characters based on search input
searchInput.addEventListener('input', e => {
    const searchValue = e.target.value.toLowerCase();
    characters.forEach(character => {
        const isVisible = character.name.includes(searchValue) || character.email.includes(searchValue);
        character.element.classList.toggle('hidden', !isVisible);
    });
});
