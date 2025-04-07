document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("content");

    document.getElementById("comboGames").onchange = onComboGamesChanged;

    function onComboGamesChanged(event){
         var id = event.id.value;
         loadGamePokedexes(id)
    };

    // (A) LOAD CATEGORY SELECTOR
    // level 1 = main category
    // level 2 = sub category
    function loadGamePokedexes (var id) {
        // (A1) GET SELECTED PARENT ID
        var data = new FormData();
        data.append("id", (level==1 ? 0 : document.getElementById("cat1").value));

        // (A2) AJAX FETCH CATEGORIES
        fetch("/getcat", { method: "POST", body: data })
            .then(res => res.json())
            .then(cat => {
                // (A2-1) UPDATE HTML SELECTOR
                let selector = document.getElementById("cat" + level);
                selector.innerHTML = "";
                for (let c of cat) {
                    let opt = document.createElement("option");
                    opt.value = c[0];
                    opt.innerHTML = c[1];
                    selector.appendChild(opt);
                }

                // (A2-2) CASCADE LOAD SUB-CATEGORY
                if (level==1) { loadcat(2); }
            });
    }

    // (B) INIT LOAD
    window.onload = () => loadGamePokedexes(1);
        /*
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
        */
});