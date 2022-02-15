/* Child of CartPage, parent of CartPageRows.
 * Handles the Total Price and Submit buttons
 */
import { Component } from "react";

class CartPageColumn extends Component {
    submitCart() {
        fetch("/cart/submit", {
            method: "POST",
            credentials: "same-origin",
            body: JSON.stringify(Array.from(this.props.rowData.values())),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json",
            }),
        }).then(function (response) {
            response.json().then(function (data) {
                if (data["success"] === true) {
                    console.log(data);
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
