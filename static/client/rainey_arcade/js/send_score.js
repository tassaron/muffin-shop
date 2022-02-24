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
    }).then((response) => {
        if (response.ok) console.log("success");
    });
}