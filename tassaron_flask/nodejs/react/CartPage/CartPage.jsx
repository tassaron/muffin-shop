import React, { Component } from "react";
import CartPageColumn from "./CartPageColumn";
import CartPageRow from "./CartPageRow";
import { getNodeOrError } from "../util";

class CartPage extends Component {
    constructor() {
        super();
        const containerNode = getNodeOrError("CartPage-container");
        const rowNodes = document.getElementsByClassName("CartPage-row");
        const rowMap = new Map();
        for (let node of rowNodes) {
            rowMap.set(node.dataset.productId, {
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
            });
            containerNode.removeChild(node);
        }
        this.state = {
            rows: rowMap,
        };
    }

    removeRow(id) {
        this.setState((state, props) => {
            state.rows.delete(id);
            return {
                rows: state.rows,
            };
        });
    }

    changeQuantity(id, newValue) {
        this.setState((state, props) => {
            const row = state.rows.get(id);
            row.quantity = row.quantity + newValue;
            return {
                rows: state.rows,
            };
        });
    }

    render() {
        return (
            <CartPageColumn>
                {Array.from(this.state.rows.values()).map((row) => {
                    return (
                        <CartPageRow
                            data={row}
                            removeMe={() => this.removeRow(row.id)}
                            changeQuantity={(newValue) =>
                                this.changeQuantity(row.id, newValue)
                            }
                        />
                    );
                })}
            </CartPageColumn>
        );
    }
}

export default CartPage;
