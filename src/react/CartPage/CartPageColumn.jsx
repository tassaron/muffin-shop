/* Child of CartPage, parent of CartPageRows.
 * Handles the Total Price and Submit buttons
 */
import { Component } from "react";

class CartPageColumn extends Component {
    rowData_to_CartData() {
        const cartData = {};

        for (let row of this.props.rowData.values()) {
            cartData[row.id] = row.quantity;
        }

        return cartData;
    }

    submitCart() {
        fetch("/cart/submit", {
            method: "POST",
            credentials: "same-origin",
            body: JSON.stringify(this.rowData_to_CartData()),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json",
                "X-CSRFToken": this.props.token,
            }),
        }).then((response) => {
            response.json().then((data) => {
                if (data["success"] === true) {
                    window.location.href = data["session_url"];
                } else {
                    // The product stock must've changed!
                    for (const [id, quantity] of Object.entries(
                        data["changed_quantities"]
                    )) {
                        this.props.setQuantity(id, quantity);
                    }
                }
            });
        });
    }

    render() {
        return (
            <>
                {this.props.children}
                {this.props.totalPrice > 0 ? (
                    <>
                        <div className="row mt-2 border-top">
                            <div className="col-md-5 col-3 d-flex justify-content-end text-decoration-underline">
                                total price
                            </div>
                            <div className="col-2 text-center">
                                ${this.props.totalPrice.toFixed(2)}
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-8 d-flex justify-content-end">
                                <button
                                    onClick={() => {
                                        this.submitCart();
                                    }}
                                    type="button"
                                    className="btn-default btn-next btn-round shadow-sm"
                                >
                                    Submit
                                </button>
                            </div>
                        </div>
                    </>
                ) : (
                    <></>
                )}
            </>
        );
    }
}

export default CartPageColumn;
