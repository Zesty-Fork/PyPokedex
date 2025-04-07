document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("content");

    // Function to create a new post
    function createPost(text) {
        const post = document.createElement("div");
        post.className = "post";
        post.textContent = text;
        content.appendChild(post);
    }

    // Simulate loading posts
    for (let i = 1; i <= 10; i++) {
        createPost(`This is post number ${i}`);
    }

    // Infinite scrolling
    window.addEventListener("scroll", () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            for (let i = 1; i <= 5; i++) {
                createPost(`This is a new post`);
            }
        }
    });
});