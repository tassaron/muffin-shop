function add_to_cart(e, id) {
    let quantity = 0;
    e.currentTarget.classList.add("btn-disabled");

    const quantityNode = document.querySelector(
        `.ProductPage-quantity[data-product-id='${id}']`
    );
    quantity = Number(quantityNode.innerText);
    const descriptionNode = document.querySelector(
        `.ProductPage-alert-area[data-product-id='${id}']`
    );

    if (quantity == 0) return;
    fetch("{{ url_for('cart.add_product_to_cart', _external=True) }}", {
        method: "POST",
        credentials: "same-origin",
        body: JSON.stringify({ id: id, quantity: quantity }),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
        }),
    }).then(function (response) {
        response.json().then(function (data) {
            if (data["success"] === true) {
                document.getElementById("cart-number").innerText =
                    data["count"];
                const updaterMessage = document.createElement("span");
                updaterMessage.setAttribute(
                    "class",
                    "p-2 text-center alert alert-success"
                );
                updaterMessage.innerText = `Added ${data["change"]} to your cart`;
                descriptionNode.appendChild(updaterMessage);
            }
        });
    });
}
