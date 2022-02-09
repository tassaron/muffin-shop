function add_to_cart(id) {
    let quantity = 0;
    let target = 0;
    const quantityNodes = document.getElementsByClassName("ProductPage-quantity");
    for (let i=0; i < quantityNodes.length; i++) {
        target = quantityNodes[i].dataset.productId;
        if (target == id) {
            quantity = Number(quantityNodes[i].innerText);
            break;
        }
    }
    delete target;
    if (quantity == 0) return;
    fetch("{{ url_for('cart.add_product_to_cart', _external=True) }}", {
        method: "POST",
        credentials: "same-origin",
        body: JSON.stringify({"id": id, "quantity": quantity}),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function (response) {
        response.json().then(function (data) {
            if (data["success"] === true) {
                document.getElementById("cart-number").innerText = data["count"];
            }
        })
    })
};