const targetNode = document.body;

const config = { attributes: false, childList: true, subtree: true };

const callback = function (mutationsList, observer) {
    for (const mutation of mutationsList) {
        if (mutation.type === "childList") {
            id_ = mutation.addedNodes[0].id;
            console.log(id_);
            if (id_ == "particles-js") {
                particlesJS.load("particles-js", "assets/particlesjs-config.json", function () {
                    console.log("Particles.js loaded!");
                });
            }
        }
    }
};

const observer = new MutationObserver(callback);

observer.observe(targetNode, config);

// observer.disconnect();