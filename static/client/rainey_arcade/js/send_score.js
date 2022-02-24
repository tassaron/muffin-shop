function send_score(filename, score, token) {
    fetch("/arcade/token/submit", {
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
        if (!response) return;
        const tokenNode = document.getElementById("arcade_tokens");
        tokenNode.innerText = Number(tokenNode.innerText) + response["payout"];
    });
}