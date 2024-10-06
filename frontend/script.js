document.getElementById('url-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const urlInput = document.getElementById('url-input').value;
    const reviewsContainer = document.getElementById('reviews-container');
    
    // Clear previous reviews
    reviewsContainer.innerHTML = '';

    try {
        const response = await fetch(`http://<YOUR_RENDER_APP_URL>/api/reviews?url=${encodeURIComponent(urlInput)}`);
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data.reviews_count === 0) {
            reviewsContainer.innerHTML = '<p>No reviews found.</p>';
            return;
        }

        // Display reviews
        data.reviews.forEach(review => {
            const reviewElement = document.createElement('div');
            reviewElement.classList.add('review');
            reviewElement.innerHTML = `
                <h2>${review.title}</h2>
                <p><strong>Reviewer:</strong> ${review.reviewer}</p>
                <p><strong>Rating:</strong> ${review.rating}</p>
                <p>${review.body}</p>
                <hr>
            `;
            reviewsContainer.appendChild(reviewElement);
        });

    } catch (error) {
        reviewsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
