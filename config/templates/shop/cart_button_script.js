function add_to_cart(e, id) {
    var productId = id;
    let quantity = 0;
    e.currentTarget.classList.add("btn-disabled");

    const quantityNode = document.querySelector(
        `.ProductPage-quantity[data-product-id='${id}']`
    );
    quantity = Number(quantityNode.innerText);
    const alertArea = document.querySelector(".ProductPage-alert-area");

    if (quantity == 0) return;
    fetch("{{ url_for('cart.add_product_to_cart', _external=True) }}", {
        method: "POST",
        credentials: "same-origin",
        body: JSON.stringify({ id: id, quantity: quantity }),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
            "X-CSRFToken": "{{ csrf_token() }}"
        }),
    }).then(function (response) {
        response.json().then(function (data) {
            if (data["success"] === true) {
                document.getElementById("cart-number").innerText =
                    data["count"];
                const updaterMessage = document.createElement("span");
                updaterMessage.setAttribute(
                    "class",
                    "p-2 text-center alert alert-success cart-alert"
                );
                updaterMessage.innerText = `Added ${data["change"]} to your cart`;
                updaterMessage.setAttribute("data-timestamp", Date.now());
                updaterMessage.setAttribute("data-product-id", productId);
                alertArea.appendChild(updaterMessage);
            }
        });
    });
}
