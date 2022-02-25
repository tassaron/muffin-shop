function send_score(filename, score, token) {
    fetch("/token/submit", {
        method: "POST",
        credentials: "same-origin",
        body: JSON.stringify({ filename: filename, score: score }),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
            "X-CSRFToken": token,
        }),
    }).then(
        response => response.ok ? response.json() : null
    ).then((response) => {
        if (!response || response["payout"] < 1) return;
        const tokenNode = document.getElementById("arcade_tokens");
        tokenNode.innerText = Number(tokenNode.innerText) + response["payout"];
        tokenNode.parentElement.classList.remove("d-none");
    });
}


function hide_send_score_button() {
    const send_score_button = document.getElementById("send_score_button");
    send_score_button.setAttribute("style", "display: none;");

    // Remove event listeners by cloning the button
    // sorta hacky but it's good enough for now
    const clone = send_score_button.cloneNode(true);
    send_score_button.parentNode.replaceChild(clone, send_score_button);
}