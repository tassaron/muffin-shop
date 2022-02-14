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
            });
        }
        Array.from(rowNodes).forEach(
            (node) => {
                containerNode.removeChild(node)
            }
        );
        this.state = {
            rowData: rowData
        };
    }

    removeRow(id, ref) {
        const callback = () => {
            this.setState((state, props) => {
                    state.rowData.delete(id);
                    return {
                        rowData: state.rowData,
                    };
                }
            );
        }
        requestAnimationFrame(
            () => animateVanish(ref.current, callback)
        );
    }

    changeQuantity(id, newValue) {
        this.setState((state, props) => {
            const row = state.rowData.get(id);
            row.quantity = row.quantity + newValue;
            return {
                rowData: state.rowData,
            };
        });
    }

    render() {
        return (
            <CartPageColumn rowData={this.state.rowData}>
                {Array.from(this.state.rowData.values()).map((row) => {
                    return (
                        <CartPageRow
                            data={row}
                            key={row.id}
                            removeMe={(ref) => this.removeRow(row.id, ref)}
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
