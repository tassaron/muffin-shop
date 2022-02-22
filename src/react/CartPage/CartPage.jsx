/* This component is the root of the Cart View. It gets the initial cart data
 * from the HTML. It owns all state and the methods to change state are passed as props
 * to the CartPageColumn and its children, the CartPageRows.
 */
import React, { Component } from "react";
import CartPageColumn from "./CartPageColumn";
import CartPageRow from "./CartPageRow";
import { getNodeOrError, animateVanish } from "../util";

class CartPage extends Component {
    constructor() {
        super();
        const containerNode = getNodeOrError("CartPage-container");
        const rowNodes = document.getElementsByClassName("CartPage-row");
        const rowData = new Map();
        for (let node of rowNodes) {
            rowData.set(node.dataset.productId, {
                id: node.dataset.productId,
                name: node.getElementsByClassName("CartPage-name")[0].innerText,
                image: node
                    .getElementsByClassName("CartPage-image")[0]
                    .children[0].getAttribute("src"),
                price: Number(
                    node
                        .getElementsByClassName("CartPage-price")[0]
                        .innerText.slice(1)
                ),
                quantity: Number(
                    node.getElementsByClassName("CartPage-quantity")[0]
                        .innerText
                ),
                stock: Number(
                    node
                        .getElementsByClassName("CartPage-stock")[0]
                        .innerText.split(" ")[0]
                ),
                changed: false,
            });
        }
        Array.from(rowNodes).forEach((node) => {
            containerNode.removeChild(node);
        });
        this.state = {
            rowData: rowData,
        };
    }

    removeRow(id, ref) {
        const callback = () => {
            this.setState((state, props) => {
                state.rowData.delete(id);
                return {
                    rowData: state.rowData,
                };
            });
        };
        fetch("/cart/del", {
            method: "POST",
            credentials: "same-origin",
            body: JSON.stringify({ id: id }),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json",
            }),
        }).then(function (response) {
            response.json().then(function (data) {
                if (data["success"] === true) {
                    const cartNumberNode =
                        document.getElementById("cart-number");
                    cartNumberNode.innerText =
                        Number(cartNumberNode.innerText) - 1;
                }
            });
        });
        requestAnimationFrame(() => animateVanish(ref.current, callback));
    }

    setQuantityRelative(id, newValue) {
        this.setState((state, props) => {
            const row = state.rowData.get(id);
            row.quantity = row.quantity + newValue;
            row.changed = false;
            return {
                rowData: state.rowData,
            };
        });
    }

    setQuantity(id, newValue) {
        this.setState((state, props) => {
            const row = state.rowData.get(id);
            row.quantity = newValue;
            row.stock = newValue;
            row.changed = true;
            return {
                rowData: state.rowData,
            };
        });
    }

    render() {
        return (
            <CartPageColumn
                rowData={this.state.rowData}
                totalPrice={Array.from(this.state.rowData.values()).reduce(
                    (prev, curr) => prev + curr.price * curr.quantity,
                    0
                )}
                setQuantity={(id, newValue) => this.setQuantity(id, newValue)}
            >
                {this.state.rowData.size == 0 ? (
                    <div className="row">
                        <div className="col-4"></div>
                        <div className="my-4 text-center p-5 fs-5">
                            Your shopping cart is empty.
                        </div>
                        <div className="col-4"></div>
                    </div>
                ) : (
                    Array.from(this.state.rowData.values()).map((row) => {
                        return (
                            <CartPageRow
                                data={row}
                                key={row.id}
                                removeMe={(ref) => this.removeRow(row.id, ref)}
                                setQuantityRelative={(newValue) =>
                                    this.setQuantityRelative(row.id, newValue)
                                }
                            />
                        );
                    })
                )}
            </CartPageColumn>
        );
    }
}

export default CartPage;
