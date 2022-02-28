import { animateVanish } from "../../../js/util.js";

export const send_score = function(filename, score, token) {
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
        if (!response) {
            return;
        }

        // Create a floating alert
        const alertArea = document.getElementById("score-alert-area");
        const updaterMessage = document.createElement("span");
        const tokenNode = document.getElementById("arcade_tokens");
        const old_value = Number(tokenNode.innerText);
        const new_value = old_value + response["payout"];
        let alert_message;

        updaterMessage.setAttribute(
            "class",
            "p-2 text-center alert alert-warning cart-alert"
        );
        updaterMessage.setAttribute("data-timestamp", Date.now());

        if (response["payout"] < 1) {
            updaterMessage.setAttribute(
                "class",
                "p-2 text-center alert alert-warning cart-alert"
            );
            alert_message = "Score too low";
        } else {
            updaterMessage.setAttribute(
                "class",
                "p-2 text-center alert alert-success cart-alert"
            );
            alert_message = `Got ${new_value} token`;            
        }
        if (response["payout"] > 1) {
            alert_message += "s";
        }
        updaterMessage.innerText = alert_message;
        alertArea.appendChild(updaterMessage);

        // Make the alert disappear later
        const doAnimation = () => {
            requestAnimationFrame(() =>
                animateVanish(updaterMessage, () => {
                    alertArea.removeChild(updaterMessage);
                })
            );
        };
        setTimeout(doAnimation, 3000);

        // Update the non-floating banner
        if (response["payout"] < 1) return;
        tokenNode.innerText = new_value;
        if (new_value == 1 || old_value == 1) {
            // pluralize/depluralize the human language (a strange one indeed)
            const tokenWordNode = document.getElementById("arcade_tokens_word");
            tokenWordNode.innerText = new_value == 1 ? (
                tokenWordNode.innerText.substring(0, tokenWordNode.innerText.length - 1)
            ) : (
                tokenWordNode.innerText + "s"
            )
        }
        tokenNode.parentElement.classList.remove("d-none");
    });
}


export const hide_send_score_button = function() {
    const send_score_button = document.getElementById("send_score_button");
    send_score_button.setAttribute("style", "display: none;");

    // Remove event listeners by cloning the button
    // sorta hacky but it's good enough for now
    const clone = send_score_button.cloneNode(true);
    send_score_button.parentNode.replaceChild(clone, send_score_button);
}